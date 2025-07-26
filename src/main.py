import cv2
import time
import yaml
import pandas as pd
import warnings
from pathlib import Path
from detectors.yolo_detector import YOLODetector
from tracking.centroid_tracker import CentroidTracker
from tracking.ocsort_tracker import OCSort
from counting.counter import FlowCounter
import numpy as np

# Suppress warnings for cloud deployment
warnings.filterwarnings("ignore", category=SyntaxWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

def load_config():
    with open("src/config.yaml") as f:
        return yaml.safe_load(f)

def inside_polygon_mask(shape, polygon):
    mask = np.zeros(shape[:2], dtype=np.uint8)
    pts = np.array([polygon], dtype=np.int32)
    cv2.fillPoly(mask, pts, 255)
    return mask

def main():
    cfg = load_config()
    model = YOLODetector(cfg["model"]["weights"])
    video_srcs = cfg["video_sources"]
    tracker_type = cfg.get("model", {}).get("tracker", "ocsort").lower()

    logs_path = Path("data/outputs/metrics.csv")
    logs_path.parent.mkdir(parents=True, exist_ok=True)

    for cam in video_srcs:
        cap = cv2.VideoCapture(cam["path"])
        if tracker_type == "ocsort":
            tracker = OCSort()
        else:
            tracker = CentroidTracker()
        counter = FlowCounter(cam["roi"])
        roi_mask = None
        heatmap = None
        last_log_time = time.time()
        counts_acc = 0

        # --- Add VideoWriter for overlayed video ---
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        fps = cap.get(cv2.CAP_PROP_FPS) or 25
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        out = cv2.VideoWriter("data/outputs/overlayed_video.mp4", fourcc, fps, (width, height))

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if roi_mask is None:
                roi_mask = inside_polygon_mask(frame.shape, cam["roi"])
                heatmap = np.zeros(frame.shape[:2], dtype=np.float32)

            boxes, scores, classes = model.infer(frame)
            box_list = [b.flatten() for b in boxes]
            tracks = tracker.update(box_list)

            # draw ROI
            cv2.polylines(frame, [np.array(cam["roi"], dtype=np.int32)], True, (0,255,255), 2)

            # draw boxes & ids
            for oid, centroid in tracks.items():
                # Extract scalar values to avoid NumPy deprecation warnings
                cx, cy = float(centroid[0]), float(centroid[1])
                cv2.circle(frame, (int(cx), int(cy)), 4, (0,255,0), -1)
                cv2.putText(frame, f"ID:{oid}", (int(cx)+5, int(cy)-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)

            in_c, out_c = counter.update(tracks)

            # heatmap accumulation for motion in ROI
            for oid, c in tracks.items():
                # Extract scalar values to avoid NumPy deprecation warnings
                x, y = int(float(c[0])), int(float(c[1]))
                if roi_mask[y, x] > 0:
                    heatmap[y, x] += 1

            # render heatmap overlay
            hm = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            hm_color = cv2.applyColorMap(hm, cv2.COLORMAP_JET)
            overlay = cv2.addWeighted(frame, 0.7, hm_color, 0.3, 0)
            frame = overlay

            cv2.putText(frame, f"IN: {in_c}  OUT: {out_c}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

            # --- Write overlayed frame to video ---
            # Ensure frame is 3-channel BGR for VideoWriter
            if len(frame.shape) == 2 or frame.shape[2] == 1:
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            out.write(frame)

            # --- Save latest frame for dashboard live stream ---
            cv2.imwrite("data/outputs/live_frame.jpg", frame)

            # Skip GUI display in cloud environment
            # cv2.imshow(f"Cam {cam['id']}", frame)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

            # aggregate & log every N seconds (e.g., 5)
            if time.time() - last_log_time > 5:
                now = pd.Timestamp.utcnow()
                total = in_c - out_c
                row = {
                    "timestamp": now,
                    "camera": cam["id"],
                    "in": in_c,
                    "out": out_c,
                    "active": len(tracks),
                    "net": total
                }
                counts_acc += total
                pd.DataFrame([row]).to_csv(logs_path, mode="a", header=not logs_path.exists(), index=False)
                last_log_time = time.time()

        cap.release()
        out.release()
        break  # Only process the first camera/video for overlayed video
    # cv2.destroyAllWindows()  # Skip in cloud environment

if __name__ == "__main__":
    main()

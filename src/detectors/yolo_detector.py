from ultralytics import YOLO
import numpy as np

class YOLODetector:
    def __init__(self, weights: str = "yolov8n.pt", conf: float = 0.3, iou: float = 0.45):
        self.model = YOLO(weights)
        self.conf = conf
        self.iou = iou

    def infer(self, frame):
        results = self.model.predict(source=frame, stream=False, conf=self.conf, iou=self.iou, verbose=False)
        boxes_xyxy = []
        scores = []
        classes = []
        for r in results:
            for b, c, s in zip(r.boxes.xyxy.cpu().numpy(),
                               r.boxes.cls.cpu().numpy(),
                               r.boxes.conf.cpu().numpy()):
                boxes_xyxy.append(b.astype(np.float32))
                scores.append(float(s))
                classes.append(int(c))
        return np.array(boxes_xyxy), np.array(scores), np.array(classes) 
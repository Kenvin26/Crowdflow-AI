import streamlit as st
import requests
import pandas as pd
import time
import os
import yaml
import subprocess
import cv2
import numpy as np
import sys

def main():
    st.set_page_config(page_title="CrowdFlow AI Dashboard", layout="wide")
    st.title("CrowdFlow AI Dashboard")

    API_URL = "http://localhost:8000/metrics/latest"
    METRICS_PATH = "data/outputs/metrics.csv"
    CONFIG_PATH = "src/config.yaml"
    VIDEO_DIR = "data/videos/"

    # Create directories if they don't exist
    os.makedirs(VIDEO_DIR, exist_ok=True)
    os.makedirs("data/outputs", exist_ok=True)
    os.makedirs("data/logs", exist_ok=True)

    # Sidebar: Video upload/record/selection
    st.sidebar.header("Video Input")
    video_file = st.sidebar.file_uploader("Upload a video file", type=["mp4", "avi", "mov"])
    record = st.sidebar.button("Record from webcam (save as input)")

    # List available videos
    video_files = [f for f in os.listdir(VIDEO_DIR) if f.endswith((".mp4", ".avi", ".mov"))]
    selected_video = st.sidebar.selectbox("Select a video to analyze", video_files if video_files else [None])

    video_path = None
    if video_file is not None:
        video_path = os.path.join(VIDEO_DIR, f"uploaded_{int(time.time())}.mp4")
        with open(video_path, "wb") as f:
            f.write(video_file.read())
        st.sidebar.success(f"Uploaded video saved as {video_path}")
        selected_video = os.path.basename(video_path)

    if record:
        video_path = os.path.join(VIDEO_DIR, f"recorded_{int(time.time())}.mp4")
        st.sidebar.info("Recording from webcam... (press 'q' to stop)")
        # Note: Webcam recording is disabled in Streamlit Cloud for security
        st.sidebar.warning("Webcam recording is not available in Streamlit Cloud")
        selected_video = None

    # Show video preview
    if selected_video and os.path.exists(os.path.join(VIDEO_DIR, selected_video)):
        st.video(os.path.join(VIDEO_DIR, selected_video))
        # ROI and overlay visualization
        try:
            with open(CONFIG_PATH, "r") as f:
                cfg = yaml.safe_load(f)
            roi = cfg["video_sources"][0]["roi"] if "roi" in cfg["video_sources"][0] else None
            frame = None
            cap = cv2.VideoCapture(os.path.join(VIDEO_DIR, selected_video))
            ret, frame = cap.read()
            cap.release()
            if ret and frame is not None:
                overlay = frame.copy()
                if roi:
                    roi_np = np.array(roi, dtype=np.int32)
                    cv2.polylines(overlay, [roi_np], isClosed=True, color=(0,255,255), thickness=2)
                # Try to load real tracks from data/outputs/tracks.csv
                tracks_path = "data/outputs/tracks.csv"
                if os.path.exists(tracks_path):
                    # Expected columns: frame, id, x1, y1, x2, y2, cx, cy
                    tracks_df = pd.read_csv(tracks_path)
                    # Show only tracks for the first frame
                    first_frame = 0
                    if not tracks_df.empty:
                        first_frame = tracks_df["frame"].min()
                        tracks = tracks_df[tracks_df["frame"] == first_frame]
                        for _, row in tracks.iterrows():
                            x1, y1, x2, y2 = int(row["x1"]), int(row["y1"]), int(row["x2"]), int(row["y2"])
                            cx, cy = int(row["cx"]), int(row["cy"])
                            track_id = int(row["id"])
                            cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 255, 0), 2)
                            cv2.circle(overlay, (cx, cy), 6, (0,255,0), -1)
                            cv2.putText(overlay, f"ID:{track_id}", (cx+8, cy-8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
                else:
                    # Fallback: show demo overlay
                    if roi:
                        h, w = overlay.shape[:2]
                        for i in range(5):
                            cx, cy = np.random.randint(roi_np[:,0].min(), roi_np[:,0].max()), np.random.randint(roi_np[:,1].min(), roi_np[:,1].max())
                            cv2.circle(overlay, (cx, cy), 6, (0,255,0), -1)
                            cv2.putText(overlay, f"ID:{i+1}", (cx+8, cy-8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
                st.image(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB), caption="ROI and Tracks (real if available)", use_container_width=True)
        except Exception as e:
            st.error(f"Error processing video preview: {e}")

    # Show overlayed video if available
    overlayed_video_path = "data/outputs/overlayed_video.mp4"
    if os.path.exists(overlayed_video_path):
        st.subheader("Video with Overlays (ROI, Tracks, Heatmap)")
        st.video(overlayed_video_path)
    else:
        if selected_video and os.path.exists(os.path.join(VIDEO_DIR, selected_video)):
            st.subheader("Original Video Preview")
            st.video(os.path.join(VIDEO_DIR, selected_video))

    # --- Metrics and Charts (existing code) ---
    # Update config.yaml and trigger processing if new video selected
    if selected_video:
        try:
            with open(CONFIG_PATH, "r") as f:
                cfg = yaml.safe_load(f)
            if cfg["video_sources"][0]["path"] != os.path.join(VIDEO_DIR, selected_video):
                cfg["video_sources"][0]["path"] = os.path.join(VIDEO_DIR, selected_video)
                with open(CONFIG_PATH, "w") as f:
                    yaml.safe_dump(cfg, f)
                # Show progress bar while processing
                with st.spinner("Processing video and generating metrics..."):
                    try:
                        st.sidebar.info("Processing video...")
                        result = subprocess.run([sys.executable, "src/main.py"], capture_output=True, text=True)
                        if result.returncode == 0:
                            st.sidebar.success("Video processed and metrics updated!")
                        else:
                            st.sidebar.error(f"Processing failed: {result.stderr}")
                    except Exception as e:
                        st.sidebar.error(f"Processing failed: {e}")
        except Exception as e:
            st.error(f"Error updating configuration: {e}")

    # Load metrics history
    if os.path.exists(METRICS_PATH):
        try:
            df = pd.read_csv(METRICS_PATH)
            if not df.empty:
                # Show last N events
                st.subheader("Recent Events")
                st.dataframe(df.tail(10).reset_index(drop=True))
                # Plot time series charts
                st.subheader("Metrics Over Time")
                chart_cols = st.columns(4)
                with chart_cols[0]:
                    st.line_chart(df["active"])
                    st.caption("Active Count")
                with chart_cols[1]:
                    st.line_chart(df["in"])
                    st.caption("In Count")
                with chart_cols[2]:
                    st.line_chart(df["out"])
                    st.caption("Out Count")
                with chart_cols[3]:
                    st.line_chart(df["net"])
                    st.caption("Net Count")
            else:
                st.warning("Metrics file is empty. Please process a video.")
        except Exception as e:
            st.error(f"Error loading metrics: {e}")
    else:
        st.info("No metrics available yet. Please upload and process a video.")

if __name__ == "__main__":
    main() 
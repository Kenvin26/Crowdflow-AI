#!/usr/bin/env python3
"""
CrowdFlow AI - Simple Streamlit Cloud Deployment
Basic version without OpenCV dependencies
"""

import streamlit as st
import pandas as pd
import numpy as np
import time
import os
import yaml

def main():
    st.set_page_config(page_title="CrowdFlow AI Dashboard", layout="wide")
    st.title("CrowdFlow AI Dashboard")
    
    st.info("🎯 This is a simplified version for Streamlit Cloud deployment. For full functionality, run locally.")

    # Create directories if they don't exist
    os.makedirs("data/videos", exist_ok=True)
    os.makedirs("data/outputs", exist_ok=True)
    os.makedirs("data/logs", exist_ok=True)

    # Sidebar
    st.sidebar.header("Video Input")
    video_file = st.sidebar.file_uploader("Upload a video file", type=["mp4", "avi", "mov"])
    
    if video_file is not None:
        # Save uploaded video
        video_path = os.path.join("data/videos", f"uploaded_{int(time.time())}.mp4")
        with open(video_path, "wb") as f:
            f.write(video_file.read())
        st.sidebar.success(f"✅ Video uploaded successfully!")
        
        # Show video
        st.subheader("Uploaded Video")
        st.video(video_file)

    # Demo Analytics Section
    st.header("📊 Crowd Analytics Dashboard")
    
    # Create sample analytics data
    dates = pd.date_range(start='2024-01-01', periods=100, freq='H')
    demo_data = pd.DataFrame({
        'timestamp': dates,
        'active': np.random.randint(10, 50, 100),
        'in': np.random.randint(0, 10, 100),
        'out': np.random.randint(0, 10, 100),
        'net': np.random.randint(-5, 5, 100)
    })
    
    # Show metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Active Count", demo_data['active'].iloc[-1], demo_data['active'].iloc[-1] - demo_data['active'].iloc[-2])
    with col2:
        st.metric("In Count", demo_data['in'].iloc[-1], demo_data['in'].iloc[-1] - demo_data['in'].iloc[-2])
    with col3:
        st.metric("Out Count", demo_data['out'].iloc[-1], demo_data['out'].iloc[-1] - demo_data['out'].iloc[-2])
    with col4:
        st.metric("Net Count", demo_data['net'].iloc[-1], demo_data['net'].iloc[-1] - demo_data['net'].iloc[-2])
    
    # Show recent events
    st.subheader("Recent Events")
    recent_events = demo_data.tail(10).copy()
    recent_events['event'] = recent_events['net'].apply(lambda x: f"{'Entry' if x > 0 else 'Exit'} ({abs(x)} people)")
    st.dataframe(recent_events[['timestamp', 'active', 'in', 'out', 'net', 'event']])
    
    # Show charts
    st.subheader("Analytics Over Time")
    chart_cols = st.columns(4)
    with chart_cols[0]:
        st.line_chart(demo_data["active"])
        st.caption("Active Count")
    with chart_cols[1]:
        st.line_chart(demo_data["in"])
        st.caption("In Count")
    with chart_cols[2]:
        st.line_chart(demo_data["out"])
        st.caption("Out Count")
    with chart_cols[3]:
        st.line_chart(demo_data["net"])
        st.caption("Net Count")
    
    # Features explanation
    st.header("🚀 Features")
    st.markdown("""
    **CrowdFlow AI** provides intelligent crowd analytics:
    
    - **🎥 Video Processing**: Upload and analyze crowd videos
    - **👥 Person Detection**: YOLO-based object detection
    - **📊 Real-time Analytics**: Live crowd counting and tracking
    - **📈 Trend Analysis**: Historical data visualization
    - **🎯 ROI Detection**: Define regions of interest
    - **🔄 Object Tracking**: Persistent ID tracking across frames
    
    **For full functionality:**
    - Run locally with `streamlit run src/dashboard/app.py`
    - Install all dependencies: `pip install -r requirements.txt`
    - Requires OpenCV for video processing
    """)
    
    # Configuration section
    st.sidebar.header("Configuration")
    if st.sidebar.button("Show Config"):
        config = {
            "model": {
                "weights": "yolov8n.pt",
                "confidence": 0.5,
                "classes": [0]  # person detection
            },
            "tracking": {
                "algorithm": "ocsort",
                "max_disappeared": 30
            },
            "counting": {
                "line_y": 300,
                "direction": "both"
            }
        }
        st.json(config)

if __name__ == "__main__":
    main() 
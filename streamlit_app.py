#!/usr/bin/env python3
"""
CrowdFlow AI - Streamlit Cloud Deployment
Main entry point for Streamlit Cloud deployment
"""

import streamlit as st
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Try to import OpenCV, but handle gracefully if it fails
try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError as e:
    OPENCV_AVAILABLE = False
    st.warning(f"OpenCV not available: {e}. Some features will be limited.")

# Import the dashboard app
try:
    from dashboard.app import main
    main()
except Exception as e:
    st.error(f"Error loading dashboard: {e}")
    st.info("Please check the deployment logs for more details.") 
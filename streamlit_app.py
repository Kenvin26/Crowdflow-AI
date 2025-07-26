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

# Import the dashboard app
from dashboard.app import main

if __name__ == "__main__":
    main() 
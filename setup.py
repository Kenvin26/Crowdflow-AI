#!/usr/bin/env python3
"""
CrowdFlow AI Setup Script
Automates the installation and configuration of CrowdFlow AI
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 10):
        print("❌ Python 3.10 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def create_directories():
    """Create necessary directories"""
    directories = [
        "data/videos",
        "data/outputs", 
        "data/logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def download_yolo_model():
    """Download YOLO model if not present"""
    model_path = "yolov8n.pt"
    if not os.path.exists(model_path):
        print("🔄 Downloading YOLO model...")
        try:
            import torch
            from ultralytics import YOLO
            model = YOLO('yolov8n.pt')
            print("✅ YOLO model downloaded successfully")
        except Exception as e:
            print(f"⚠️  Could not download YOLO model: {e}")
            print("   You can download it manually from: https://github.com/ultralytics/ultralytics")
    else:
        print("✅ YOLO model already exists")

def main():
    """Main setup function"""
    print("🚀 CrowdFlow AI Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not os.path.exists("venv"):
        if not run_command("python -m venv venv", "Creating virtual environment"):
            sys.exit(1)
    else:
        print("✅ Virtual environment already exists")
    
    # Activate virtual environment and install dependencies
    if os.name == 'nt':  # Windows
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Unix/Linux/Mac
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
    
    # Install dependencies
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Installing dependencies"):
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Download YOLO model
    download_yolo_model()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Activate virtual environment:")
    if os.name == 'nt':
        print("   .\\venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("2. Start the API server:")
    print("   uvicorn src.api.server:app --host 0.0.0.0 --port 8000")
    print("3. Start the dashboard:")
    print("   streamlit run src/dashboard/app.py")
    print("4. Open http://localhost:8501 in your browser")
    
    print("\n📚 For more information, see README.md")

if __name__ == "__main__":
    main() 
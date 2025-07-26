# CrowdFlow AI - Intelligent Crowd Analytics Platform

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.47.0-red.svg)](https://streamlit.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.11.0-orange.svg)](https://opencv.org/)
[![YOLO](https://img.shields.io/badge/YOLO-v8-00ff00.svg)](https://github.com/ultralytics/ultralytics)

## 🎯 Overview

CrowdFlow AI is an intelligent crowd analytics platform that provides real-time video analysis for crowd monitoring, counting, and behavior analysis. The system combines computer vision, machine learning, and web technologies to deliver comprehensive crowd insights through an intuitive dashboard interface.

## ✨ Features

### 🎥 Video Processing
- **Multi-format Support**: Upload MP4, AVI, MOV videos or record directly from webcam
- **Real-time Processing**: Live video stream analysis with instant overlays
- **ROI Detection**: Define regions of interest for targeted analysis
- **Object Tracking**: Advanced OCSort algorithm for persistent object tracking

### 📊 Analytics Dashboard
- **Interactive Web Interface**: Streamlit-based dashboard with real-time updates
- **Metrics Visualization**: Time series charts for crowd counts and trends
- **Event Logging**: Comprehensive tracking of entry/exit events
- **Video Overlays**: Display processed videos with bounding boxes, IDs, and heatmaps

### 🤖 AI-Powered Detection
- **YOLO v8 Integration**: State-of-the-art object detection
- **Person Detection**: Specialized model for human detection
- **Multi-class Support**: Extensible for various object types
- **Confidence Scoring**: Reliable detection with confidence thresholds

### 📈 Data Management
- **CSV Export**: Metrics saved to structured CSV format
- **REST API**: FastAPI backend for data access
- **Real-time Updates**: Live dashboard refresh with latest metrics
- **Historical Analysis**: Time-based trend analysis

## 🏗️ Architecture

```
CrowdFlow AI/
├── src/
│   ├── main.py                 # Core analytics pipeline
│   ├── dashboard/
│   │   └── app.py             # Streamlit web interface
│   ├── api/
│   │   └── server.py          # FastAPI REST server
│   ├── detectors/
│   │   └── yolo_detector.py   # YOLO object detection
│   ├── tracking/
│   │   ├── centroid_tracker.py
│   │   └── ocsort_tracker.py  # Advanced tracking algorithm
│   ├── counting/
│   │   └── counter.py         # Crowd counting logic
│   ├── analytics/             # Various analytics modules
│   └── utils/                 # Utility functions
├── data/
│   ├── videos/               # Input video storage
│   ├── outputs/              # Processed results
│   └── logs/                 # System logs
├── requirements.txt          # Python dependencies
└── config.yaml              # Configuration file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Git
- Webcam (for recording feature)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Kenvin26/Crowdflow-AI.git
   cd Crowdflow-AI
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   ```bash
   # Windows
   .\venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Download YOLO model** (if not included)
   ```bash
   # The yolov8n.pt file should be in the root directory
   # If missing, it will be downloaded automatically on first run
   ```

### Running the Application

1. **Start the API server**
   ```bash
   uvicorn src.api.server:app --host 0.0.0.0 --port 8000
   ```

2. **Start the dashboard** (in a new terminal)
   ```bash
   streamlit run src/dashboard/app.py
   ```

3. **Access the application**
   - Dashboard: http://localhost:8501
   - API: http://localhost:8000

## 📖 Usage Guide

### 1. Video Upload/Recording
- **Upload Video**: Use the file uploader in the sidebar
- **Record Video**: Click "Record from webcam" to capture live video
- **Select Existing**: Choose from previously uploaded videos

### 2. ROI Configuration
- Define regions of interest for targeted analysis
- Configure entry/exit zones for accurate counting
- Adjust detection parameters as needed

### 3. Analytics Dashboard
- **Real-time Metrics**: View live crowd counts and trends
- **Historical Data**: Analyze patterns over time
- **Video Overlays**: Watch processed videos with detection overlays
- **Event Log**: Review detailed entry/exit events

### 4. API Endpoints
- `GET /metrics/latest`: Get latest analytics metrics
- `GET /metrics/history`: Retrieve historical data
- `POST /process-video`: Trigger video processing

## 🔧 Configuration

Edit `src/config.yaml` to customize:
- Video source paths
- Detection thresholds
- ROI coordinates
- Model parameters
- Output settings

## 📊 Output Files

The system generates several output files:
- `data/outputs/metrics.csv`: Crowd analytics data
- `data/outputs/overlayed_video.mp4`: Processed video with overlays
- `data/outputs/live_frame.jpg`: Latest processed frame
- `data/outputs/tracks.csv`: Object tracking data

## 🛠️ Development

### Project Structure
- **Modular Design**: Each component is self-contained
- **Extensible Architecture**: Easy to add new analytics modules
- **Clean Code**: Well-documented and maintainable codebase

### Adding New Features
1. Create new modules in appropriate directories
2. Update configuration files as needed
3. Add dependencies to requirements.txt
4. Update documentation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ultralytics YOLO](https://github.com/ultralytics/ultralytics) for object detection
- [Streamlit](https://streamlit.io/) for the web interface
- [FastAPI](https://fastapi.tiangolo.com/) for the REST API
- [OpenCV](https://opencv.org/) for computer vision operations

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the code comments

## 🔄 Version History

- **v1.0.0**: Initial release with core functionality
- Basic crowd detection and counting
- Streamlit dashboard
- FastAPI backend
- Video processing pipeline

---

**Made with ❤️ for intelligent crowd analytics** 
from ultralytics import YOLO

def export_yolo_to_onnx(weights_path, onnx_path="yolov8.onnx"):
    model = YOLO(weights_path)
    model.export(format="onnx", dynamic=True, simplify=True, imgsz=640, half=False, optimize=True, output=onnx_path)
    print(f"Exported YOLO model to {onnx_path}")

# Example usage:
# export_yolo_to_onnx("yolov8n.pt", "yolov8n.onnx") 
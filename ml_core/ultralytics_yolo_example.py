"""
Example: YOLOv8 inference with Ultralytics
"""
from ultralytics import YOLO
import cv2
import sys

def run_yolo_inference(image_path, model_path="yolov8n.pt"):
    # Load YOLOv8 model (default: yolov8n.pt)
    model = YOLO(model_path)
    # Run inference on the image
    results = model(image_path)
    # Print results
    print("Detections:")
    for box in results[0].boxes:
        print(f"Class: {box.cls}, Confidence: {box.conf}, BBox: {box.xyxy}")
    # Optionally, show the image with detections
    img = results[0].plot()
    cv2.imshow("YOLOv8 Detections", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ultralytics_yolo_example.py <image_path> [<model_path>]")
        sys.exit(1)
    image_path = sys.argv[1]
    model_path = sys.argv[2] if len(sys.argv) > 2 else "yolov8n.pt"
    run_yolo_inference(image_path, model_path)
from ultralytics import YOLO


def get_yolo_v8_model():
    model = YOLO("yolov8x.pt")
    return model

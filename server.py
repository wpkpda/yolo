import rpc
import yolov8

model = yolov8.get_yolo_v8_model()
rpc.serve(model)

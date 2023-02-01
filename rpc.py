import io
from concurrent import futures

import grpc
from PIL import Image

import pb.yolo_pb2_grpc
import pb.yolo_pb2


class YOLOServer(pb.yolo_pb2_grpc.YOLO_RPCServicer):
    def __init__(self, model):
        self.model = model
        self.names = [model.names[i] for i in model.names]

    def Detect(self, request, context):
        img = io.BytesIO(request.image.data)
        img = Image.open(img)

        results = self.model(img)
        if len(results) == 0:
            return pb.yolo_pb2.Detection(boxes=[])
        result = results[0]
        xyxy = result.boxes.xyxy
        cls = result.boxes.cls

        boxes = []
        for i in range(0, len(xyxy), 1):
            box = pb.yolo_pb2.Box(
                x1=xyxy[i][0].item(),
                y1=xyxy[i][1].item(),
                x2=xyxy[i][2].item(),
                y2=xyxy[i][3].item(),
                label=self.names[int(cls[i].item())],
            )
            boxes.append(box)

        detection = pb.yolo_pb2.Detection(boxes=boxes)
        return detection

    def GetClassnames(self, request, context):
        return pb.yolo_pb2.Classnames(names=self.names)


def serve(model):
    rpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb.yolo_pb2_grpc.add_YOLO_RPCServicer_to_server(YOLOServer(model), rpc_server)
    rpc_server.add_insecure_port('[::]:50051')
    rpc_server.start()
    print("Server started on port 50051")
    rpc_server.wait_for_termination()

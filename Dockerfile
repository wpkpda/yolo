FROM ultralytics/ultralytics:latest-cpu

ADD yolov8.py /app/yolov8.py
ADD rpc.py /app/rpc.py
ADD server.py /app/server.py
ADD download.py /app/download.py
ADD pb /app/pb

WORKDIR /app

ENTRYPOINT ["python3", "server.py"]

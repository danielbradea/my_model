from ultralytics import YOLO

model = YOLO("yolov8s.yaml")
model.train(data="./dataset/data.yaml", epochs=100, imgsz=600)





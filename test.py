from ultralytics import YOLO

# Load the trained model
model = YOLO("./runs/detect/train5/weights/best.pt")

# Run inference on an image
results = model("3.jpg")

# Show results
for result in results:
    result.show()  # Show image with detections
    result.save(filename="output.jpg") 
from ultralytics import YOLO

DATASET = "data/neu_det_raw/data.yaml"

model = YOLO("yolo11n.pt")

results = model.train(
    data=DATASET,
    epochs=50,
    imgsz=640,
    batch=16,
    device=0,
    workers=4,
    project="runs/defect_detection",
    name="yolo11n_baseline",
    pretrained=True,
    patience=10,
    save=True,
    plots=True,
)

print("\nTraining completed.")
print("Best model: runs/defect_detection/yolo11n_baseline/weights/best.pt")
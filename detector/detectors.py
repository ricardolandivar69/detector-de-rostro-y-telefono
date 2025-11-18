import cv2
import numpy as np
from .state import GLOBAL_STATE


class BaseDetector:
    name = 'base'
    def process(self, frame):
        return frame


class FaceDetector(BaseDetector):
    name = 'face'

    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )

    def process(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.2, 5)
        labels = []
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            labels.append('face')
        if labels:
            GLOBAL_STATE.update_counts(labels)
        cv2.putText(
            frame,
            f"Faces: {len(faces)}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 255, 0),
            2,
        )
        return frame


# --- YOLO opcional ---
try:
    from ultralytics import YOLO
    _YOLO_AVAILABLE = True
except Exception:
    _YOLO_AVAILABLE = False


class YOLODetector(BaseDetector):
    name = 'yolo'

    def __init__(self, classes_filter=None, conf=0.5):
        if not _YOLO_AVAILABLE:
            raise RuntimeError(
                'Ultralytics no disponible. Instala "ultralytics" o usa FaceDetector.'
            )
        self.model = YOLO('yolov8n.pt')
        self.conf = float(conf)
        self.classes_filter = None
        if classes_filter:
            cf = [c.strip().lower() for c in classes_filter.split(',') if c.strip()]
            self.classes_filter = set(cf)

    def process(self, frame):
        results = self.model.predict(source=frame, conf=self.conf, verbose=False)
        labels = []
        annotated = frame.copy()
        for r in results:
            boxes = r.boxes
            names = r.names
            for b in boxes:
                cls_id = int(b.cls)
                cls_name = names.get(cls_id, str(cls_id)).lower()
                if self.classes_filter and cls_name not in self.classes_filter:
                    continue
                x1, y1, x2, y2 = map(int, b.xyxy[0].tolist())
                conf = float(b.conf)
                cv2.rectangle(annotated, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(
                    annotated,
                    f"{cls_name} {conf:.2f}",
                    (x1, max(y1 - 10, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 0, 0),
                    2,
                )
                labels.append(cls_name)
        if labels:
            GLOBAL_STATE.update_counts(labels)
        cv2.putText(
            annotated,
            f"Detections: {len(labels)}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (255, 0, 0),
            2,
        )
        return annotated


def get_detector(name: str, classes: str = None, conf: float = 0.5):
    detector_name = (name or '').lower()
    GLOBAL_STATE.set_detector(detector_name or 'face')
    if detector_name == 'yolo':
        return YOLODetector(classes_filter=classes, conf=conf)
    return FaceDetector()

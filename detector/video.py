# detector/video.py (versión tolerante a import)
import threading
import time

try:
    import cv2
except Exception as e:
    cv2 = None
    _CV2_IMPORT_ERR = e
else:
    _CV2_IMPORT_ERR = None

VIDEO_SOURCE = 0

class VideoCamera:
    def __init__(self):
        if cv2 is None:
            raise RuntimeError(f'OpenCV (cv2) no disponible: {_CV2_IMPORT_ERR}')
        self.cap = cv2.VideoCapture(VIDEO_SOURCE)
        if not self.cap.isOpened():
            raise RuntimeError('No se pudo abrir la fuente de video')
        self.lock = threading.Lock()

    def read(self):
        with self.lock:
            ok, frame = self.cap.read()
        if not ok:
            return None
        return frame

    def __del__(self):
        try:
            if hasattr(self, 'cap') and self.cap:
                self.cap.release()
        except Exception:
            pass

camera_singleton = None

def get_camera():
    global camera_singleton
    if camera_singleton is None:
        camera_singleton = VideoCamera()
    return camera_singleton

def mjpeg_generator(process_frame_fn):
    if cv2 is None:
        raise RuntimeError(f'OpenCV (cv2) no disponible: {_CV2_IMPORT_ERR}')
    while True:
        frame = get_camera().read()
        if frame is None:
            time.sleep(0.03)
            continue
        frame = process_frame_fn(frame)
        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

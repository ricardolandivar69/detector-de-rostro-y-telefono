# detector/views.py
from django.http import StreamingHttpResponse, JsonResponse
from django.shortcuts import render
from .video import mjpeg_generator
from .detectors import get_detector, FaceDetector
from .state import GLOBAL_STATE

def index(request):
    return render(request, 'detector/index.html')

def video_feed(request):
    det = request.GET.get('detector', 'face')
    classes = request.GET.get('classes')
    conf = float(request.GET.get('conf', 0.5))

    try:
        detector = get_detector(det, classes, conf)
    except RuntimeError as e:
        # Fallback automático si YOLO no está instalado
        detector = FaceDetector()

    def process(frame):
        return detector.process(frame)

    return StreamingHttpResponse(
        mjpeg_generator(process),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )

def stats(request):
    return JsonResponse(GLOBAL_STATE.snapshot())

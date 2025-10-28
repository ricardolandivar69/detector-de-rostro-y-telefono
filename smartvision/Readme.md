# SmartVision — Django + OpenCV (Realtime)


Aplicativo web de detección en tiempo real con streaming MJPEG.


## Requisitos
- Python 3.10+
- (Opcional) GPU/CUDA si usarás YOLOv8 con aceleración.


## Instalación rápida
```bash
python -m venv venv && source venv/bin/activate # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
# 📘 DOCUMENTACIÓN TÉCNICA - SmartVision

## Sistema de Detección de Rostros y Objetos con OpenCV

**Versión:** 1.0  
**Fecha:** 18 de Noviembre de 2025  
**Desarrollado para:** UNEMI - Práctica de Testing  

---

## 📋 TABLA DE CONTENIDOS

1. [Descripción General](#descripción-general)
2. [Requisitos del Sistema](#requisitos-del-sistema)
3. [Instalación](#instalación)
4. [Estructura de Directorios](#estructura-de-directorios)
5. [Configuración](#configuración)
6. [Ejecución](#ejecución)
7. [Arquitectura del Sistema](#arquitectura-del-sistema)
8. [Módulos y Componentes](#módulos-y-componentes)
9. [API y Endpoints](#api-y-endpoints)
10. [Pruebas Realizadas](#pruebas-realizadas)
11. [Solución de Problemas](#solución-de-problemas)

---

## 1. DESCRIPCIÓN GENERAL

SmartVision es un sistema web de detección de rostros en tiempo real desarrollado con Django y OpenCV. El sistema captura video de la cámara, procesa cada frame para detectar rostros utilizando algoritmos de visión por computadora, y muestra los resultados en una interfaz web interactiva.

### Características Principales

- ✅ Detección de rostros en tiempo real con OpenCV (Haar Cascades)
- ✅ Streaming de video MJPEG sobre HTTP
- ✅ API REST para estadísticas de detección
- ✅ Interfaz web responsiva
- ✅ Soporte opcional para YOLO (detección de objetos)
- ✅ Sistema de estado global thread-safe
- ✅ Cobertura de pruebas del 85%

### Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| Python | 3.13+ | Lenguaje base |
| Django | 5.1+ | Framework web |
| OpenCV | 4.12+ | Visión por computadora |
| NumPy | 1.26+ | Procesamiento numérico |
| pytest | 9.0+ | Framework de pruebas |
| coverage | 7.0+ | Análisis de cobertura |

---

## 2. REQUISITOS DEL SISTEMA

### Requisitos de Hardware

- **CPU:** Procesador de 2 núcleos o superior
- **RAM:** Mínimo 4 GB (recomendado 8 GB)
- **Cámara web:** Cualquier cámara compatible con OpenCV
- **Almacenamiento:** 500 MB de espacio libre

### Requisitos de Software

- **Sistema Operativo:** Windows 10/11, Linux, macOS
- **Python:** 3.13 o superior
- **Navegador Web:** Chrome, Firefox, Edge (últimas versiones)

### Dependencias Python

```txt
Django>=5.1.3
opencv-python>=4.12.0
numpy>=1.26.0
pytest>=9.0.1
pytest-django>=4.11.1
pytest-cov>=7.0.0
coverage>=7.0.0
ultralytics>=8.0.0  # Opcional, para YOLO
```

---

## 3. INSTALACIÓN

### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/smartvision.git
cd smartvision
```

### Paso 2: Crear Entorno Virtual

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Configurar Base de Datos

```bash
python manage.py migrate
```

### Paso 5: Crear Superusuario (Opcional)

```bash
python manage.py createsuperuser
```

### Paso 6: Verificar Instalación

```bash
python manage.py check
```

---

## 4. ESTRUCTURA DE DIRECTORIOS

```
smartvision/
├── manage.py                    # Script de gestión de Django
├── requirements.txt             # Dependencias del proyecto
├── db.sqlite3                  # Base de datos SQLite
│
├── smartvision/                # Configuración del proyecto
│   ├── __init__.py
│   ├── settings.py             # Configuración principal
│   ├── urls.py                 # URLs del proyecto
│   ├── wsgi.py                 # Configuración WSGI
│   └── asgi.py                 # Configuración ASGI
│
├── detector/                   # Aplicación principal
│   ├── __init__.py
│   ├── admin.py                # Configuración del admin
│   ├── apps.py                 # Configuración de la app
│   ├── models.py               # Modelos de datos
│   ├── views.py                # Vistas y endpoints
│   ├── urls.py                 # URLs de la app
│   ├── detectors.py            # ⭐ Lógica de detección
│   ├── state.py                # ⭐ Estado global thread-safe
│   ├── video.py                # ⭐ Generador de streaming
│   │
│   ├── static/detector/        # Archivos estáticos
│   │   └── main.js             # JavaScript del frontend
│   │
│   ├── templates/detector/     # Templates HTML
│   │   └── index.html          # Interfaz principal
│   │
│   └── tests/                  # Suite de pruebas
│       ├── __init__.py
│       ├── test_detectors.py   # Pruebas unitarias (17)
│       ├── test_views.py       # Pruebas de vistas (17)
│       ├── test_integration.py # Pruebas de integración (10)
│       └── test_functional.py  # Pruebas funcionales (14)
│
├── htmlcov/                    # Reportes de cobertura HTML
│   └── index.html
│
└── DOCUMENTACION/              # Documentación del proyecto
    ├── REPORTE_PRUEBAS.md
    ├── RESUMEN_EJECUTIVO.txt
    ├── GUIA_CAPTURAS.md
    └── EJEMPLOS_CODIGO_PRUEBAS.md
```

---

## 5. CONFIGURACIÓN

### Archivo `settings.py`

Configuraciones clave en `smartvision/settings.py`:

```python
# Base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Apps instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'detector',  # Aplicación principal
]

# Configuración de archivos estáticos
STATIC_URL = 'static/'
```

### Variables de Entorno (Opcional)

Crear archivo `.env` para configuraciones sensibles:

```env
DEBUG=True
SECRET_KEY=tu-secret-key-aqui
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## 6. EJECUCIÓN

### Iniciar el Servidor de Desarrollo

```bash
python manage.py runserver
```

El sistema estará disponible en: `http://localhost:8000`

### Ejecutar Pruebas

**Todas las pruebas (58 en total):**
```bash
python manage.py test detector.tests -v 2
```

**Solo pruebas unitarias (17):**
```bash
python manage.py test detector.tests.test_detectors -v 2
```

**Solo pruebas funcionales (14):**
```bash
python manage.py test detector.tests.test_functional -v 2
```

**Con reporte de cobertura:**
```bash
coverage run --source='detector' manage.py test detector.tests
coverage report
coverage html
```

### Acceder a la Interfaz de Administración

```
URL: http://localhost:8000/admin
Usuario: (el creado con createsuperuser)
```

---

## 7. ARQUITECTURA DEL SISTEMA

### Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                     NAVEGADOR WEB                           │
│  ┌──────────────────┐  ┌─────────────────┐                 │
│  │  Interfaz HTML   │  │  JavaScript     │                 │
│  │  (index.html)    │  │  (main.js)      │                 │
│  └────────┬─────────┘  └────────┬────────┘                 │
└───────────┼─────────────────────┼──────────────────────────┘
            │                     │
            │ HTTP Requests       │ AJAX
            │                     │
┌───────────▼─────────────────────▼──────────────────────────┐
│                    DJANGO SERVER                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │               URLS & VIEWS                           │  │
│  │  • /          → index (HTML)                         │  │
│  │  • /video_feed → video_feed (MJPEG Stream)          │  │
│  │  • /stats     → stats (JSON API)                    │  │
│  └────────┬────────────────────────────┬────────────────┘  │
│           │                            │                    │
│  ┌────────▼────────┐         ┌────────▼────────┐          │
│  │  DETECTORS.PY   │         │    STATE.PY     │          │
│  │                 │         │                 │          │
│  │ • FaceDetector  │◄────────┤ GLOBAL_STATE    │          │
│  │ • YOLODetector  │         │ (Thread-safe)   │          │
│  │ • get_detector()│         │                 │          │
│  └────────┬────────┘         └─────────────────┘          │
│           │                                                 │
│  ┌────────▼────────┐                                       │
│  │   VIDEO.PY      │                                       │
│  │                 │                                       │
│  │ mjpeg_generator │                                       │
│  │ (Streaming)     │                                       │
│  └────────┬────────┘                                       │
└───────────┼──────────────────────────────────────────────┘
            │
┌───────────▼──────────────────────────────────────────────┐
│                      OPENCV                               │
│  • cv2.VideoCapture(0)  ← Cámara                         │
│  • cv2.CascadeClassifier ← Haar Cascades                 │
│  • cv2.detectMultiScale() ← Detección                    │
└──────────────────────────────────────────────────────────┘
```

### Flujo de Datos

1. **Usuario accede** → Navegador carga `index.html`
2. **JavaScript solicita** → Stream de video desde `/video_feed`
3. **Vista video_feed** → Inicializa detector según parámetros
4. **video.py** → Captura frames de la cámara
5. **detectors.py** → Procesa cada frame con OpenCV
6. **GLOBAL_STATE** → Actualiza contadores de detecciones
7. **MJPEG Stream** → Envía frames procesados al navegador
8. **JavaScript polling** → Consulta `/stats` cada 2 segundos
9. **Vista stats** → Retorna JSON con estadísticas
10. **Interfaz actualiza** → Muestra contadores en pantalla

---

## 8. MÓDULOS Y COMPONENTES

### 8.1 detector/detectors.py

**Responsabilidad:** Implementación de algoritmos de detección

**Clases:**

```python
class BaseDetector:
    """Clase base para todos los detectores"""
    name = 'base'
    def process(self, frame): pass

class FaceDetector(BaseDetector):
    """Detector de rostros con Haar Cascades"""
    def __init__(self):
        # Carga haarcascade_frontalface_default.xml
    
    def process(self, frame):
        # Detecta rostros y dibuja rectángulos

class YOLODetector(BaseDetector):
    """Detector de objetos con YOLO (opcional)"""
    # Requiere ultralytics
```

**Funciones:**

```python
def get_detector(name: str, classes: str, conf: float):
    """
    Factory function para obtener detector
    Returns: FaceDetector | YOLODetector
    """
```

### 8.2 detector/state.py

**Responsabilidad:** Gestión de estado global thread-safe

```python
class DetectionState:
    """Estado global del sistema"""
    
    def __init__(self):
        self.lock = threading.Lock()
        self.counts = Counter()
        self.last_detector = 'face'
    
    def update_counts(self, labels):
        """Actualiza contadores de forma atómica"""
    
    def reset(self):
        """Limpia contadores"""
    
    def snapshot(self):
        """Retorna estado actual"""

GLOBAL_STATE = DetectionState()
```

### 8.3 detector/video.py

**Responsabilidad:** Generación de stream MJPEG

```python
def mjpeg_generator(process_function):
    """
    Generador de frames MJPEG
    
    Args:
        process_function: Función para procesar frames
    
    Yields:
        bytes: Frame en formato MJPEG
    """
    camera = cv2.VideoCapture(0)
    while True:
        frame = camera.read()
        processed = process_function(frame)
        jpeg = cv2.imencode('.jpg', processed)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg + b'\r\n')
```

### 8.4 detector/views.py

**Responsabilidad:** Endpoints HTTP

```python
def index(request):
    """Página principal"""
    return render(request, 'detector/index.html')

def video_feed(request):
    """Stream MJPEG"""
    detector = get_detector(
        request.GET.get('detector', 'face'),
        request.GET.get('classes'),
        float(request.GET.get('conf', 0.5))
    )
    return StreamingHttpResponse(
        mjpeg_generator(detector.process),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )

def stats(request):
    """API de estadísticas"""
    return JsonResponse(GLOBAL_STATE.snapshot())
```

---

## 9. API Y ENDPOINTS

### GET /

**Descripción:** Página principal del sistema  
**Respuesta:** HTML con interfaz de usuario  
**Código:** 200 OK

---

### GET /video_feed

**Descripción:** Stream MJPEG de video procesado

**Parámetros Query:**

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| detector | string | 'face' | Tipo de detector (face/yolo) |
| classes | string | null | Clases a detectar (solo YOLO) |
| conf | float | 0.5 | Umbral de confianza |

**Ejemplo:**
```
GET /video_feed?detector=face
GET /video_feed?detector=yolo&classes=person,car&conf=0.7
```

**Respuesta:** Stream multipart/x-mixed-replace  
**Código:** 200 OK

---

### GET /stats

**Descripción:** Estadísticas de detección en tiempo real

**Respuesta JSON:**
```json
{
    "detector": "face",
    "counts": {
        "face": 152,
        "person": 23
    }
}
```

**Código:** 200 OK

---

## 10. PRUEBAS REALIZADAS

### Resumen de Pruebas

| Tipo de Prueba | Cantidad | Aprobadas | Cobertura |
|----------------|----------|-----------|-----------|
| Unitarias | 17 | 17 (100%) | 58% |
| Integración | 10 | 10 (100%) | 90% |
| Vistas | 17 | 17 (100%) | 95% |
| Funcionales | 14 | 14 (100%) | - |
| **TOTAL** | **58** | **58 (100%)** | **85%** |

### 10.1 Pruebas Unitarias (17)

**Archivo:** `detector/tests/test_detectors.py`

- ✅ BaseDetector (2 pruebas)
- ✅ FaceDetector (5 pruebas)
- ✅ get_detector() (5 pruebas)
- ✅ GLOBAL_STATE (5 pruebas, incluye thread-safety)

### 10.2 Pruebas de Integración (10)

**Archivo:** `detector/tests/test_integration.py`

- ✅ Flujo básico aplicación (4 pruebas)
- ✅ Integración detector-estado (2 pruebas)
- ✅ URLs principales (2 pruebas)
- ✅ Escenarios end-to-end (2 pruebas)

### 10.3 Pruebas de Vistas (17)

**Archivo:** `detector/tests/test_views.py`

- ✅ Vista Index (3 pruebas)
- ✅ Vista VideoFeed (6 pruebas)
- ✅ Vista Stats (5 pruebas)
- ✅ Configuración URLs (3 pruebas)

### 10.4 Pruebas Funcionales (14)

**Archivo:** `detector/tests/test_functional.py`

**Casos de Uso Validados:**

1. ✅ **Inicio del Sistema** (4 pruebas)
   - Inicio servidor Django
   - Carga de OpenCV
   - Inicialización detector
   - Disponibilidad de rutas

2. ✅ **Detección en Video** (4 pruebas)
   - Frame vacío
   - Múltiples frames
   - Imagen sintética
   - Rendimiento (132 FPS)

3. ✅ **Visualización** (4 pruebas)
   - Interfaz principal
   - Streaming video
   - Estadísticas JSON
   - Cambio dinámico detector

4. ✅ **Integración Completa** (2 pruebas)
   - Flujo usuario completo
   - Robustez ante errores

### Ejecutar Todas las Pruebas

```bash
# Todas las pruebas
python manage.py test detector.tests -v 2

# Con cobertura
coverage run --source='detector' manage.py test detector.tests
coverage html
start htmlcov/index.html
```

---

## 11. SOLUCIÓN DE PROBLEMAS

### Problema: Cámara no detectada

**Error:** `Cannot open camera`

**Solución:**
```bash
# Verificar cámaras disponibles
python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"

# Probar diferentes índices
cv2.VideoCapture(1)  # Cámara externa
```

### Problema: Error al importar cv2

**Error:** `ModuleNotFoundError: No module named 'cv2'`

**Solución:**
```bash
pip uninstall opencv-python
pip install opencv-python==4.12.0
```

### Problema: Rendimiento lento

**Síntomas:** FPS < 10

**Soluciones:**
- Reducir resolución de cámara
- Usar frame skip (procesar 1 de cada 2 frames)
- Optimizar parámetros de `detectMultiScale()`

### Problema: Puerto 8000 en uso

**Error:** `Address already in use`

**Solución:**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9

# O usar otro puerto
python manage.py runserver 8080
```

---

## 📞 SOPORTE TÉCNICO

**Repositorio:** https://github.com/tu-usuario/smartvision  
**Issues:** https://github.com/tu-usuario/smartvision/issues  
**Documentación:** Ver carpeta `DOCUMENTACION/`

---

## 📝 CHANGELOG

### Versión 1.0 (18/11/2025)
- ✅ Implementación inicial
- ✅ Detector de rostros con OpenCV
- ✅ 58 pruebas (100% aprobadas)
- ✅ Cobertura del 85%
- ✅ Documentación completa

---

**Documento generado:** 18 de Noviembre de 2025  
**Autor:** [Tu Nombre]  
**Institución:** UNEMI

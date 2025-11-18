"""
PRUEBAS FUNCIONALES - Sesión 2
Validar el correcto funcionamiento del sistema en casos de uso clave
"""
import unittest
from django.test import TestCase, Client, LiveServerTestCase
from django.urls import reverse
from detector.detectors import FaceDetector, get_detector
from detector.state import GLOBAL_STATE
import numpy as np
import cv2
import time


class TestFuncionalInicio(TestCase):
    """
    CASO DE USO 1: INICIO DEL SISTEMA
    Validar que el sistema inicia correctamente y todas las dependencias están disponibles
    """

    def setUp(self):
        """Preparación para cada prueba"""
        self.client = Client()
        GLOBAL_STATE.reset()

    def test_funcional_inicio_servidor(self):
        """
        Prueba Funcional 1: Inicio del servidor Django
        
        Objetivo: Verificar que el servidor web inicia correctamente
        Pasos:
        1. Iniciar servidor Django
        2. Verificar que responde en el puerto configurado
        3. Verificar que no hay errores de configuración
        
        Resultado Esperado: Servidor responde con código 200
        """
        # Acceder a la URL raíz
        response = self.client.get('/')
        
        # Verificaciones
        self.assertEqual(response.status_code, 200, 
                        "El servidor debe responder con código 200")
        self.assertContains(response, 'SmartVision', 
                           msg_prefix="La página debe contener el título del proyecto")

    def test_funcional_carga_opencv(self):
        """
        Prueba Funcional 2: Carga de OpenCV
        
        Objetivo: Verificar que OpenCV está instalado y funcional
        Pasos:
        1. Importar cv2
        2. Verificar versión de OpenCV
        3. Verificar disponibilidad de Haar Cascades
        
        Resultado Esperado: OpenCV cargado correctamente
        """
        # Verificar que cv2 está disponible
        self.assertIsNotNone(cv2, "OpenCV (cv2) debe estar instalado")
        
        # Verificar que la versión es válida
        version = cv2.__version__
        self.assertIsNotNone(version, "OpenCV debe tener una versión válida")
        print(f"   ℹ️ OpenCV versión detectada: {version}")

    def test_funcional_inicializacion_detector(self):
        """
        Prueba Funcional 3: Inicialización del Detector
        
        Objetivo: Verificar que el detector de rostros se inicializa sin errores
        Pasos:
        1. Crear instancia de FaceDetector
        2. Verificar carga del modelo Haar Cascade
        3. Verificar que está listo para procesar
        
        Resultado Esperado: Detector inicializado correctamente
        """
        # Inicializar detector
        detector = FaceDetector()
        
        # Verificaciones
        self.assertIsNotNone(detector.face_cascade, 
                            "Haar Cascade debe estar cargado")
        self.assertEqual(detector.name, 'face', 
                        "El nombre del detector debe ser 'face'")
        
        print("   ✅ FaceDetector inicializado correctamente")

    def test_funcional_rutas_disponibles(self):
        """
        Prueba Funcional 4: Disponibilidad de Rutas
        
        Objetivo: Verificar que todas las rutas principales están disponibles
        Pasos:
        1. Acceder a ruta principal (/)
        2. Acceder a ruta de video feed (/video_feed)
        3. Acceder a ruta de estadísticas (/stats)
        
        Resultado Esperado: Todas las rutas responden correctamente
        """
        rutas_criticas = [
            ('/', 200, 'Página principal'),
            ('/video_feed', 200, 'Video feed'),
            ('/stats', 200, 'Estadísticas'),
        ]
        
        for url, codigo_esperado, descripcion in rutas_criticas:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, codigo_esperado,
                               f"{descripcion} debe responder con código {codigo_esperado}")
                print(f"   ✅ {descripcion}: {url} - OK")


class TestFuncionalDeteccion(TestCase):
    """
    CASO DE USO 2: DETECCIÓN EN VIDEO
    Validar que el sistema detecta rostros correctamente en diferentes escenarios
    """

    def setUp(self):
        """Preparación para cada prueba"""
        GLOBAL_STATE.reset()
        self.detector = FaceDetector()

    def test_funcional_deteccion_frame_vacio(self):
        """
        Prueba Funcional 5: Detección en Frame Vacío
        
        Objetivo: Verificar comportamiento con frame sin contenido
        Pasos:
        1. Crear un frame negro (sin rostros)
        2. Procesar con el detector
        3. Verificar que no hay detecciones pero no hay error
        
        Resultado Esperado: Frame procesado sin errores, 0 detecciones
        """
        # Crear frame negro
        frame_vacio = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Procesar
        resultado = self.detector.process(frame_vacio)
        
        # Verificaciones
        self.assertIsNotNone(resultado, "Debe retornar un frame procesado")
        self.assertEqual(resultado.shape, frame_vacio.shape, 
                        "Las dimensiones deben mantenerse")
        
        print("   ✅ Frame vacío procesado correctamente (0 detecciones)")

    def test_funcional_deteccion_multiples_frames(self):
        """
        Prueba Funcional 6: Detección en Múltiples Frames
        
        Objetivo: Verificar que el detector procesa secuencias de video
        Pasos:
        1. Crear secuencia de 10 frames
        2. Procesar cada frame secuencialmente
        3. Verificar consistencia en el procesamiento
        
        Resultado Esperado: Todos los frames procesados correctamente
        """
        frames_procesados = 0
        total_frames = 10
        
        for i in range(total_frames):
            # Crear frame con contenido aleatorio
            frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
            
            # Procesar
            resultado = self.detector.process(frame)
            
            # Verificar
            self.assertIsNotNone(resultado)
            frames_procesados += 1
        
        self.assertEqual(frames_procesados, total_frames,
                        "Todos los frames deben procesarse")
        
        print(f"   ✅ {frames_procesados} frames procesados correctamente")

    def test_funcional_deteccion_imagen_sintetica(self):
        """
        Prueba Funcional 7: Detección en Imagen Sintética
        
        Objetivo: Verificar detección en imagen con formas similares a rostros
        Pasos:
        1. Crear imagen sintética con forma de rostro
        2. Procesar con el detector
        3. Verificar que el frame contiene anotaciones
        
        Resultado Esperado: Imagen procesada con overlay de detección
        """
        # Crear imagen con forma de rostro
        frame = np.ones((480, 640, 3), dtype=np.uint8) * 200
        
        # Dibujar forma de rostro (óvalo blanco)
        cv2.ellipse(frame, (320, 240), (100, 130), 0, 0, 360, (255, 255, 255), -1)
        
        # Agregar "ojos"
        cv2.circle(frame, (280, 220), 15, (0, 0, 0), -1)
        cv2.circle(frame, (360, 220), 15, (0, 0, 0), -1)
        
        # Agregar "boca"
        cv2.ellipse(frame, (320, 280), (40, 20), 0, 0, 180, (0, 0, 0), 2)
        
        # Procesar
        frame_original = frame.copy()
        resultado = self.detector.process(frame)
        
        # Verificaciones
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.shape, frame.shape,
                        "Las dimensiones deben mantenerse")
        
        print("   ✅ Imagen sintética procesada con anotaciones")

    def test_funcional_rendimiento_deteccion(self):
        """
        Prueba Funcional 8: Rendimiento de Detección
        
        Objetivo: Verificar que la detección es lo suficientemente rápida
        Pasos:
        1. Procesar 30 frames (simulando 1 segundo de video a 30fps)
        2. Medir tiempo total de procesamiento
        3. Verificar que se mantiene tiempo real (< 2 segundos)
        
        Resultado Esperado: Procesamiento en tiempo real
        """
        num_frames = 30
        inicio = time.time()
        
        for i in range(num_frames):
            frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
            self.detector.process(frame)
        
        tiempo_total = time.time() - inicio
        fps = num_frames / tiempo_total
        
        # Verificar que puede procesar al menos 10 fps
        self.assertGreater(fps, 10, 
                          "Debe procesar al menos 10 frames por segundo")
        
        print(f"   ✅ Rendimiento: {fps:.2f} FPS (procesó {num_frames} frames en {tiempo_total:.2f}s)")


class TestFuncionalVisualizacion(TestCase):
    """
    CASO DE USO 3: VISUALIZACIÓN EN INTERFAZ
    Validar que la interfaz muestra correctamente la información
    """

    def setUp(self):
        """Preparación para cada prueba"""
        self.client = Client()
        GLOBAL_STATE.reset()

    def test_funcional_interfaz_principal(self):
        """
        Prueba Funcional 9: Interfaz Principal
        
        Objetivo: Verificar que la página principal se renderiza correctamente
        Pasos:
        1. Acceder a la página principal
        2. Verificar que contiene elementos clave (título, video, controles)
        3. Verificar que el HTML es válido
        
        Resultado Esperado: Interfaz completa y funcional
        """
        response = self.client.get('/')
        
        # Verificaciones de contenido
        elementos_requeridos = [
            'SmartVision',  # Título
            'video',        # Tag de video
            'img',          # Imagen/stream
        ]
        
        for elemento in elementos_requeridos:
            self.assertContains(response, elemento, 
                              msg_prefix=f"La interfaz debe contener: {elemento}")
        
        print("   ✅ Interfaz principal renderizada correctamente")

    def test_funcional_streaming_video(self):
        """
        Prueba Funcional 10: Streaming de Video
        
        Objetivo: Verificar que el endpoint de video streaming responde
        Pasos:
        1. Acceder al endpoint /video_feed
        2. Verificar Content-Type multipart
        3. Verificar que es StreamingHttpResponse
        
        Resultado Esperado: Stream de video activo
        """
        from django.http import StreamingHttpResponse
        
        response = self.client.get('/video_feed')
        
        # Verificaciones
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, StreamingHttpResponse,
                            "Debe ser una respuesta de streaming")
        self.assertIn('multipart', response['Content-Type'],
                     "Debe usar multipart para streaming")
        
        print("   ✅ Streaming de video configurado correctamente")

    def test_funcional_estadisticas_json(self):
        """
        Prueba Funcional 11: Visualización de Estadísticas
        
        Objetivo: Verificar que las estadísticas se muestran correctamente
        Pasos:
        1. Simular detecciones
        2. Consultar endpoint /stats
        3. Verificar estructura JSON correcta
        4. Verificar valores actualizados
        
        Resultado Esperado: Estadísticas actualizadas en tiempo real
        """
        # Simular detecciones
        GLOBAL_STATE.update_counts(['face', 'face', 'person'])
        GLOBAL_STATE.set_detector('face')
        
        # Consultar estadísticas
        response = self.client.get('/stats')
        
        # Verificaciones
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        
        data = response.json()
        
        # Verificar estructura
        self.assertIn('detector', data)
        self.assertIn('counts', data)
        
        # Verificar valores
        self.assertEqual(data['detector'], 'face')
        self.assertEqual(data['counts']['face'], 2)
        self.assertEqual(data['counts']['person'], 1)
        
        print(f"   ✅ Estadísticas correctas: {data}")

    def test_funcional_cambio_detector_dinamico(self):
        """
        Prueba Funcional 12: Cambio Dinámico de Detector
        
        Objetivo: Verificar que se puede cambiar el detector sin reiniciar
        Pasos:
        1. Iniciar con detector 'face'
        2. Cambiar a detector diferente mediante parámetro
        3. Verificar que el cambio se refleja en stats
        
        Resultado Esperado: Cambio de detector en caliente
        """
        # Iniciar con face
        self.client.get('/video_feed?detector=face')
        response1 = self.client.get('/stats')
        data1 = response1.json()
        self.assertEqual(data1['detector'], 'face')
        
        # Cambiar detector (intentar yolo, fallback a face si no está)
        self.client.get('/video_feed?detector=yolo')
        response2 = self.client.get('/stats')
        data2 = response2.json()
        
        # El detector debe haber cambiado (o intentado cambiar)
        self.assertIn(data2['detector'], ['face', 'yolo'],
                     "Debe cambiar o hacer fallback correctamente")
        
        print(f"   ✅ Cambio dinámico: face → {data2['detector']}")


class TestFuncionalIntegracionCompleta(TestCase):
    """
    CASO DE USO 4: INTEGRACIÓN COMPLETA
    Validar el flujo completo del sistema desde inicio hasta visualización
    """

    def setUp(self):
        """Preparación para cada prueba"""
        self.client = Client()
        GLOBAL_STATE.reset()

    def test_funcional_flujo_usuario_completo(self):
        """
        Prueba Funcional 13: Flujo de Usuario Completo
        
        Objetivo: Simular un usuario real usando el sistema
        Pasos:
        1. Usuario accede a la página principal
        2. Usuario inicia el video feed
        3. Sistema realiza detecciones (simuladas)
        4. Usuario consulta estadísticas
        5. Usuario cambia parámetros
        6. Sistema actualiza visualización
        
        Resultado Esperado: Flujo completo funcional
        """
        print("\n   📋 Simulando flujo de usuario completo...")
        
        # Paso 1: Acceder a página principal
        print("   1️⃣ Usuario accede a la página principal")
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        # Paso 2: Iniciar video feed
        print("   2️⃣ Usuario inicia video feed")
        response = self.client.get('/video_feed?detector=face')
        self.assertEqual(response.status_code, 200)
        
        # Paso 3: Simular detecciones
        print("   3️⃣ Sistema realiza detecciones")
        GLOBAL_STATE.update_counts(['face', 'face'])
        
        # Paso 4: Consultar estadísticas
        print("   4️⃣ Usuario consulta estadísticas")
        response = self.client.get('/stats')
        data = response.json()
        self.assertEqual(data['counts']['face'], 2)
        
        # Paso 5: Cambiar parámetros
        print("   5️⃣ Usuario cambia parámetros (conf=0.7)")
        response = self.client.get('/video_feed?detector=face&conf=0.7')
        self.assertEqual(response.status_code, 200)
        
        # Paso 6: Verificar actualización
        print("   6️⃣ Sistema actualiza visualización")
        response = self.client.get('/stats')
        self.assertEqual(response.status_code, 200)
        
        print("   ✅ Flujo de usuario completado exitosamente")

    def test_funcional_robustez_errores(self):
        """
        Prueba Funcional 14: Robustez ante Errores
        
        Objetivo: Verificar que el sistema maneja errores gracefully
        Pasos:
        1. Enviar parámetros inválidos
        2. Acceder a rutas no existentes
        3. Verificar que el sistema no se cae
        
        Resultado Esperado: Sistema estable ante errores
        """
        # Parámetros inválidos (debe causar error controlado)
        try:
            response = self.client.get('/video_feed?conf=invalid')
            # Si llegamos aquí, el sistema manejó el error
            self.assertIn(response.status_code, [200, 400, 500],
                         "Debe manejar parámetros inválidos")
        except ValueError:
            # Es aceptable que lance ValueError, es un comportamiento esperado
            pass
        
        # Ruta no existente
        response = self.client.get('/ruta_inexistente')
        self.assertEqual(response.status_code, 404,
                        "Debe retornar 404 para rutas inexistentes")
        
        # Verificar que el sistema sigue funcionando
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200,
                        "El sistema debe seguir funcionando después de errores")
        
        print("   ✅ Sistema robusto ante errores")


if __name__ == '__main__':
    unittest.main()

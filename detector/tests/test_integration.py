"""
Pruebas de integración para validar el flujo básico de la aplicación
Estas pruebas verifican la interacción entre múltiples componentes
"""
import unittest
from django.test import TestCase, Client
from django.urls import reverse
from detector.detectors import get_detector, FaceDetector
from detector.state import GLOBAL_STATE
import numpy as np


class TestBasicApplicationFlow(TestCase):
    """Pruebas de integración para el flujo básico de la aplicación"""

    def setUp(self):
        """Configuración antes de cada prueba"""
        self.client = Client()
        GLOBAL_STATE.reset()

    def test_complete_user_flow(self):
        """
        Prueba de integración completa:
        1. Acceder a la página principal
        2. Verificar que video_feed funciona
        3. Verificar que stats funciona
        """
        # Paso 1: Acceder a la página principal
        response_index = self.client.get(reverse('index'))
        self.assertEqual(response_index.status_code, 200)
        
        # Paso 2: Verificar video feed
        response_video = self.client.get(reverse('video_feed'))
        self.assertEqual(response_video.status_code, 200)
        
        # Paso 3: Verificar stats
        response_stats = self.client.get(reverse('stats'))
        self.assertEqual(response_stats.status_code, 200)
        data = response_stats.json()
        self.assertIn('detector', data)
        self.assertIn('counts', data)

    def test_detector_selection_and_stats_integration(self):
        """
        Prueba de integración detector-stats:
        Verificar que al seleccionar un detector, stats refleja el cambio
        """
        # Solicitar video feed con detector face
        self.client.get(reverse('video_feed'), {'detector': 'face'})
        
        # Verificar que stats refleja el detector correcto
        response = self.client.get(reverse('stats'))
        data = response.json()
        self.assertEqual(data['detector'], 'face')

    def test_multiple_detector_switches(self):
        """
        Prueba de integración: múltiples cambios de detector
        """
        # Cambiar a face
        self.client.get(reverse('video_feed'), {'detector': 'face'})
        response1 = self.client.get(reverse('stats'))
        self.assertEqual(response1.json()['detector'], 'face')
        
        # Intentar cambiar a yolo (debería fallback a face si no está disponible)
        self.client.get(reverse('video_feed'), {'detector': 'yolo'})
        response2 = self.client.get(reverse('stats'))
        # Puede ser 'yolo' o 'face' dependiendo de si ultralytics está instalado
        self.assertIn(response2.json()['detector'], ['face', 'yolo'])

    def test_stats_update_after_detection(self):
        """
        Prueba de integración: verificar que stats se actualiza
        después de simular detecciones
        """
        # Simular detecciones actualizando GLOBAL_STATE
        GLOBAL_STATE.update_counts(['face', 'face', 'person'])
        
        # Verificar que stats refleja las detecciones
        response = self.client.get(reverse('stats'))
        data = response.json()
        
        self.assertEqual(data['counts']['face'], 2)
        self.assertEqual(data['counts']['person'], 1)


class TestDetectorIntegration(TestCase):
    """Pruebas de integración para los detectores"""

    def setUp(self):
        """Configuración antes de cada prueba"""
        GLOBAL_STATE.reset()

    def test_detector_and_state_integration(self):
        """
        Verificar que el detector actualiza correctamente el estado global
        """
        detector = get_detector('face')
        
        # Crear frame de prueba
        test_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Procesar frame
        result = detector.process(test_frame)
        
        # Verificar que el frame fue procesado
        self.assertIsNotNone(result)
        
        # Verificar estado global
        snapshot = GLOBAL_STATE.snapshot()
        self.assertEqual(snapshot['detector'], 'face')

    def test_face_detector_processing_pipeline(self):
        """
        Prueba de integración completa del pipeline de FaceDetector
        """
        detector = FaceDetector()
        
        # Crear múltiples frames de prueba
        frames = [
            np.zeros((480, 640, 3), dtype=np.uint8),
            np.ones((480, 640, 3), dtype=np.uint8) * 128,
            np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8),
        ]
        
        # Procesar todos los frames
        results = [detector.process(frame) for frame in frames]
        
        # Verificar que todos los frames fueron procesados correctamente
        for result in results:
            self.assertIsNotNone(result)
            self.assertEqual(result.shape, (480, 640, 3))


class TestURLsIntegration(TestCase):
    """Pruebas de integración para las rutas principales de Django"""

    def setUp(self):
        """Configuración antes de cada prueba"""
        self.client = Client()

    def test_all_main_routes_accessible(self):
        """
        Verificar que todas las rutas principales son accesibles
        """
        routes = [
            ('index', {}),
            ('video_feed', {}),
            ('stats', {}),
        ]
        
        for route_name, params in routes:
            with self.subTest(route=route_name):
                response = self.client.get(reverse(route_name), params)
                self.assertEqual(
                    response.status_code,
                    200,
                    f"La ruta {route_name} no es accesible"
                )

    def test_video_feed_with_different_parameters(self):
        """
        Prueba de integración: video_feed con diferentes combinaciones de parámetros
        """
        parameter_combinations = [
            {},
            {'detector': 'face'},
            {'detector': 'face', 'conf': '0.5'},
            {'detector': 'face', 'classes': 'person'},
            {'detector': 'face', 'conf': '0.7', 'classes': 'person,car'},
        ]
        
        for params in parameter_combinations:
            with self.subTest(params=params):
                response = self.client.get(reverse('video_feed'), params)
                self.assertEqual(
                    response.status_code,
                    200,
                    f"video_feed falló con parámetros {params}"
                )


class TestEndToEndScenarios(TestCase):
    """Pruebas de escenarios de extremo a extremo"""

    def setUp(self):
        """Configuración antes de cada prueba"""
        self.client = Client()
        GLOBAL_STATE.reset()

    def test_user_session_scenario(self):
        """
        Escenario completo de sesión de usuario:
        1. Usuario visita la página principal
        2. Usuario inicia video feed
        3. Se realizan detecciones (simuladas)
        4. Usuario consulta estadísticas
        5. Usuario cambia detector
        6. Usuario vuelve a consultar estadísticas
        """
        # Paso 1: Visitar página principal
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        
        # Paso 2: Iniciar video feed con face detector
        response = self.client.get(reverse('video_feed'), {'detector': 'face'})
        self.assertEqual(response.status_code, 200)
        
        # Paso 3: Simular detecciones
        GLOBAL_STATE.update_counts(['face', 'face'])
        
        # Paso 4: Consultar estadísticas
        response = self.client.get(reverse('stats'))
        data = response.json()
        self.assertEqual(data['counts']['face'], 2)
        
        # Paso 5: Cambiar detector (resetear y cambiar)
        GLOBAL_STATE.reset()
        response = self.client.get(reverse('video_feed'), {'detector': 'face'})
        
        # Paso 6: Consultar estadísticas nuevamente
        response = self.client.get(reverse('stats'))
        data = response.json()
        self.assertEqual(data['counts'], {})

    def test_concurrent_stats_access(self):
        """
        Verificar que múltiples accesos concurrentes a stats funcionan correctamente
        """
        # Actualizar estado
        GLOBAL_STATE.update_counts(['face', 'person'])
        
        # Múltiples solicitudes concurrentes simuladas
        responses = [self.client.get(reverse('stats')) for _ in range(5)]
        
        # Verificar que todas las respuestas son correctas
        for response in responses:
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data['counts']['face'], 1)
            self.assertEqual(data['counts']['person'], 1)


if __name__ == '__main__':
    unittest.main()

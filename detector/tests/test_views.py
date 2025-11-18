"""
Pruebas unitarias para las vistas de Django
Validan el comportamiento de las vistas y respuestas HTTP
"""
import unittest
from django.test import TestCase, Client
from django.urls import reverse
from detector.state import GLOBAL_STATE


class TestIndexView(TestCase):
    """Pruebas para la vista principal (index)"""

    def setUp(self):
        """Configuración antes de cada prueba"""
        self.client = Client()
        GLOBAL_STATE.reset()

    def test_index_view_status_code(self):
        """Verificar que la vista index retorna código 200"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_index_view_uses_correct_template(self):
        """Verificar que la vista index usa el template correcto"""
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'detector/index.html')

    def test_index_view_accessible_by_name(self):
        """Verificar que la vista es accesible por su nombre"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


class TestVideoFeedView(TestCase):
    """Pruebas para la vista de video feed"""

    def setUp(self):
        """Configuración antes de cada prueba"""
        self.client = Client()
        GLOBAL_STATE.reset()

    def test_video_feed_view_status_code(self):
        """Verificar que video_feed retorna código 200"""
        response = self.client.get(reverse('video_feed'))
        self.assertEqual(response.status_code, 200)

    def test_video_feed_content_type(self):
        """Verificar que video_feed retorna el content-type correcto"""
        response = self.client.get(reverse('video_feed'))
        self.assertEqual(
            response['Content-Type'],
            'multipart/x-mixed-replace; boundary=frame'
        )

    def test_video_feed_with_face_detector_parameter(self):
        """Verificar que video_feed acepta el parámetro detector=face"""
        response = self.client.get(reverse('video_feed'), {'detector': 'face'})
        self.assertEqual(response.status_code, 200)

    def test_video_feed_with_confidence_parameter(self):
        """Verificar que video_feed acepta el parámetro conf"""
        response = self.client.get(
            reverse('video_feed'),
            {'detector': 'face', 'conf': '0.7'}
        )
        self.assertEqual(response.status_code, 200)

    def test_video_feed_with_classes_parameter(self):
        """Verificar que video_feed acepta el parámetro classes"""
        response = self.client.get(
            reverse('video_feed'),
            {'detector': 'face', 'classes': 'person,car'}
        )
        self.assertEqual(response.status_code, 200)

    def test_video_feed_is_streaming_response(self):
        """Verificar que video_feed retorna StreamingHttpResponse"""
        from django.http import StreamingHttpResponse
        response = self.client.get(reverse('video_feed'))
        self.assertIsInstance(response, StreamingHttpResponse)


class TestStatsView(TestCase):
    """Pruebas para la vista de estadísticas"""

    def setUp(self):
        """Configuración antes de cada prueba"""
        self.client = Client()
        GLOBAL_STATE.reset()

    def test_stats_view_status_code(self):
        """Verificar que stats retorna código 200"""
        response = self.client.get(reverse('stats'))
        self.assertEqual(response.status_code, 200)

    def test_stats_view_returns_json(self):
        """Verificar que stats retorna una respuesta JSON"""
        response = self.client.get(reverse('stats'))
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_stats_view_json_structure(self):
        """Verificar que stats retorna la estructura JSON correcta"""
        response = self.client.get(reverse('stats'))
        data = response.json()
        
        self.assertIn('detector', data)
        self.assertIn('counts', data)

    def test_stats_view_initial_counts_empty(self):
        """Verificar que los contadores iniciales están vacíos"""
        response = self.client.get(reverse('stats'))
        data = response.json()
        
        self.assertEqual(data['counts'], {})

    def test_stats_view_reflects_global_state(self):
        """Verificar que stats refleja el estado global actualizado"""
        # Actualizar estado global
        GLOBAL_STATE.update_counts(['face', 'face', 'person'])
        GLOBAL_STATE.set_detector('face')
        
        response = self.client.get(reverse('stats'))
        data = response.json()
        
        self.assertEqual(data['detector'], 'face')
        self.assertEqual(data['counts']['face'], 2)
        self.assertEqual(data['counts']['person'], 1)


class TestURLConfiguration(TestCase):
    """Pruebas para la configuración de URLs"""

    def test_index_url_resolves(self):
        """Verificar que la URL index se resuelve correctamente"""
        url = reverse('index')
        self.assertEqual(url, '/')

    def test_video_feed_url_resolves(self):
        """Verificar que la URL video_feed se resuelve correctamente"""
        url = reverse('video_feed')
        self.assertEqual(url, '/video_feed')

    def test_stats_url_resolves(self):
        """Verificar que la URL stats se resuelve correctamente"""
        url = reverse('stats')
        self.assertEqual(url, '/stats')


if __name__ == '__main__':
    unittest.main()

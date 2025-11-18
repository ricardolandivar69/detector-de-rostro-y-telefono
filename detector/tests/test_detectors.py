"""
Pruebas unitarias para el módulo de detección con OpenCV
Estas pruebas validan las funciones críticas del sistema de detección
"""
import unittest
import numpy as np
import cv2
from detector.detectors import FaceDetector, BaseDetector, get_detector
from detector.state import GLOBAL_STATE


class TestBaseDetector(unittest.TestCase):
    """Pruebas para el detector base"""

    def setUp(self):
        """Configuración antes de cada prueba"""
        GLOBAL_STATE.reset()
        self.detector = BaseDetector()

    def test_base_detector_name(self):
        """Verificar que el detector base tiene el nombre correcto"""
        self.assertEqual(self.detector.name, 'base')

    def test_base_detector_returns_frame(self):
        """Verificar que el detector base retorna el frame sin modificar"""
        # Crear un frame de prueba (imagen negra de 100x100)
        test_frame = np.zeros((100, 100, 3), dtype=np.uint8)
        result = self.detector.process(test_frame)
        
        # Verificar que el resultado es el mismo frame
        np.testing.assert_array_equal(result, test_frame)


class TestFaceDetector(unittest.TestCase):
    """Pruebas unitarias para FaceDetector - función crítica del sistema"""

    def setUp(self):
        """Configuración antes de cada prueba"""
        GLOBAL_STATE.reset()
        self.detector = FaceDetector()

    def test_face_detector_initialization(self):
        """Verificar que el detector de rostros se inicializa correctamente"""
        self.assertIsNotNone(self.detector.face_cascade)
        self.assertEqual(self.detector.name, 'face')

    def test_face_detector_with_empty_frame(self):
        """Verificar que el detector maneja correctamente un frame vacío"""
        # Frame negro de 100x100
        empty_frame = np.zeros((100, 100, 3), dtype=np.uint8)
        result = self.detector.process(empty_frame)
        
        # Verificar que retorna un frame válido
        self.assertIsNotNone(result)
        self.assertEqual(result.shape, empty_frame.shape)

    def test_face_detector_returns_valid_frame(self):
        """Verificar que el detector retorna un frame válido con dimensiones correctas"""
        # Frame de prueba con dimensiones específicas
        test_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        result = self.detector.process(test_frame)
        
        # Verificar dimensiones
        self.assertEqual(result.shape, test_frame.shape)
        self.assertEqual(result.dtype, np.uint8)

    def test_face_detector_adds_text_overlay(self):
        """Verificar que el detector agrega texto al frame procesado"""
        test_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        original_frame = test_frame.copy()
        
        result = self.detector.process(test_frame)
        
        # El frame debe ser modificado (texto agregado)
        # No deben ser exactamente iguales
        self.assertFalse(np.array_equal(result, original_frame))

    def test_face_detector_with_real_image(self):
        """Prueba con una imagen sintética que simula un rostro"""
        # Crear imagen con un rectángulo blanco que podría ser detectado
        test_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        # Agregar un óvalo blanco simulando un rostro
        cv2.ellipse(test_frame, (320, 240), (80, 100), 0, 0, 360, (255, 255, 255), -1)
        # Agregar "ojos" (círculos oscuros)
        cv2.circle(test_frame, (290, 220), 10, (50, 50, 50), -1)
        cv2.circle(test_frame, (350, 220), 10, (50, 50, 50), -1)
        
        result = self.detector.process(test_frame)
        
        # Verificar que se procesó correctamente
        self.assertIsNotNone(result)
        self.assertEqual(result.shape, (480, 640, 3))


class TestGetDetector(unittest.TestCase):
    """Pruebas para la función get_detector - función crítica de selección"""

    def setUp(self):
        """Configuración antes de cada prueba"""
        GLOBAL_STATE.reset()

    def test_get_detector_default(self):
        """Verificar que get_detector retorna FaceDetector por defecto"""
        detector = get_detector('face')
        self.assertIsInstance(detector, FaceDetector)
        self.assertEqual(detector.name, 'face')

    def test_get_detector_empty_name(self):
        """Verificar que get_detector maneja nombres vacíos correctamente"""
        detector = get_detector('')
        self.assertIsInstance(detector, FaceDetector)

    def test_get_detector_none_name(self):
        """Verificar que get_detector maneja None correctamente"""
        detector = get_detector(None)
        self.assertIsInstance(detector, FaceDetector)

    def test_get_detector_updates_global_state(self):
        """Verificar que get_detector actualiza el estado global"""
        get_detector('face')
        snapshot = GLOBAL_STATE.snapshot()
        self.assertEqual(snapshot['detector'], 'face')

    def test_get_detector_case_insensitive(self):
        """Verificar que get_detector no es sensible a mayúsculas"""
        detector1 = get_detector('FACE')
        detector2 = get_detector('Face')
        detector3 = get_detector('face')
        
        self.assertIsInstance(detector1, FaceDetector)
        self.assertIsInstance(detector2, FaceDetector)
        self.assertIsInstance(detector3, FaceDetector)


class TestGlobalState(unittest.TestCase):
    """Pruebas para el estado global del sistema"""

    def setUp(self):
        """Configuración antes de cada prueba"""
        GLOBAL_STATE.reset()

    def test_global_state_initial_values(self):
        """Verificar valores iniciales del estado global"""
        snapshot = GLOBAL_STATE.snapshot()
        self.assertIn('detector', snapshot)
        self.assertIn('counts', snapshot)
        self.assertEqual(snapshot['counts'], {})

    def test_global_state_update_counts(self):
        """Verificar que update_counts funciona correctamente"""
        GLOBAL_STATE.update_counts(['face', 'face', 'person'])
        snapshot = GLOBAL_STATE.snapshot()
        
        self.assertEqual(snapshot['counts']['face'], 2)
        self.assertEqual(snapshot['counts']['person'], 1)

    def test_global_state_reset(self):
        """Verificar que reset limpia los contadores"""
        GLOBAL_STATE.update_counts(['face', 'person'])
        GLOBAL_STATE.reset()
        snapshot = GLOBAL_STATE.snapshot()
        
        self.assertEqual(snapshot['counts'], {})

    def test_global_state_set_detector(self):
        """Verificar que set_detector actualiza el detector activo"""
        GLOBAL_STATE.set_detector('yolo')
        snapshot = GLOBAL_STATE.snapshot()
        
        self.assertEqual(snapshot['detector'], 'yolo')

    def test_global_state_thread_safety(self):
        """Verificar que las operaciones son thread-safe"""
        import threading
        
        def update_counts():
            for _ in range(100):
                GLOBAL_STATE.update_counts(['face'])
        
        threads = [threading.Thread(target=update_counts) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        snapshot = GLOBAL_STATE.snapshot()
        # Debe haber exactamente 500 detecciones (5 threads * 100 actualizaciones)
        self.assertEqual(snapshot['counts']['face'], 500)


if __name__ == '__main__':
    unittest.main()

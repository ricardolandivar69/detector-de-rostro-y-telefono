# EJEMPLOS DE CÓDIGO - PRUEBAS IMPLEMENTADAS

## Este archivo contiene ejemplos de las pruebas más importantes
## Úsalo como referencia para anexos en tu reporte

---

## 📌 EJEMPLO 1: Prueba Unitaria - FaceDetector con OpenCV

```python
def test_face_detector_initialization(self):
    """Verificar que el detector de rostros se inicializa correctamente"""
    self.assertIsNotNone(self.detector.face_cascade)
    self.assertEqual(self.detector.name, 'face')
```

**Explicación:**
Esta prueba valida que el detector facial se inicializa correctamente,
verificando que el modelo Haar Cascade de OpenCV se carga sin errores.

**Función crítica probada:** 
- `cv2.CascadeClassifier()` - Carga del modelo de detección

---

## 📌 EJEMPLO 2: Prueba Unitaria - Procesamiento de Frame

```python
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
```

**Explicación:**
Esta prueba crea una imagen sintética simulando un rostro y valida que
el detector la procesa correctamente sin errores.

**Funciones críticas probadas:**
- `FaceDetector.process()` - Pipeline completo de detección
- `cv2.detectMultiScale()` - Algoritmo de detección facial

---

## 📌 EJEMPLO 3: Prueba de Thread-Safety (Concurrencia)

```python
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
```

**Explicación:**
Esta prueba crea 5 threads concurrentes que actualizan el estado global
simultáneamente. Valida que no hay condiciones de carrera (race conditions)
y que el contador final es correcto (500).

**Funciones críticas probadas:**
- `threading.Lock()` - Sincronización de threads
- `GLOBAL_STATE.update_counts()` - Operación thread-safe

---

## 📌 EJEMPLO 4: Prueba de Integración - Flujo Completo

```python
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
```

**Explicación:**
Esta prueba valida el flujo completo de un usuario:
1. Accede a la página principal (/)
2. Inicia el video feed (/video_feed)
3. Consulta las estadísticas (/stats)

**Componentes integrados:**
- Vista Index
- Vista VideoFeed (streaming)
- Vista Stats (API JSON)
- URLs de Django
- Cliente HTTP de prueba

---

## 📌 EJEMPLO 5: Prueba de Vista Django - JSON Response

```python
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
```

**Explicación:**
Esta prueba valida que el endpoint /stats retorna correctamente
el estado actual del sistema en formato JSON.

**Funciones críticas probadas:**
- `views.stats()` - Vista Django
- `JsonResponse` - Serialización JSON
- Integración con GLOBAL_STATE

---

## 📊 ESTADÍSTICAS DE LOS EJEMPLOS

- **Total de líneas de código de pruebas:** ~450 líneas
- **Assertions por prueba (promedio):** 2-3
- **Frameworks usados:**
  - unittest (estándar Python)
  - Django TestCase
  - pytest (opcional)
  
- **Librerías de testing:**
  - cv2 (OpenCV) - Para pruebas de visión
  - numpy - Para manipulación de arrays
  - threading - Para pruebas de concurrencia

---

## 🔍 PATRONES DE TESTING UTILIZADOS

### 1. Arrange-Act-Assert (AAA)
```python
def test_example(self):
    # Arrange (Preparar)
    detector = FaceDetector()
    test_frame = np.zeros((100, 100, 3), dtype=np.uint8)
    
    # Act (Actuar)
    result = detector.process(test_frame)
    
    # Assert (Verificar)
    self.assertIsNotNone(result)
```

### 2. Setup y Teardown
```python
def setUp(self):
    """Configuración antes de cada prueba"""
    GLOBAL_STATE.reset()
    self.detector = FaceDetector()

def tearDown(self):
    """Limpieza después de cada prueba"""
    GLOBAL_STATE.reset()
```

### 3. Fixtures (datos de prueba)
```python
# Frames de prueba reutilizables
self.empty_frame = np.zeros((480, 640, 3), dtype=np.uint8)
self.random_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
```

---

## 📚 REFERENCIAS TEÓRICAS

### ¿Qué es una prueba unitaria?
Prueba que valida una unidad mínima de código (función, método, clase)
de forma aislada, sin dependencias externas.

**Ejemplo en este proyecto:**
- Probar `FaceDetector.process()` con un frame sintético

### ¿Qué es una prueba de integración?
Prueba que valida la interacción entre múltiples componentes del sistema
trabajando juntos.

**Ejemplo en este proyecto:**
- Probar flujo completo: Index → VideoFeed → Stats

### ¿Por qué es importante la cobertura?
La cobertura mide qué porcentaje del código es ejecutado por las pruebas.
Una cobertura del 85% significa que el 85% de las líneas de código fueron
probadas, reduciendo el riesgo de bugs.

---

## 💡 CONCLUSIONES TÉCNICAS

✅ **Ventajas de las pruebas implementadas:**
1. Detección temprana de errores
2. Documentación viva del código
3. Facilita refactoring seguro
4. Valida comportamiento esperado
5. Evita regresiones

⚠️ **Limitaciones identificadas:**
1. YOLODetector no probado (dependencia opcional)
2. video.py con baja cobertura (requiere hardware)
3. Pruebas de UI pendientes (Selenium/Playwright)

🎯 **Próximos pasos recomendados:**
1. Implementar pruebas para YOLODetector
2. Agregar mocks para cámara en video.py
3. Pruebas de rendimiento (benchmark)
4. Integración continua (CI/CD)

---

**Este código está listo para ser incluido en tu reporte académico.**
**Puedes copiar los ejemplos y explicaciones según lo requiera tu profesor.**

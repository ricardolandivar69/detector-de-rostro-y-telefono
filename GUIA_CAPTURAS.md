# 📸 GUÍA PARA CAPTURAS DE PANTALLA - EVIDENCIAS DE PRUEBAS

## Producto esperado según actividad:
**"Reporte inicial de pruebas ejecutadas con resultados (logs o capturas de pantalla)"**

---

## 📋 CAPTURAS REQUERIDAS PARA TU REPORTE

### 1️⃣ CAPTURA: Ejecución completa de pruebas
**Comando a ejecutar y capturar:**
```bash
python manage.py test detector.tests -v 2
```

**Qué debe mostrar:**
- Total de 44 pruebas encontradas
- Listado de todas las pruebas con resultado OK
- Mensaje final: "Ran 44 tests in X.XXXs - OK"
- Sin errores ni fallos

**Nombre sugerido:** `01_ejecucion_completa_pruebas.png`

---

### 2️⃣ CAPTURA: Reporte de cobertura en consola
**Comando a ejecutar y capturar:**
```bash
coverage report
```

**Qué debe mostrar:**
- Tabla con todos los módulos
- Columnas: Name, Stmts, Miss, Cover
- Cobertura total: 85%
- Destacar state.py con 100%

**Nombre sugerido:** `02_reporte_cobertura.png`

---

### 3️⃣ CAPTURA: Reporte HTML de cobertura (Página principal)
**Ya abierto en tu navegador**

**Qué capturar:**
- Página principal de htmlcov/index.html
- Barra de progreso mostrando 85%
- Listado de archivos con sus porcentajes
- Colores verde (>80%), amarillo (50-80%), rojo (<50%)

**Nombre sugerido:** `03_reporte_html_principal.png`

---

### 4️⃣ CAPTURA: Detalle de cobertura - state.py (100%)
**En el reporte HTML, hacer clic en `state.py`**

**Qué capturar:**
- Código fuente con líneas marcadas en verde (ejecutadas)
- Indicador de 100% coverage
- Todas las funciones críticas cubiertas

**Nombre sugerido:** `04_detalle_state_100.png`

---

### 5️⃣ CAPTURA: Detalle de cobertura - detectors.py
**En el reporte HTML, hacer clic en `detectors.py`**

**Qué capturar:**
- FaceDetector completamente testeado (verde)
- YOLODetector sin testear (rojo/amarillo)
- Esto explica el 58% de cobertura

**Nombre sugerido:** `05_detalle_detectors.png`

---

### 6️⃣ CAPTURA: Pruebas unitarias específicas
**Comando a ejecutar y capturar:**
```bash
python manage.py test detector.tests.test_detectors -v 2
```

**Qué debe mostrar:**
- Solo las 17 pruebas unitarias
- TestBaseDetector (2)
- TestFaceDetector (5)
- TestGetDetector (5)
- TestGlobalState (5)

**Nombre sugerido:** `06_pruebas_unitarias.png`

---

### 7️⃣ CAPTURA: Pruebas de integración
**Comando a ejecutar y capturar:**
```bash
python manage.py test detector.tests.test_integration -v 2
```

**Qué debe mostrar:**
- Las 10 pruebas de integración
- Flujos completos validados
- Sin errores

**Nombre sugerido:** `07_pruebas_integracion.png`

---

### 8️⃣ CAPTURA (OPCIONAL): Estructura de archivos de prueba
**En VS Code o explorador de archivos**

**Qué capturar:**
- Carpeta detector/tests/
- Archivos: __init__.py, test_detectors.py, test_integration.py, test_views.py
- Tamaño de archivos (para mostrar complejidad)

**Nombre sugerido:** `08_estructura_tests.png`

---

## 📊 RESUMEN DE EVIDENCIAS PARA TU REPORTE

### Capturas Obligatorias (mínimo):
1. ✅ Ejecución completa de 44 pruebas
2. ✅ Reporte de cobertura (85%)
3. ✅ Reporte HTML (página principal)

### Capturas Recomendadas (para mejor nota):
4. ✅ Detalle de módulo con 100% (state.py)
5. ✅ Pruebas unitarias (17)
6. ✅ Pruebas de integración (10)

### Capturas Opcionales (extras):
7. ⭐ Detalle de detectors.py
8. ⭐ Estructura de archivos

---

## 📝 DOCUMENTOS YA GENERADOS

Además de las capturas, ya tienes estos archivos listos:

1. **REPORTE_PRUEBAS.md** 
   - Reporte completo en Markdown
   - Detalle de las 44 pruebas
   - Análisis de cobertura
   - Conclusiones y recomendaciones

2. **RESUMEN_EJECUTIVO.txt**
   - Resumen visual con tablas
   - Resultados generales
   - Comandos de ejecución

3. **htmlcov/** (carpeta)
   - Reporte interactivo HTML
   - Navegable por módulos
   - Colores y gráficos

---

## 🎯 CÓMO ARMAR TU REPORTE FINAL

### Opción 1: Documento Word/PDF
```
1. Portada con datos personales
2. Introducción (objetivos de la sesión)
3. Metodología (qué herramientas usaste)
4. Resultados:
   - Pegar RESUMEN_EJECUTIVO.txt
   - Insertar capturas de pantalla
5. Conclusiones personales
6. Anexos (código de algunas pruebas importantes)
```

### Opción 2: Presentación (si lo requieren)
```
Diapositiva 1: Portada
Diapositiva 2: Objetivos
Diapositiva 3: Resultados generales (44/44 pruebas OK)
Diapositiva 4: Pruebas unitarias (captura)
Diapositiva 5: Pruebas de integración (captura)
Diapositiva 6: Cobertura de código (85%)
Diapositiva 7: Reporte HTML (captura)
Diapositiva 8: Conclusiones
```

### Opción 3: Entregar archivos directamente
```
Si tu profesor acepta archivos:
- REPORTE_PRUEBAS.md
- RESUMEN_EJECUTIVO.txt
- Carpeta con capturas
- htmlcov.zip (opcional)
```

---

## ⚡ COMANDOS RÁPIDOS PARA COPIAR/PEGAR

```bash
# 1. Ejecutar todas las pruebas
python manage.py test detector.tests -v 2

# 2. Solo unitarias
python manage.py test detector.tests.test_detectors -v 2

# 3. Solo integración
python manage.py test detector.tests.test_integration -v 2

# 4. Generar cobertura
coverage run --source='detector' manage.py test detector.tests
coverage report
coverage html

# 5. Abrir reporte HTML
start htmlcov\index.html
```

---

## 💡 TIPS PARA MEJORES CAPTURAS

1. **Pantalla completa** - Maximiza la terminal antes de capturar
2. **Fuente legible** - Aumenta tamaño si es necesario (Ctrl + rueda del mouse)
3. **Sin información personal** - Revisa que no aparezcan datos sensibles
4. **Fondo oscuro** - Se ve más profesional (opcional)
5. **Recortar** - Elimina bordes innecesarios en las capturas
6. **Numerarlas** - Facilita referenciarlas en el reporte

---

## ✅ CHECKLIST FINAL

Antes de entregar, verifica que tengas:

- [ ] Al menos 3 capturas de pantalla
- [ ] REPORTE_PRUEBAS.md o equivalente
- [ ] Documento Word/PDF con tu nombre y datos
- [ ] Conclusiones personales sobre la actividad
- [ ] Referencias a las herramientas usadas (pytest, coverage, Django)
- [ ] Explicación de qué son pruebas unitarias vs integración

---

## 🎓 PUNTOS CLAVE PARA TU INFORME

**Menciona en tus conclusiones:**

1. Se implementaron **44 pruebas** (17 unitarias + 27 integración)
2. Cobertura de código: **85%** (excelente)
3. Funciones críticas validadas: **Detección facial con OpenCV**
4. Thread-safety probado con **500 operaciones concurrentes**
5. Framework usado: **Django TestCase + pytest**
6. Tiempo de ejecución: **< 1 segundo** (muy eficiente)
7. Todas las pruebas: **✅ APROBADAS**

---

**¡Éxito con tu entrega! 🚀**

Tienes todo el material necesario para un reporte completo y profesional.

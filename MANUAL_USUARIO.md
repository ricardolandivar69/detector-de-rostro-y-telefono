# 📖 MANUAL DE USUARIO - SmartVision

## Guía Completa para Usuarios del Sistema de Detección de Rostros

**Versión:** 1.0  
**Fecha:** 18 de Noviembre de 2025  
**Para:** Usuarios finales del sistema  

---

## 📋 TABLA DE CONTENIDOS

1. [Introducción](#introducción)
2. [Requisitos Previos](#requisitos-previos)
3. [Instalación Rápida](#instalación-rápida)
4. [Guía de Uso Paso a Paso](#guía-de-uso-paso-a-paso)
5. [Capturas de Pantalla](#capturas-de-pantalla)
6. [Explicación de Resultados](#explicación-de-resultados)
7. [Casos de Uso Comunes](#casos-de-uso-comunes)
8. [Preguntas Frecuentes](#preguntas-frecuentes)
9. [Solución de Problemas](#solución-de-problemas)

---

## 1. INTRODUCCIÓN

### ¿Qué es SmartVision?

SmartVision es un sistema de detección de rostros en tiempo real que utiliza la cámara de tu computadora para identificar y contar rostros. El sistema procesa el video en vivo y muestra los resultados instantáneamente en tu navegador web.

### ¿Para qué sirve?

- 🎯 **Conteo de personas:** Detecta cuántas personas están frente a la cámara
- 📊 **Estadísticas:** Lleva un registro del total de detecciones
- 🔄 **Tiempo real:** Procesa video en vivo con baja latencia
- 🌐 **Acceso web:** No requiere instalar aplicaciones adicionales

### ¿Quién puede usarlo?

- Estudiantes de programación
- Desarrolladores aprendiendo visión por computadora
- Docentes demostrando conceptos de IA
- Cualquier persona interesada en detección de rostros

---

## 2. REQUISITOS PREVIOS

### ✅ Lo que necesitas tener instalado:

- **Computadora con:**
  - Windows 10/11, Linux o macOS
  - Cámara web funcionando
  - Mínimo 4 GB de RAM
  - 500 MB de espacio libre

- **Software:**
  - Python 3.13 o superior → [Descargar aquí](https://www.python.org/downloads/)
  - Navegador web moderno (Chrome, Firefox, Edge)

### 🔍 Verificar que tienes Python instalado:

1. Abre la terminal (CMD en Windows, Terminal en Mac/Linux)
2. Escribe: `python --version`
3. Debe aparecer algo como: `Python 3.13.3`

---

## 3. INSTALACIÓN RÁPIDA

### Opción A: Instalación Completa (Recomendada)

**Paso 1:** Descarga el proyecto
```bash
# Si tienes git instalado
git clone https://github.com/tu-usuario/smartvision.git
cd smartvision

# Si descargaste un ZIP, descomprime y abre la carpeta
```

**Paso 2:** Instala las dependencias
```bash
pip install -r requirements.txt
```

**Paso 3:** Prepara la base de datos
```bash
python manage.py migrate
```

**Paso 4:** Inicia el servidor
```bash
python manage.py runserver
```

**Paso 5:** Abre tu navegador
```
http://localhost:8000
```

¡Listo! El sistema ya está funcionando 🎉

---

### Opción B: Instalación Paso a Paso Detallada

#### 1️⃣ Crear entorno virtual (opcional pero recomendado)

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Verás `(venv)` al inicio de tu terminal.

#### 2️⃣ Instalar paquetes uno por uno

```bash
pip install Django==5.1.3
pip install opencv-python==4.12.0
pip install numpy==1.26.0
```

#### 3️⃣ Verificar instalación

```bash
python -c "import cv2; print(f'OpenCV {cv2.__version__} OK')"
```

Debe aparecer: `OpenCV 4.12.0 OK`

#### 4️⃣ Configurar Django

```bash
python manage.py check
```

Debe decir: `System check identified no issues`

#### 5️⃣ Iniciar servidor

```bash
python manage.py runserver
```

Verás:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

---

## 4. GUÍA DE USO PASO A PASO

### 🚀 Primera Vez Usando el Sistema

#### Paso 1: Iniciar el Sistema

1. Abre la terminal en la carpeta del proyecto
2. Activa el entorno virtual (si lo creaste)
3. Ejecuta: `python manage.py runserver`
4. Espera a ver el mensaje: `Starting development server...`

#### Paso 2: Abrir la Interfaz

1. Abre tu navegador web favorito
2. Ve a: `http://localhost:8000`
3. Deberías ver la página principal de SmartVision

#### Paso 3: Permitir Acceso a la Cámara

1. El navegador pedirá permiso para usar la cámara
2. Haz clic en **"Permitir"** o **"Allow"**
3. Espera unos segundos mientras el sistema se conecta

#### Paso 4: Ver la Detección en Acción

1. El video de tu cámara aparecerá en pantalla
2. Cuando detecte un rostro, dibujará un **rectángulo verde**
3. En la esquina verás: **"Faces: 1"** (o el número de rostros detectados)

#### Paso 5: Consultar Estadísticas

1. En la parte inferior de la pantalla verás contadores
2. **Detector actual:** Muestra qué algoritmo está en uso
3. **Total de detecciones:** Cuenta acumulada desde que iniciaste

---

### 🎮 Usando las Funciones Avanzadas

#### Cambiar Parámetros del Detector

Puedes modificar la URL para cambiar configuraciones:

**Usar detector de rostros (por defecto):**
```
http://localhost:8000/video_feed?detector=face
```

**Cambiar nivel de confianza (0.0 a 1.0):**
```
http://localhost:8000/video_feed?conf=0.7
```

Valores de confianza:
- `0.3` = Más sensible (detecta más, pero puede dar falsos positivos)
- `0.5` = Balanceado (recomendado)
- `0.7` = Más estricto (solo detecciones muy seguras)

#### Reiniciar Contadores

1. Detén el servidor (Ctrl+C en la terminal)
2. Vuelve a iniciarlo: `python manage.py runserver`
3. Los contadores volverán a 0

---

## 5. CAPTURAS DE PANTALLA

### 📸 Captura 1: Página Principal

**Qué verás:**
- Título "SmartVision" en la parte superior
- Área de video en el centro
- Indicador de FPS (frames por segundo)
- Panel de estadísticas en la parte inferior

**Ubicación sugerida:** `screenshots/01_pagina_principal.png`

```
┌────────────────────────────────────────┐
│         🎥 SMARTVISION                 │
├────────────────────────────────────────┤
│                                        │
│    ┌────────────────────────────┐     │
│    │                            │     │
│    │   📹 VIDEO EN VIVO         │     │
│    │   (Rostro con rectángulo)  │     │
│    │   Faces: 1                 │     │
│    │                            │     │
│    └────────────────────────────┘     │
│                                        │
│  Detector: face                        │
│  Total detecciones: 127                │
└────────────────────────────────────────┘
```

---

### 📸 Captura 2: Detección en Acción

**Cómo tomarla:**
1. Colócate frente a la cámara
2. Espera a que aparezca el rectángulo verde
3. Toma captura de pantalla (Win+Shift+S en Windows)

**Qué debe mostrar:**
- Video en vivo con tu rostro
- Rectángulo verde rodeando tu cara
- Texto "Faces: 1" en la esquina superior izquierda
- Valor de FPS (ejemplo: "30 FPS")

**Ubicación sugerida:** `screenshots/02_deteccion_activa.png`

---

### 📸 Captura 3: Múltiples Rostros

**Cómo tomarla:**
1. Pide a 2-3 personas que se coloquen frente a la cámara
2. Espera a que todos tengan rectángulos verdes
3. Toma la captura

**Qué debe mostrar:**
- Múltiples rostros con rectángulos verdes
- Texto "Faces: 3" (o el número correspondiente)
- Contadores actualizados

**Ubicación sugerida:** `screenshots/03_multiples_rostros.png`

---

### 📸 Captura 4: Estadísticas JSON

**Cómo tomarla:**
1. En el navegador, ve a: `http://localhost:8000/stats`
2. Verás datos en formato JSON
3. Toma captura

**Qué debe mostrar:**
```json
{
    "detector": "face",
    "counts": {
        "face": 152
    }
}
```

**Ubicación sugerida:** `screenshots/04_estadisticas_json.png`

---

### 📸 Captura 5: Terminal con Servidor Activo

**Cómo tomarla:**
1. Muestra la terminal donde ejecutaste `runserver`
2. Debe verse el log del servidor
3. Toma captura

**Qué debe mostrar:**
```
System check identified no issues (0 silenced).
November 18, 2025 - 10:30:45
Django version 5.1.3, using settings 'smartvision.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
[18/Nov/2025 10:30:52] "GET / HTTP/1.1" 200 1234
[18/Nov/2025 10:30:53] "GET /video_feed HTTP/1.1" 200 0
```

**Ubicación sugerida:** `screenshots/05_servidor_activo.png`

---

## 6. EXPLICACIÓN DE RESULTADOS

### 🎯 ¿Qué significan los números?

#### "Faces: X"

**Ubicación:** Esquina superior izquierda del video

**Significado:**
- Número de rostros detectados **en el frame actual**
- Se actualiza en tiempo real (30 veces por segundo)
- Puede variar entre 0 y el número de personas presentes

**Ejemplos:**
- `Faces: 0` → No hay nadie frente a la cámara
- `Faces: 1` → Una persona detectada
- `Faces: 3` → Tres personas detectadas

---

#### Rectángulos Verdes

**Qué son:**
- Boxes de delimitación alrededor de cada rostro
- Dibujados por el algoritmo de detección
- Color: Verde (RGB: 0, 255, 0)
- Grosor: 2 píxeles

**Significado:**
- El sistema está **seguro** de que hay un rostro ahí
- La posición es precisa (sigue tu cara si te mueves)
- Tamaño del rectángulo = tamaño estimado del rostro

---

#### Estadísticas Acumuladas

**Total de detecciones:**
- Suma de todas las detecciones desde que iniciaste
- **NO** es el número de personas diferentes
- Es un contador que aumenta con cada frame procesado

**Ejemplo de interpretación:**
```
Detector: face
Total detecciones: 1,523
```

**Significa:**
- Se usó el detector de rostros
- En 1,523 frames se detectó al menos un rostro
- A 30 FPS, esto equivale a ~50 segundos de video

---

#### FPS (Frames Por Segundo)

**Qué es:**
- Velocidad de procesamiento del sistema
- Cuántas imágenes procesa por segundo

**Valores normales:**
- **20-30 FPS:** Excelente, video fluido
- **10-20 FPS:** Bueno, aceptable
- **< 10 FPS:** Lento, puede verse entrecortado

**Factores que afectan:**
- Potencia de tu CPU
- Resolución de la cámara
- Número de rostros en escena

---

### 🧮 Fórmulas y Cálculos

#### Precisión de la Detección

```
Precisión = (Rostros detectados) / (Rostros reales)
```

**Ejemplo:**
- Rostros reales: 3 personas
- Rostros detectados: 3
- Precisión: 100% ✅

#### Tiempo de Procesamiento

```
Tiempo por frame = 1 / FPS
```

**Ejemplo:**
- FPS: 30
- Tiempo: 1/30 = 0.033 segundos = 33 milisegundos

---

## 7. CASOS DE USO COMUNES

### 📚 Caso 1: Contar Personas en una Sala

**Objetivo:** Saber cuántas personas están en un espacio

**Pasos:**
1. Coloca la cámara con vista a la sala
2. Inicia SmartVision
3. Lee el valor "Faces: X"
4. Ese número es la cantidad de personas visibles

**Limitaciones:**
- Solo cuenta rostros visibles (no personas de espaldas)
- Puede contar la misma persona varias veces si se mueve

---

### 🎓 Caso 2: Demo Educativa de IA

**Objetivo:** Mostrar cómo funciona la detección de rostros

**Pasos:**
1. Proyecta la pantalla en clase
2. Pide a estudiantes que pasen al frente
3. Muestra cómo aparecen/desaparecen los rectángulos
4. Explica el algoritmo Haar Cascades

**Puntos a destacar:**
- Tiempo real vs procesamiento posterior
- Tasa de aciertos (true positives)
- Falsos positivos (detecta objetos como rostros)

---

### 🔬 Caso 3: Experimento de Rendimiento

**Objetivo:** Medir cómo afecta el número de personas al FPS

**Pasos:**
1. Inicia con 0 personas → Anota FPS
2. Agrega 1 persona → Anota FPS
3. Agrega 2 personas → Anota FPS
4. Agrega 3 personas → Anota FPS

**Resultados esperados:**
```
0 rostros: 35 FPS
1 rostro:  32 FPS
2 rostros: 28 FPS
3 rostros: 24 FPS
```

**Conclusión:** Más rostros = más cálculos = menor FPS

---

### 📊 Caso 4: Análisis de Datos

**Objetivo:** Exportar estadísticas para análisis

**Pasos:**
1. Accede a `http://localhost:8000/stats`
2. Copia el JSON
3. Pégalo en un archivo `datos.json`
4. Procesa con Python/Excel

**Ejemplo de procesamiento:**
```python
import json

with open('datos.json') as f:
    stats = json.load(f)

print(f"Total detecciones: {stats['counts']['face']}")
```

---

## 8. PREGUNTAS FRECUENTES

### ❓ ¿Por qué no veo mi cámara?

**R:** El navegador necesita permisos. Haz clic en el ícono de cámara en la barra de direcciones y selecciona "Permitir".

---

### ❓ ¿Funciona sin conexión a internet?

**R:** Sí, SmartVision funciona completamente offline. Solo necesitas internet para descargar las dependencias inicialmente.

---

### ❓ ¿Puede detectar más de un rostro?

**R:** Sí, puede detectar múltiples rostros simultáneamente. El límite práctico depende de tu hardware, pero funciona bien hasta 10-15 personas.

---

### ❓ ¿Se guardan las imágenes de mi cámara?

**R:** No. El sistema procesa los frames en memoria RAM y los descarta inmediatamente. No se guarda ningún video ni foto.

---

### ❓ ¿Por qué a veces no detecta mi rostro?

**Posibles razones:**
- Poca iluminación
- Ángulo muy lateral
- Rostro parcialmente cubierto (mascarilla, mano, cabello)
- Cámara de baja resolución

**Soluciones:**
- Mejora la iluminación
- Mira directo a la cámara
- Retírate objetos de la cara
- Ajusta el parámetro `conf` a 0.3 (más sensible)

---

### ❓ ¿Puedo usar el sistema en mi teléfono?

**R:** No directamente. El sistema requiere Python y Django que normalmente corren en computadoras. Sin embargo, si tienes el servidor en tu PC, puedes acceder desde el móvil en la misma red Wi-Fi usando la IP de tu PC.

---

### ❓ ¿Cómo detengo el sistema?

**R:** 
1. Ve a la terminal donde está corriendo
2. Presiona `Ctrl + C` (Windows/Linux) o `Cmd + C` (Mac)
3. Espera a que diga "Server stopped"
4. Cierra la terminal

---

## 9. SOLUCIÓN DE PROBLEMAS

### 🔧 Problema: "Servidor no inicia"

**Error típico:**
```
Error: That port is already in use.
```

**Solución:**
```bash
# Usa otro puerto
python manage.py runserver 8080

# Luego accede a:
http://localhost:8080
```

---

### 🔧 Problema: "Video negro o congelado"

**Posibles causas:**
- Otra aplicación está usando la cámara
- Permisos no otorgados
- Cámara desconectada

**Soluciones:**
1. Cierra otras apps que usen cámara (Zoom, Skype, etc.)
2. Revisa permisos del navegador
3. Verifica que la cámara funcione en otras apps
4. Reinicia el navegador

---

### 🔧 Problema: "FPS muy bajo (< 5)"

**Causas:**
- CPU sobrecargada
- Resolución muy alta
- Muchos rostros en escena

**Soluciones:**
1. Cierra otros programas
2. Reduce la resolución de la cámara
3. Actualiza drivers de la cámara
4. Considera usar una computadora más potente

---

### 🔧 Problema: "ModuleNotFoundError"

**Error típico:**
```
ModuleNotFoundError: No module named 'cv2'
```

**Solución:**
```bash
# Reinstala OpenCV
pip install --upgrade opencv-python
```

---

### 🔧 Problema: "Falsos positivos"

**Síntoma:** Detecta rostros donde no los hay

**Solución:**
```
# Aumenta el umbral de confianza
http://localhost:8000/video_feed?conf=0.7
```

Valores más altos = más estricto = menos falsos positivos

---

## 📞 SOPORTE Y CONTACTO

### 🆘 ¿Necesitas ayuda?

1. **Revisa esta guía primero** - La mayoría de problemas están cubiertos
2. **Consulta la documentación técnica** - Para detalles avanzados
3. **Busca en Issues de GitHub** - Puede que alguien ya resolvió tu problema
4. **Crea un nuevo Issue** - Describe tu problema detalladamente

### 📧 Información de Contacto

**Proyecto:** SmartVision  
**Repositorio:** https://github.com/tu-usuario/smartvision  
**Issues:** https://github.com/tu-usuario/smartvision/issues  
**Institución:** UNEMI

---

## 📝 NOTAS FINALES

### ✅ Checklist de Verificación

Antes de reportar un problema, verifica:

- [ ] Python 3.13+ instalado
- [ ] Todas las dependencias instaladas (`pip list`)
- [ ] Cámara funcionando en otras aplicaciones
- [ ] Permisos del navegador otorgados
- [ ] Puerto 8000 disponible
- [ ] Siguió todos los pasos de instalación

### 🎯 Próximos Pasos

Ahora que dominas SmartVision:

1. **Experimenta con parámetros** - Prueba diferentes valores de `conf`
2. **Intenta casos extremos** - ¿Qué pasa con 10 personas?
3. **Explora el código** - Revisa `detector/detectors.py` para aprender
4. **Contribuye** - Mejora el proyecto y comparte tus cambios

---

## 📚 GLOSARIO

- **FPS:** Frames Por Segundo - velocidad de procesamiento
- **Haar Cascade:** Algoritmo clásico de detección de rostros
- **MJPEG:** Motion JPEG - formato de streaming de video
- **Frame:** Una imagen individual de un video
- **Bounding Box:** Rectángulo que rodea un objeto detectado
- **Confidence:** Nivel de certeza de una detección (0.0 a 1.0)
- **OpenCV:** Librería de visión por computadora
- **Django:** Framework web de Python

---

**Manual generado:** 18 de Noviembre de 2025  
**Versión del sistema:** 1.0  
**Autor:** [Tu Nombre]  
**Para:** Usuario Final

**¡Disfruta usando SmartVision! 🎉**

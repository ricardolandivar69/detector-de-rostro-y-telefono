const stream = document.getElementById('stream');
const detectorSel = document.getElementById('detector');
const classesInp = document.getElementById('classes');
const confInp = document.getElementById('conf');
const applyBtn = document.getElementById('apply');
const badge = document.getElementById('current-detector');

function buildSrc() {
  const d = detectorSel.value;
  const params = new URLSearchParams();
  params.set('detector', d);
  if (d === 'yolo') {
    if (classesInp.value.trim()) params.set('classes', classesInp.value.trim());
    params.set('conf', confInp.value || '0.5');
  }
  badge.textContent = d;
  return '/video_feed?' + params.toString();
}

applyBtn.addEventListener('click', () => {
  stream.src = buildSrc();
});

// Permitir aplicar con Enter
classesInp.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') {
    e.preventDefault();
    stream.src = buildSrc();
  }
});

// 🔹 Actualización dinámica de FPS e indicadores
async function pollStats() {
  try {
    const r = await fetch('/stats');
    const j = await r.json();

    // FPS
    const fpsEl = document.getElementById('fps');
    if (fpsEl && j.fps !== undefined) {
      fpsEl.textContent = j.fps.toFixed(1);
    }

    // Indicadores de detección
    const chipsEl = document.getElementById('chips');
    if (chipsEl) {
      chipsEl.innerHTML = '';
      if (j.detections && j.detections.length > 0) {
        j.detections.forEach(det => {
          const span = document.createElement('span');
          span.className = 'chip';
          span.textContent = det;
          chipsEl.appendChild(span);
        });
      } else {
        chipsEl.innerHTML = '<span class="hint">Sin datos aún…</span>';
      }
    }
  } catch (e) {
    console.warn('Error al obtener stats', e);
  }

  setTimeout(pollStats, 800);
}

pollStats();

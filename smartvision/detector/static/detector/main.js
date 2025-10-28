const stream = document.getElementById('stream');
const detectorSel = document.getElementById('detector');
const classesInp = document.getElementById('classes');
const confInp = document.getElementById('conf');
const applyBtn = document.getElementById('apply');
const statsPre = document.getElementById('stats');
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

async function pollStats() {
  try {
    const r = await fetch('/stats');
    const j = await r.json();
    statsPre.textContent = JSON.stringify(j, null, 2);
  } catch (e) {}
  setTimeout(pollStats, 800);
}

pollStats();

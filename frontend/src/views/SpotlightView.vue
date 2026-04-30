<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const spotlightRef = ref<HTMLElement | null>(null)

const mouse = { x: 0.5, y: 0.5 }
const current = { x: 0.5, y: 0.5 }
let rafId = 0

function onPointerMove(e: PointerEvent) {
  mouse.x = e.clientX / window.innerWidth
  mouse.y = e.clientY / window.innerHeight
}

function animate() {
  current.x += (mouse.x - current.x) * 0.08
  current.y += (mouse.y - current.y) * 0.08

  if (spotlightRef.value) {
    const xPct = (current.x * 100).toFixed(2)
    const yPct = (current.y * 100).toFixed(2)
    spotlightRef.value.style.setProperty('--mx', xPct + '%')
    spotlightRef.value.style.setProperty('--my', yPct + '%')
  }

  rafId = requestAnimationFrame(animate)
}

onMounted(() => {
  window.addEventListener('pointermove', onPointerMove)
  rafId = requestAnimationFrame(animate)
})

onUnmounted(() => {
  window.removeEventListener('pointermove', onPointerMove)
  cancelAnimationFrame(rafId)
})
</script>

<template>
  <div ref="spotlightRef" class="spotlight-page">
    <!-- SVG noise filter (hidden) -->
    <svg class="noise-svg" xmlns="http://www.w3.org/2000/svg">
      <filter id="noise-filter">
        <feTurbulence
          type="fractalNoise"
          baseFrequency="0.65"
          numOctaves="4"
          stitchTiles="stitch"
        />
        <feColorMatrix type="saturate" values="0" />
      </filter>
      <rect width="100%" height="100%" filter="url(#noise-filter)" />
    </svg>

    <!-- Background grid dots -->
    <div class="grid-dots" />

    <!-- Main spotlight layer -->
    <div class="spotlight-glow" />

    <!-- Secondary softer ambient -->
    <div class="ambient-glow" />

    <!-- Content -->
    <div class="spotlight-content">
      <h1 class="title">Spotlight Effect</h1>
      <p class="subtitle">移动鼠标，体验聚光灯跟随效果</p>

      <div class="card-grid">
        <div class="demo-card">
          <div class="card-icon">01</div>
          <h3>径向渐变聚光</h3>
          <p>使用 radial-gradient + CSS 变量实现鼠标跟随光晕</p>
        </div>
        <div class="demo-card">
          <div class="card-icon">02</div>
          <h3>SVG 噪点纹理</h3>
          <p>feTurbulence 生成高质量程序化噪点，无需外部图片</p>
        </div>
        <div class="demo-card">
          <div class="card-icon">03</div>
          <h3>平滑插值</h3>
          <p>requestAnimationFrame + lerp 实现丝滑跟随动画</p>
        </div>
        <div class="demo-card">
          <div class="card-icon">04</div>
          <h3>多层叠加</h3>
          <p>聚光层 + 环境光层 + 噪点层 + 网格层组合</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.spotlight-page {
  position: relative;
  width: calc(100vw - var(--sidebar-width, 200px));
  height: 100vh;
  overflow: hidden;
  background: #0a0a0a;
  color: #e0e0e0;
  --mx: 50%;
  --my: 50%;
}

/* ─── SVG Noise Texture ─── */
.noise-svg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  opacity: 0.035;
  pointer-events: none;
  z-index: 4;
  mix-blend-mode: overlay;
}

/* ─── Grid Dots ─── */
.grid-dots {
  position: absolute;
  inset: 0;
  background-image: radial-gradient(circle, rgba(255, 255, 255, 0.07) 1px, transparent 1px);
  background-size: 32px 32px;
  z-index: 1;
}

/* ─── Main Spotlight ─── */
.spotlight-glow {
  position: absolute;
  inset: 0;
  background: radial-gradient(
    ellipse 650px 500px at var(--mx) var(--my),
    rgba(120, 160, 255, 0.12) 0%,
    rgba(80, 120, 220, 0.06) 30%,
    rgba(40, 60, 140, 0.02) 55%,
    transparent 70%
  );
  z-index: 2;
  pointer-events: none;
}

/* ─── Ambient Glow ─── */
.ambient-glow {
  position: absolute;
  inset: 0;
  background: radial-gradient(
    ellipse 900px 700px at var(--mx) var(--my),
    rgba(180, 200, 255, 0.04) 0%,
    transparent 60%
  );
  z-index: 2;
  pointer-events: none;
}

/* ─── Content ─── */
.spotlight-content {
  position: relative;
  z-index: 5;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  padding: 48px;
  pointer-events: none;
}

.title {
  font-size: 48px;
  font-weight: 800;
  letter-spacing: -1px;
  margin: 0;
  background: linear-gradient(135deg, #fff 0%, #a0b4ff 50%, #6e8cff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.45);
  margin-top: 12px;
  margin-bottom: 48px;
}

/* ─── Card Grid ─── */
.card-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  max-width: 640px;
  width: 100%;
  pointer-events: auto;
}

.demo-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 12px;
  padding: 24px;
  transition: border-color 0.3s, background 0.3s, box-shadow 0.3s, transform 0.2s;
}

.demo-card:hover {
  background: rgba(255, 255, 255, 0.06);
  border-color: rgba(160, 180, 255, 0.2);
  box-shadow: 0 0 40px -12px rgba(110, 140, 255, 0.15);
  transform: translateY(-2px);
}

.card-icon {
  font-size: 13px;
  font-weight: 700;
  color: rgba(160, 180, 255, 0.6);
  margin-bottom: 10px;
}

.demo-card h3 {
  font-size: 15px;
  font-weight: 600;
  margin: 0 0 6px;
  color: rgba(255, 255, 255, 0.85);
}

.demo-card p {
  font-size: 13px;
  margin: 0;
  color: rgba(255, 255, 255, 0.35);
  line-height: 1.5;
}
</style>

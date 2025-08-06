<template>
  <div
    ref="dropZone"
    class="upload-drop-zone"
    :class="{ 'error': isError, 'success': isSuccess }"
    @dragover.prevent="onDragOver"
    @dragleave.prevent="onDragLeave"
    @drop.prevent="onDrop"
  >
    <lottie-vue3
      v-if="isSuccess"
      :animationData="successAnimation"
      :loop="false"
      :autoplay="true"
      class="checkmark-animation"
    />
    <div v-else class="upload-content">
      <span class="upload-icon">📄</span>
      <span class="upload-text">Drag & drop your PDF here</span>
      <span v-if="fileName" class="file-name">{{ fileName }} ({{ fileSize }})</span>
      <div v-if="progress > 0" class="radial-progress">
        <svg viewBox="0 0 36 36">
          <path
            class="circle-bg"
            d="M18 2.0845
              a 15.9155 15.9155 0 0 1 0 31.831
              a 15.9155 15.9155 0 0 1 0 -31.831"
            fill="none"
            stroke="#eee"
            stroke-width="2"
          />
          <path
            class="circle"
            :stroke="COLORS.primary"
            d="M18 2.0845
              a 15.9155 15.9155 0 0 1 0 31.831
              a 15.9155 15.9155 0 0 1 0 -31.831"
            fill="none"
            stroke-width="2"
            :stroke-dasharray="progress + ', 100'"
          />
        </svg>
        <span class="progress-label">{{ Math.round(progress) }}%</span>
      </div>
      <div v-if="chunkCount > 0" class="chunk-counter">
        <transition name="flip">
          <span :key="chunkCount">Chunks: {{ chunkCount }}</span>
        </transition>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import gsap from 'gsap';
import { LottieVue3 } from 'vue3-lottie';
import successAnimation from '../../public/assets/lottie/success.json';
import { ANIMATION_TIMINGS, ANIMATION_EASING, COLORS } from '../animations.js';

const dropZone = ref(null);
const isError = ref(false);
const isSuccess = ref(false);
const fileName = ref('');
const fileSize = ref('');
const progress = ref(0);
const chunkCount = ref(0);

function onDragOver() {
  gsap.to(dropZone.value, {
    boxShadow: `0 0 20px 5px ${COLORS.primary}`,
    duration: ANIMATION_TIMINGS.prominent,
    ease: ANIMATION_EASING.entering,
  });
}
function onDragLeave() {
  gsap.to(dropZone.value, {
    boxShadow: 'none',
    duration: ANIMATION_TIMINGS.subtle,
    ease: ANIMATION_EASING.exiting,
  });
}
function onDrop(e) {
  const file = e.dataTransfer.files[0];
  if (!file || file.type !== 'application/pdf') {
    isError.value = true;
    gsap.fromTo(dropZone.value, { x: -10 }, {
      x: 10,
      repeat: 3,
      yoyo: true,
      duration: 0.1,
      onComplete: () => {
        gsap.to(dropZone.value, { x: 0 });
        isError.value = false;
      },
    });
    return;
  }
  isError.value = false;
  fileName.value = file.name;
  fileSize.value = (file.size / 1024).toFixed(1) + ' KB';
  simulateUpload();
}
function simulateUpload() {
  progress.value = 0;
  chunkCount.value = 0;
  isSuccess.value = false;
  const totalChunks = 5;
  let uploaded = 0;
  const interval = setInterval(() => {
    uploaded++;
    chunkCount.value = uploaded;
    progress.value = (uploaded / totalChunks) * 100;
    if (uploaded >= totalChunks) {
      clearInterval(interval);
      isSuccess.value = true;
      setTimeout(() => {
        isSuccess.value = false;
        progress.value = 0;
        chunkCount.value = 0;
        fileName.value = '';
        fileSize.value = '';
      }, 2000);
    }
  }, 500);
}

watch(isSuccess, (val) => {
  if (val) {
    gsap.to(dropZone.value, {
      boxShadow: `0 0 30px 10px ${COLORS.success}`,
      duration: ANIMATION_TIMINGS.prominent,
      ease: ANIMATION_EASING.standard,
    });
  } else {
    gsap.to(dropZone.value, {
      boxShadow: 'none',
      duration: ANIMATION_TIMINGS.subtle,
      ease: ANIMATION_EASING.exiting,
    });
  }
});
</script>

<style scoped>
.upload-drop-zone {
  border: 2px dashed #0056b3;
  border-radius: 16px;
  padding: 2rem;
  text-align: center;
  transition: box-shadow 0.3s cubic-bezier(0.4,0,0.2,1);
  background: #f8faff;
  position: relative;
  min-height: 200px;
  cursor: pointer;
}
.upload-drop-zone.error {
  border-color: #dd2c00;
  animation: error-flash 0.3s;
}
.upload-drop-zone.success {
  border-color: #00c853;
}
@keyframes error-flash {
  0% { background: #fff; }
  50% { background: #ffd6d6; }
  100% { background: #fff; }
}
.checkmark-animation {
  width: 80px;
  margin: 0 auto;
}
.radial-progress {
  width: 60px;
  height: 60px;
  margin: 1rem auto;
  position: relative;
}
.circle-bg {
  stroke: #eee;
}
.circle {
  stroke-linecap: round;
  transition: stroke-dasharray 0.5s cubic-bezier(0.4,0,0.2,1);
}
.progress-label {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-weight: bold;
  color: #0056b3;
}
.chunk-counter {
  margin-top: 1rem;
  font-size: 1.1rem;
  color: #7d3cff;
  font-weight: 600;
}
.flip-enter-active, .flip-leave-active {
  transition: transform 0.3s cubic-bezier(0.4,0,0.2,1);
}
.flip-enter-from, .flip-leave-to {
  transform: rotateX(90deg);
  opacity: 0;
}
</style> 
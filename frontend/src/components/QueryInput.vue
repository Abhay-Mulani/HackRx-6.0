<template>
  <div class="query-input-container">
    <form @submit.prevent="onSubmit">
      <textarea
        ref="inputField"
        v-model="query"
        class="query-textarea"
        :style="{ height: inputHeight + 'px' }"
        @input="autoResize"
        placeholder="Ask your insurance question..."
        aria-label="Query input"
      ></textarea>
      <div class="query-toolbar">
        <span class="token-counter">
          <transition name="flip">
            <span :key="tokenCount">{{ tokenCount }}</span>
          </transition>
          tokens
        </span>
        <button type="submit" class="submit-btn" :disabled="loading">
          <span v-if="!loading && !success && !error">Submit</span>
          <span v-if="loading">Loading...</span>
          <span v-if="success">✓</span>
          <span v-if="error">✗</span>
        </button>
      </div>
      <div class="syntax-highlighted" v-html="highlightedQuery"></div>
    </form>
    <div v-if="success" class="particle-burst"></div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue';
import gsap from 'gsap';
import { ANIMATION_TIMINGS, ANIMATION_EASING, COLORS } from '../animations.js';

const query = ref('');
const inputField = ref(null);
const inputHeight = ref(48);
const loading = ref(false);
const success = ref(false);
const error = ref(false);
const tokenCount = computed(() => query.value.split(/\s+/).filter(Boolean).length);

const insuranceTerms = [
  'premium', 'deductible', 'claim', 'policy', 'coverage', 'beneficiary', 'exclusion', 'endorsement', 'rider', 'underwriting'
];

const highlightedQuery = computed(() => {
  let text = query.value;
  insuranceTerms.forEach(term => {
    const regex = new RegExp(`\\b${term}\\b`, 'gi');
    text = text.replace(regex, `<span class='highlight-term'>${term}</span>`);
  });
  return text.replace(/\n/g, '<br>');
});

function autoResize() {
  nextTick(() => {
    inputHeight.value = inputField.value.scrollHeight;
  });
}

function onSubmit() {
  loading.value = true;
  error.value = false;
  success.value = false;
  setTimeout(() => {
    loading.value = false;
    if (query.value.toLowerCase().includes('error')) {
      error.value = true;
      gsap.fromTo(inputField.value, { x: -10 }, {
        x: 10,
        repeat: 3,
        yoyo: true,
        duration: 0.1,
        onComplete: () => gsap.to(inputField.value, { x: 0 })
      });
    } else {
      success.value = true;
      gsap.from('.particle-burst', {
        scale: 0.5,
        opacity: 0,
        duration: 0.6,
        ease: ANIMATION_EASING.entering
      });
      setTimeout(() => {
        success.value = false;
        query.value = '';
      }, 1500);
    }
  }, 1200);
}
</script>

<style scoped>
.query-input-container {
  background: #fff;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 2px 16px rgba(0,0,0,0.08);
  max-width: 600px;
  margin: 2rem auto;
}
.query-textarea {
  width: 100%;
  min-height: 48px;
  max-height: 200px;
  border: 2px solid #0056b3;
  border-radius: 8px;
  padding: 1rem;
  font-size: 1.1rem;
  transition: border-color 0.3s cubic-bezier(0.4,0,0.2,1);
  resize: none;
  outline: none;
}
.query-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 0.5rem;
}
.token-counter {
  font-family: monospace;
  color: #7d3cff;
  font-weight: bold;
  font-size: 1.1rem;
}
.flip-enter-active, .flip-leave-active {
  transition: transform 0.3s cubic-bezier(0.4,0,0.2,1);
}
.flip-enter-from, .flip-leave-to {
  transform: rotateX(90deg);
  opacity: 0;
}
.submit-btn {
  background: linear-gradient(90deg, #0056b3 60%, #7d3cff 100%);
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.5rem 1.5rem;
  font-weight: bold;
  font-size: 1rem;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}
.submit-btn:active {
  transform: scale(0.9);
}
.syntax-highlighted {
  margin-top: 1rem;
  min-height: 24px;
  font-size: 1rem;
}
.highlight-term {
  background: #e3e0ff;
  color: #7d3cff;
  border-radius: 4px;
  padding: 0 2px;
  font-weight: 600;
  box-shadow: 0 1px 4px #7d3cff22;
  animation: glow 1.2s infinite alternate;
}
@keyframes glow {
  from { box-shadow: 0 0 4px #7d3cff44; }
  to { box-shadow: 0 0 12px #7d3cffcc; }
}
.particle-burst {
  width: 100px;
  height: 100px;
  background: radial-gradient(circle, #00c853 60%, #fff0 100%);
  border-radius: 50%;
  position: absolute;
  left: 50%;
  top: 0;
  transform: translateX(-50%);
  pointer-events: none;
  z-index: 10;
}
</style> 
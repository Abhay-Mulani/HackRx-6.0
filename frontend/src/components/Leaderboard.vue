<template>
  <div class="leaderboard-container">
    <div class="flash-notification" v-if="showFlash">New submission!</div>
    <div class="leaderboard-list">
      <transition-group name="position" tag="div">
        <div
          v-for="(team, idx) in teams"
          :key="team.id"
          :class="['leaderboard-item', { 'user-team': team.isUser }]"
        >
          <span class="rank">{{ idx + 1 }}</span>
          <span class="team-name">{{ team.name }}</span>
          <span class="score">{{ team.score }}</span>
          <span v-if="team.isUser" class="trophy-placeholder">🏆</span>
        </div>
      </transition-group>
    </div>
    <div class="trophy-case">
      <!-- 3D trophy case placeholder (replace with Three.js or Lottie) -->
      <div class="trophy-3d">3D Trophy Case</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import gsap from 'gsap';
import { ANIMATION_TIMINGS, ANIMATION_EASING, COLORS } from '../animations.js';

const teams = ref([
  { id: 1, name: 'Alpha', score: 120, isUser: false },
  { id: 2, name: 'Bravo', score: 110, isUser: true },
  { id: 3, name: 'Charlie', score: 90, isUser: false },
]);
const showFlash = ref(false);

function simulateWebSocketUpdate() {
  // Simulate a new submission and position change
  showFlash.value = true;
  setTimeout(() => (showFlash.value = false), 1200);
  // Move user team up
  teams.value = [teams.value[1], teams.value[0], teams.value[2]];
}

onMounted(() => {
  setInterval(simulateWebSocketUpdate, 6000);
});
</script>

<style scoped>
.leaderboard-container {
  background: #fff;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 2px 16px rgba(0,0,0,0.08);
  max-width: 400px;
  margin: 2rem auto;
  position: relative;
}
.leaderboard-list {
  margin-bottom: 2rem;
}
.leaderboard-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 0.5rem;
  background: #f8faff;
  transition: box-shadow 0.3s cubic-bezier(0.4,0,0.2,1);
}
.leaderboard-item.user-team {
  border: 2px solid gold;
  box-shadow: 0 0 12px 2px gold;
  animation: pulse-gold 1.5s infinite;
}
@keyframes pulse-gold {
  0% { box-shadow: 0 0 12px 2px gold; }
  50% { box-shadow: 0 0 24px 6px gold; }
  100% { box-shadow: 0 0 12px 2px gold; }
}
.rank {
  font-weight: bold;
  color: #0056b3;
  width: 2rem;
}
.team-name {
  flex: 1;
  margin-left: 1rem;
}
.score {
  font-weight: 600;
  color: #7d3cff;
}
.trophy-placeholder {
  margin-left: 0.5rem;
  font-size: 1.5rem;
}
.trophy-case {
  text-align: center;
  margin-top: 1rem;
}
.trophy-3d {
  width: 100px;
  height: 100px;
  background: linear-gradient(135deg, #7d3cff 60%, #0056b3 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-weight: bold;
  font-size: 1.2rem;
  box-shadow: 0 4px 24px rgba(125,60,255,0.2);
}
.flash-notification {
  position: absolute;
  top: -1.5rem;
  left: 50%;
  transform: translateX(-50%);
  background: #ffab00;
  color: #fff;
  padding: 0.5rem 1.5rem;
  border-radius: 8px;
  font-weight: bold;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  animation: flash-in 0.5s cubic-bezier(0.4,0,0.2,1);
}
@keyframes flash-in {
  0% { opacity: 0; transform: translateX(-50%) scale(0.8); }
  100% { opacity: 1; transform: translateX(-50%) scale(1); }
}
.position-move {
  transition: transform 0.6s cubic-bezier(0.4,0,0.2,1);
}
</style> 
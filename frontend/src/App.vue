<template>
  <div class="app">
    <div class="content">
      <Quests 
        @switchToGame="activeGame = 'wordgame'"
        @switchToSapper="activeGame = 'sapper'"
        @switchToWheel="activeGame = 'wheel'"
        @switchToGoldChart="activeGame = 'goldchart'"
      />
    </div>

    <!-- Слово дня -->
    <div v-if="activeGame === 'wordgame'" class="game-overlay">
      <div class="game-header">
        <button class="back-btn" @click="activeGame = null">Назад</button>
        <h2>Слово дня</h2>
      </div>
      <WordGame @gameCompleted="activeGame = null" />
    </div>

    <!-- Сапёр -->
    <div v-if="activeGame === 'sapper'" class="game-overlay">
      <div class="game-header">
        <button class="back-btn" @click="activeGame = null">Назад</button>
        <h2>Сапёр</h2>
      </div>
      <SapperGame @gameCompleted="activeGame = null" />
    </div>

    <!-- Колесо фортуны -->
    <div v-if="activeGame === 'wheel'" class="game-overlay">
      <div class="game-header">
        <button class="back-btn" @click="activeGame = null">Назад</button>
        <h2>Колесо фортуны</h2>
      </div>
      <WheelGame @gameCompleted="activeGame = null" />
    </div>

    <!-- Трейдер золота -->
    <div v-if="activeGame === 'goldchart'" class="game-overlay">
      <div class="game-header">
        <button class="back-btn" @click="activeGame = null">Назад</button>
        <h2>Трейдер золота</h2>
      </div>
      <GoldChart @gameCompleted="activeGame = null" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Quests from './components/Quests.vue'
import WordGame from './components/WordGame.vue'
import SapperGame from './components/Sapper.vue'
import WheelGame from './components/Wheel.vue'
import GoldChart from './components/GoldChart.vue'

const activeGame = ref(null)
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  background: #f5f0e8;
  min-height: 100vh;
}

.app {
  max-width: 600px;
  margin: 0 auto;
  padding: 16px;
  min-height: 100vh;
}

.content {
  background: white;
  border-radius: 24px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.game-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: #f5f0e8;
  z-index: 100;
  overflow-y: auto;
  padding: 16px;
}

.game-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #cc0000;
}

.back-btn {
  background: #2c3e50;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 30px;
  cursor: pointer;
  font-weight: bold;
}

.game-header h2 {
  color: #cc0000;
  margin: 0;
}

@media (max-width: 480px) {
  .app {
    padding: 12px;
  }
  .content {
    padding: 16px;
  }
}
</style>
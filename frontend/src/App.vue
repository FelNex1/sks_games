<template>
  <div class="app">
    <!-- Основной контент -->
    <div class="content">
      <Quests 
        v-if="activeTab === 'kvesty'" 
        @switchToGame="activeTab = 'wordgame'"
        @switchToWheel="activeTab = 'wheel'"
        @switchToQuiz="activeTab = 'quiz'"
      />
      <WordGame v-if="activeTab === 'wordgame'" />
      <Quiz v-if="activeTab === 'quiz'" />
      <Wheel v-if="activeTab === 'wheel'" />
      <div v-else-if="activeTab !== 'kvesty' && activeTab !== 'wordgame' && activeTab !== 'quiz' && activeTab !== 'wheel'" class="placeholder">
        <div class="placeholder-icon">{{ activeIcon }}</div>
        <h2>{{ activeTitle }}</h2>
        <p>Функционал в разработке</p>
      </div>
    </div>

    <!-- Нижняя навигация -->
    <div class="bottom-nav">
      <button 
        v-for="item in navItems" 
        :key="item.id"
        @click="activeTab = item.id"
        :class="{ active: activeTab === item.id }"
        class="nav-btn"
      >
        <span class="nav-icon">{{ item.icon }}</span>
        <span class="nav-label">{{ item.label }}</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import Quests from './components/Quests.vue'
import WordGame from './components/WordGame.vue'
import Quiz from './components/Quiz.vue'
import Wheel from './components/Wheel.vue'

const activeTab = ref('kvesty')

const navItems = [
  { id: 'home', label: 'Главная' },
  { id: 'chats', label: 'Чаты' },
  { id: 'kvesty', label: 'Квесты' },
  { id: 'offices', label: 'Офисы' },
  { id: 'profile', label: 'Профиль' }
]

const activeTitle = computed(() => {
  const item = navItems.find(i => i.id === activeTab.value)
  return item ? item.label : ''
})

const activeIcon = computed(() => {
  const item = navItems.find(i => i.id === activeTab.value)
  return item ? item.icon : ''
})
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
  height: 100vh;
  overflow: hidden;
}

.app {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 500px;
  margin: 0 auto;
  background: #f5f0e8;
  position: relative;
}

.content {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  padding-bottom: 80px;
}

.placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
  color: #888;
}

.placeholder-icon {
  font-size: 64px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.placeholder h2 {
  font-size: 20px;
  color: #cc0000;
  margin-bottom: 8px;
}

.placeholder p {
  font-size: 14px;
  color: #999;
}

.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  max-width: 500px;
  margin: 0 auto;
  background: white;
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 8px 16px 16px;
  border-top: 1px solid #eee;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
  z-index: 100;
}

.nav-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 30px;
  transition: all 0.2s;
  flex: 1;
}

.nav-icon {
  font-size: 24px;
}

.nav-label {
  font-size: 11px;
  color: #888;
  font-weight: 500;
}

.nav-btn.active .nav-icon {
  color: #cc0000;
}

.nav-btn.active .nav-label {
  color: #cc0000;
}

.nav-btn:active {
  transform: scale(0.95);
}

.content::-webkit-scrollbar {
  width: 4px;
}

.content::-webkit-scrollbar-track {
  background: #eee;
  border-radius: 4px;
}

.content::-webkit-scrollbar-thumb {
  background: #cc0000;
  border-radius: 4px;
}

@media (max-width: 480px) {
  .content {
    padding: 12px;
    padding-bottom: 70px;
  }
  
  .nav-label {
    font-size: 10px;
  }
  
  .nav-icon {
    font-size: 22px;
  }
  
  .bottom-nav {
    padding: 6px 12px 12px;
  }
}
</style>
<template>
  <div class="sapper-container">
    <h2>Сапёр</h2>
    <p class="desc">Открывай клетки, не наступи на мину</p>

    <div class="game-info">
      <div class="info-card">
        <span class="label">💎 Алмазы</span>
        <span class="value">{{ diamondsCount }}</span>
      </div>
      <div class="info-card">
        <span class="label">💣 Мины</span>
        <span class="value">{{ bombsCount }} / {{ totalMines }}</span>
      </div>
    </div>

    <div class="ceils-container">
      <div 
        v-for="ceil in ceils" 
        :key="ceil.id" 
        class="ceil" 
        :class="{ opened: ceil.opened }"
        @click="onCeilOpen(ceil)"
      >
        <span v-if="ceil.opened && ceil.value === 'diamond'" class="emoji">💎</span>
        <span v-if="ceil.opened && ceil.value === 'bomb'" class="emoji">💣</span>
        <span v-if="!ceil.opened" class="closed">?</span>
      </div>
    </div>

    <div v-if="gameOver" class="message" :class="{ error: !gameWon, success: gameWon }">
      {{ gameWon ? '🎉 Поздравляем! Вы выиграли!' : '💀 Вы наступили на мину!' }}
    </div>

    <button @click="initGame" class="reset-btn">Новая игра</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const emit = defineEmits(['gameCompleted'])

// Константы
const SIZE = 5  // 5x5 = 25 клеток
const TOTAL_CELLS = SIZE * SIZE
const BOMB_PROBABILITY = 0.2  // 20% бомба, 80% алмаз
const TOTAL_MINES = Math.floor(TOTAL_CELLS * BOMB_PROBABILITY)  // 5 мин

// Данные
const ceils = ref([])
const bombsCount = ref(0)
const diamondsCount = ref(0)
const gameOver = ref(false)
const gameWon = ref(false)
const openedCount = ref(0)
const totalMines = ref(TOTAL_MINES)

// Инициализация поля (все клетки закрыты)
const initGame = () => {
  gameOver.value = false
  gameWon.value = false
  bombsCount.value = 0
  diamondsCount.value = 0
  openedCount.value = 0
  
  // Создаём закрытое поле
  const newCeils = []
  for (let i = 0; i < TOTAL_CELLS; i++) {
    newCeils.push({ 
      id: i, 
      value: null,      // 'diamond', 'bomb' (определится при открытии)
      opened: false
    })
  }
  
  ceils.value = newCeils
}

// Открытие клетки
const onCeilOpen = (ceil) => {
  if (gameOver.value) return
  if (ceil.opened) return
  
  // Генерируем результат только при первом открытии
  if (ceil.value === null) {
    const randWeight = Math.random()
    if (randWeight < BOMB_PROBABILITY) {
      ceil.value = 'bomb'
      bombsCount.value++
      gameOver.value = true
      gameWon.value = false
      ceil.opened = true
      alert('💣 Вы наступили на мину! Игра окончена.')
      return
    } else {
      ceil.value = 'diamond'
      diamondsCount.value++
    }
  }
  
  ceil.opened = true
  openedCount.value++
  
  // Проверка победы (все клетки открыты ИЛИ все алмазы собраны)
  const allOpened = openedCount.value >= TOTAL_CELLS
  const maxDiamonds = TOTAL_CELLS - TOTAL_MINES
  const allDiamondsFound = diamondsCount.value >= maxDiamonds
  
  if (allOpened || allDiamondsFound) {
    gameOver.value = true
    gameWon.value = true
    
    let balance = localStorage.getItem('sks_balance')
    balance = balance ? parseInt(balance) : 350
    const bonus = diamondsCount.value * 5
    balance += bonus
    localStorage.setItem('sks_balance', balance)
    alert(`🎉 Поздравляем! Вы выиграли ${bonus} бонусов! Баланс: ${balance}`)
    
    if (window.completeSapperQuest) {
      window.completeSapperQuest()
    }
    emit('gameCompleted')
  }
}

onMounted(() => {
  initGame()
})
</script>

<style scoped>
.sapper-container {
  text-align: center;
  padding: 20px;
}

h2 {
  color: #cc0000;
  font-size: 24px;
  margin-bottom: 5px;
}

.desc {
  color: #666;
  font-size: 14px;
  margin-bottom: 20px;
}

.game-info {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 20px;
}

.info-card {
  background: #f0f0f0;
  border-radius: 12px;
  padding: 8px 20px;
}

.info-card .label {
  font-size: 12px;
  color: #666;
  display: block;
}

.info-card .value {
  font-size: 24px;
  font-weight: bold;
  color: #cc0000;
}

.ceils-container {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  justify-content: center;
  max-width: 350px;
  margin: 0 auto;
}

.ceil {
  width: 60px;
  height: 60px;
  background-color: #bbb;
  border: 3px solid #2c3e50;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.1s;
}

.ceil:hover {
  transform: scale(1.02);
  background-color: #aaa;
}

.ceil.opened {
  background-color: #eee;
  cursor: default;
}

.ceil.opened:hover {
  transform: none;
}

.emoji {
  font-size: 32px;
}

.closed {
  font-size: 24px;
  font-weight: bold;
  color: #2c3e50;
}

.message {
  padding: 12px;
  border-radius: 10px;
  margin: 15px 0;
  font-weight: bold;
}

.message.error {
  background: #cc0000;
  color: white;
}

.message.success {
  background: #2ecc71;
  color: white;
}

.reset-btn {
  padding: 10px 24px;
  background: #2c3e50;
  color: white;
  border: none;
  border-radius: 30px;
  cursor: pointer;
  font-weight: bold;
  margin-top: 10px;
}

.reset-btn:hover {
  background: #1a252f;
}

@media (max-width: 480px) {
  .ceil {
    width: 50px;
    height: 50px;
  }
  .emoji {
    font-size: 28px;
  }
  .closed {
    font-size: 20px;
  }
  .ceils-container {
    gap: 6px;
  }
}
</style>
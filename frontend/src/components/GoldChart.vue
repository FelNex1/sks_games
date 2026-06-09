<template>
  <div class="game-container">
    <h2 class="text-center">Трейдер золота</h2>
    <p class="text-center text-secondary">Цена упадёт или вырастет?</p>

    <!-- Статистика -->
    <div class="stats">
      <div class="stat-card">
        <span class="stat-label">Жизни</span>
        <span class="stat-value" :class="{ warning: lives <= 2 }">{{ lives }}</span>
      </div>
      <div class="stat-card">
        <span class="stat-label">Серия</span>
        <span class="stat-value">{{ streak }}</span>
      </div>
      <div class="stat-card">
        <span class="stat-label">Бонусы</span>
        <span class="stat-value">+{{ totalBonus }}</span>
      </div>
    </div>

    <!-- График -->
    <canvas ref="chartCanvas" width="300" height="150" class="chart"></canvas>

    <div class="current-price">
      Текущая цена: <strong>{{ currentPrice }}</strong> руб/г
    </div>

    <div class="buttons" v-if="!gameOver && !gameWon">
      <button @click="predict('up')" class="btn-up">Цена вырастет ↑</button>
      <button @click="predict('down')" class="btn-down">Цена упадёт ↓</button>
    </div>

    <div v-if="gameWon" class="message success">
      Поздравляем! Ты выиграл +{{ totalBonus }} бонусов
    </div>
    <div v-if="gameOver && !gameWon" class="message error">
      Ты банкрот! Заработано: +{{ totalBonus }} бонусов
    </div>

    <button @click="resetGame" class="btn-reset">Новая игра</button>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const emit = defineEmits(['gameCompleted'])

const chartCanvas = ref(null)
let ctx = null

// Игровые переменные
const lives = ref(3)           // Стартовые 5 жизней
const streak = ref(0)          // Серия правильных ответов
const totalBonus = ref(0)      // Накопленные бонусы
const gameOver = ref(false)
const gameWon = ref(false)

// График
let chartData = []
let currentIndex = 0
const currentPrice = ref(2750)  // Стартовая цена

// Генерация случайного графика (от 2500 до 3000)
const generateRandomWalk = () => {
  let price = 2750
  chartData = [price]
  for (let i = 0; i < 9; i++) {
    // Рандомный шаг: -30, -20, -10, +10, +20, +30
    const step = [ -50,-40,-30, -20, -10, 10, 20, 30,40,50 ][Math.floor(Math.random() * 6)]
    price = price + step
    // Ограничиваем диапазон 2500-3000
    price = Math.max(2500, Math.min(3000, price))
    chartData.push(price)
  }
}

// Отрисовка графика
const drawChart = () => {
  if (!ctx || chartData.length < 2) return
  
  const width = 300, height = 150
  ctx.clearRect(0, 0, width, height)
  
  const minPrice = 2500
  const maxPrice = 3000
  const range = maxPrice - minPrice
  
  ctx.beginPath()
  ctx.strokeStyle = '#cc0000'
  ctx.lineWidth = 2
  
  for (let i = 0; i <= currentIndex + 1; i++) {
    const x = (i / 9) * width
    const y = height - ((chartData[i] - minPrice) / range) * (height - 20) - 10
    if (i === 0) ctx.moveTo(x, y)
    else ctx.lineTo(x, y)
  }
  ctx.stroke()
  
  // Последняя точка
  const lastX = ((currentIndex + 1) / 9) * width
  const lastY = height - ((chartData[currentIndex + 1] - minPrice) / range) * (height - 20) - 10
  ctx.fillStyle = '#cc0000'
  ctx.beginPath()
  ctx.arc(lastX, lastY, 5, 0, 2 * Math.PI)
  ctx.fill()
  ctx.fillStyle = 'white'
  ctx.beginPath()
  ctx.arc(lastX, lastY, 2, 0, 2 * Math.PI)
  ctx.fill()
  
  // Линия текущей цены
  const lineY = height - ((currentPrice.value - minPrice) / range) * (height - 20) - 10
  ctx.beginPath()
  ctx.strokeStyle = '#aaa'
  ctx.setLineDash([5, 5])
  ctx.moveTo(0, lineY)
  ctx.lineTo(width, lineY)
  ctx.stroke()
  ctx.setLineDash([])
}

// Следующий шаг графика
const nextStep = () => {
  currentIndex++
  currentPrice.value = chartData[currentIndex]
  drawChart()
}

// Проверка прогноза
const predict = (direction) => {
  if (gameOver.value || gameWon.value) return
  
  const nextPrice = chartData[currentIndex + 1]
  const isUp = nextPrice > currentPrice.value
  
  if ((direction === 'up' && isUp) || (direction === 'down' && !isUp)) {
    // Правильный прогноз
    streak.value++
    const addBonus = 2
    totalBonus.value += addBonus
    
    if (currentIndex + 2 >= chartData.length) {
      // Победа — прошли весь график
      gameWon.value = true
      gameOver.value = true
      
      let balance = localStorage.getItem('sks_balance')
      balance = balance ? parseInt(balance) : 350
      balance += totalBonus.value
      localStorage.setItem('sks_balance', balance)
      
      emit('gameCompleted')
      alert('+' + totalBonus.value + ' бонусов! Баланс: ' + balance)
    } else {
      nextStep()
    }
  } else {
    // Неправильный прогноз
    lives.value -= 1
    streak.value = 0
    
    if (lives.value <= 0) {
      gameOver.value = true
      
      let balance = localStorage.getItem('sks_balance')
      balance = balance ? parseInt(balance) : 350
      balance += totalBonus.value
      localStorage.setItem('sks_balance', balance)
      
      emit('gameCompleted')
      alert('Ты банкрот! +' + totalBonus.value + ' бонусов! Баланс: ' + balance)
    } else {
      nextStep()
    }
  }
}

// Сброс игры
const resetGame = () => {
  generateRandomWalk()
  currentIndex = 0
  currentPrice.value = chartData[0]
  lives.value = 5
  streak.value = 0
  totalBonus.value = 0
  gameOver.value = false
  gameWon.value = false
  
  if (ctx) drawChart()
}

onMounted(() => {
  if (chartCanvas.value) {
    ctx = chartCanvas.value.getContext('2d')
  }
  resetGame()
})

onUnmounted(() => {
  if (ctx) ctx.clearRect(0, 0, 300, 150)
})
</script>

<style scoped>
.game-container {
  text-align: center;
  padding: 10px;
}

.stats {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 20px;
}

.stat-card {
  background: #f0f0f0;
  border-radius: 12px;
  padding: 8px 16px;
  min-width: 80px;
}

.stat-label {
  font-size: 11px;
  color: #666;
  display: block;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #1a1a1a;
}

.stat-value.warning {
  color: #cc0000;
}

.chart {
  background: #fafafa;
  border: 1px solid #ddd;
  border-radius: 8px;
  margin-bottom: 15px;
}

.current-price {
  font-size: 18px;
  margin-bottom: 20px;
}

.current-price strong {
  color: #cc0000;
  font-size: 24px;
}

.buttons {
  display: flex;
  gap: 15px;
  justify-content: center;
  margin-bottom: 20px;
}

.btn-up, .btn-down {
  padding: 10px 20px;
  font-size: 14px;
  font-weight: bold;
  border: none;
  border-radius: 30px;
  cursor: pointer;
}

.btn-up {
  background: #2ecc71;
  color: white;
}

.btn-up:hover {
  background: #27ae60;
}

.btn-down {
  background: #e74c3c;
  color: white;
}

.btn-down:hover {
  background: #c0392b;
}

.message {
  padding: 12px;
  border-radius: 10px;
  margin-bottom: 15px;
  font-weight: bold;
}

.message.success {
  background: #2ecc71;
  color: white;
}

.message.error {
  background: #cc0000;
  color: white;
}

.btn-reset {
  padding: 8px 20px;
  background: #2c3e50;
  color: white;
  border: none;
  border-radius: 30px;
  cursor: pointer;
  font-weight: bold;
}

.btn-reset:hover {
  background: #1a252f;
}

.text-center {
  text-align: center;
}

.text-secondary {
  color: #666;
}
</style>
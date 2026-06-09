<template>
  <div class="roller-container">
    <h2>Колесо фортуны</h2>
    <p class="desc">Покрути ленту и получи приз</p>

    <div class="roller">
      <div class="blur left"></div>
      <div class="blur right"></div>
      
      <div class="prizes-list" ref="prizesContainer">
        <div 
          v-for="prize in extendedPrizes" 
          :key="prize.id" 
          class="prize-item"
        >
          <div class="prize-content">
            <span class="prize-value">{{ prize.name }}</span>
            <span v-if="prize.value > 0" class="prize-bonus">+{{ prize.value }}</span>
          </div>
        </div>
      </div>
    </div>
    
    <button class="spin-button" @click="spin" :disabled="isSpinning">
      {{ isSpinning ? 'Крутится...' : 'Вращать!' }}
    </button>

    <div v-if="lastPrize" class="result" :class="lastPrize.type">
      <p>Выпало: {{ lastPrize.name }}</p>
      <p v-if="lastPrize.value > 0">+{{ lastPrize.value }} бонусов</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const emit = defineEmits(['gameCompleted'])

const prizesContainer = ref(null)
const isSpinning = ref(false)
const lastPrize = ref(null)

// Призы
const prizes = ref([
  { id: 1, name: '10 бонусов', value: 10, type: 'points' },
  { id: 2, name: '20 бонусов', value: 20, type: 'points' },
  { id: 3, name: '50 бонусов', value: 50, type: 'points' },
  { id: 4, name: '100 бонусов', value: 100, type: 'points' },
  { id: 5, name: '5 бонусов', value: 5, type: 'points' },
  { id: 6, name: '2 бонуса', value: 2, type: 'points' },
  { id: 7, name: 'Скидка 5%', value: 5, type: 'discount' },
  { id: 8, name: 'Скидка 10%', value: 10, type: 'discount' },
  { id: 9, name: 'Алмаз', value: 0, type: 'item' },
  { id: 10, name: 'Спасибо', value: 0, type: 'nothing' },
])

const extendedPrizes = ref([])

// Создаём длинную ленту (повторяем призы 3 раза)
const createExtendedList = () => {
  const extended = []
  for (let i = 0; i < 3; i++) {
    prizes.value.forEach(prize => {
      extended.push({
        ...prize,
        id: extended.length + 1
      })
    })
  }
  return extended
}

// Начисление награды
const awardPrize = (prize) => {
  if (prize.type === 'points' && prize.value > 0) {
    let balance = localStorage.getItem('sks_balance')
    balance = balance ? parseInt(balance) : 350
    balance += prize.value
    localStorage.setItem('sks_balance', balance)
    alert(`Вы выиграли ${prize.name}! Баланс: ${balance}`)
  } else if (prize.type === 'discount') {
    localStorage.setItem('sks_discount', String(prize.value))
    alert(`Вы выиграли ${prize.name}! Скидка сохранена`)
  } else if (prize.type === 'item') {
    alert(`Вы выиграли ${prize.name}! Предмет добавлен в коллекцию`)
  } else {
    alert(`Выпало: ${prize.name}`)
  }
  
  if (window.completeWheelQuest) {
    window.completeWheelQuest()
  }
  emit('gameCompleted')
}

// Вращение
let spinTimeout = null

function spin() {
  if (isSpinning.value) return
  
  // Очищаем предыдущий таймаут, если есть
  if (spinTimeout) clearTimeout(spinTimeout)
  
  isSpinning.value = true
  lastPrize.value = null
  
  if (!prizesContainer.value) return
  
  const itemCount = prizesContainer.value.children.length
  const randomIndex = Math.floor(Math.random() * itemCount)
  const targetElement = prizesContainer.value.children[randomIndex]
  
  // Плавная прокрутка к выбранному призу
  targetElement.scrollIntoView({
    behavior: 'smooth',
    block: 'nearest',
    inline: 'center'
  })
  
  // После остановки анимации начисляем награду
  spinTimeout = setTimeout(() => {
    isSpinning.value = false
    const selectedPrize = extendedPrizes.value[randomIndex]
    lastPrize.value = selectedPrize
    awardPrize(selectedPrize)
    spinTimeout = null
  }, 800)
}

onMounted(() => {
  extendedPrizes.value = createExtendedList()
  
  setTimeout(() => {
    if (prizesContainer.value && prizesContainer.value.children.length > 0) {
      const centerIndex = Math.floor(prizesContainer.value.children.length / 2)
      const centerElement = prizesContainer.value.children[centerIndex]
      centerElement.scrollIntoView({
        behavior: 'auto',
        inline: 'center'
      })
    }
  }, 100)
})
</script>

<style scoped>
.roller-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  box-sizing: border-box;
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
  margin-bottom: 10px;
}

.roller {
  position: relative;
  width: 100%;
  max-width: 500px;
  height: 100px;
  background-color: #f5f5f5;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.roller .blur {
  position: absolute;
  top: 0;
  width: 60px;
  height: 100%;
  pointer-events: none;
  z-index: 2;
}

.roller .blur.left {
  left: 0;
  background: linear-gradient(to right, rgba(245, 245, 245, 0.95), transparent);
}

.roller .blur.right {
  right: 0;
  background: linear-gradient(to left, rgba(245, 245, 245, 0.95), transparent);
}

.prizes-list {
  display: flex;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  scroll-behavior: smooth;
  height: 100%;
  gap: 0;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.prizes-list::-webkit-scrollbar {
  display: none;
}

.prize-item {
  flex-shrink: 0;
  scroll-snap-align: center;
  width: 100px;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.prize-content {
  text-align: center;
  background: white;
  border-radius: 12px;
  padding: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  min-width: 80px;
}

.prize-value {
  font-size: 14px;
  font-weight: bold;
  color: #cc0000;
  display: block;
}

.prize-bonus {
  font-size: 12px;
  color: #666;
  display: block;
}

.spin-button {
  z-index: 3;
  padding: 10px 28px;
  font-size: 16px;
  font-weight: 600;
  color: white;
  background: linear-gradient(135deg, #cc0000, #8b0000);
  border: none;
  border-radius: 40px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.spin-button:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(204, 0, 0, 0.3);
}

.spin-button:disabled {
  opacity: 0.5;
}

.result {
  margin-top: 15px;
  padding: 12px;
  border-radius: 12px;
  text-align: center;
}

.result.points {
  background: #2ecc71;
  color: white;
}

.result.discount {
  background: #f39c12;
  color: white;
}

.result.item {
  background: #9b59b6;
  color: white;
}

.result.nothing {
  background: #95a5a6;
  color: white;
}

@media (max-width: 768px) {
  .roller {
    height: 80px;
  }
  .roller .blur {
    width: 40px;
  }
  .prize-item {
    width: 80px;
  }
  .spin-button {
    padding: 8px 22px;
    font-size: 14px;
  }
}
</style>
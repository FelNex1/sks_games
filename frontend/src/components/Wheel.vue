<template>
  <div>
    <h2>Колесо фортуны</h2>
    <p>1 раз в день — бесплатно!</p>

    <div class="wheel-container">
      <div class="wheel" :style="{ transform: `rotate(${rotation}deg)` }">
        <div v-for="(prize, idx) in prizes" :key="idx" class="sector" :style="{ transform: `rotate(${idx * 60}deg)` }">
          {{ prize.icon }}
        </div>
      </div>
    </div>

    <div class="controls">
      <button @click="handleSpin" :disabled="isSpinning || !canSpinToday">
        Крутить ({{ canSpinToday ? 'бесплатно' : 'завтра' }})
      </button>
      <p v-if="lastPrize" class="result">Выпало: {{ lastPrize }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getWheelStatus, spinWheel } from '../api'

const rotation = ref(0)
const isSpinning = ref(false)
const lastPrize = ref('')
const canSpinToday = ref(true)

const prizes = [
  { icon: '6', name: '10 бонусов', value: 10 },
  { icon: '5', name: '50 бонусов', value: 50 },
  { icon: '4', name: '100 бонусов', value: 100 },
  { icon: '3', name: 'Скидка 0.5%', value: 0 },
  { icon: '2', name: 'Бесплатный квест', value: 0 },
  { icon: '1', name: 'Редкий бейдж', value: 0 },
]

const loadStatus = async () => {
  try {
    const res = await getWheelStatus()
    canSpinToday.value = res.data.can_spin
  } catch (error) {
    console.error('Ошибка загрузки статуса колеса:', error)
  }
}

const handleSpin = async () => {
  if (isSpinning.value || !canSpinToday.value) return
  
  isSpinning.value = true
  
  try {
    const res = await spinWheel()
    const prize = res.data.prize
    lastPrize.value = prize.name
    
    const sectorSize = 360 / prizes.length
    const prizeIndex = prizes.findIndex(p => p.name === prize.name)
    const targetAngle = prizeIndex * sectorSize
    const spins = 1440 + targetAngle
    rotation.value += spins
    
    setTimeout(() => {
      isSpinning.value = false
      canSpinToday.value = false
      alert(`🎉 Ты выиграл ${prize.name}!`)
      
      // Вызываем завершение квеста
      if (window.completeWheelQuest) {
        window.completeWheelQuest()
      }
    }, 2000)
  } catch (error) {
    isSpinning.value = false
    alert('Ошибка при вращении колеса')
  }
}

onMounted(loadStatus)
</script>

<style scoped>
.wheel-container { display: flex; justify-content: center; margin: 20px 0; cursor: pointer; }
.wheel { width: 250px; height: 250px; border-radius: 50%; background: conic-gradient(#f39c12, #e67e22, #f1c40f, #e67e22); position: relative; transition: transform 2s ease-out; box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
.sector { position: absolute; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; font-size: 28px; }
.controls { text-align: center; }
.result { background: #2c3e50; color: white; padding: 10px; border-radius: 30px; margin: 15px 0; }
button { background: #e67e22; padding: 12px 30px; font-size: 18px; border: none; border-radius: 30px; color: white; font-weight: bold; cursor: pointer; }
button:disabled { opacity: 0.5; }
</style>
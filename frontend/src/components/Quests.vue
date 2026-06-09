<template>
  <div>
    <div class="reset-header">
      <h2 class="section-title">Ежедневные задания</h2>
      <button @click="resetAllQuests" class="reset-all-btn">Сбросить все</button>
    </div>
    <p class="hint">Выполняй задания и получай бонусы</p>

    <div class="quest-list">
      <div 
        v-for="quest in quests" 
        :key="quest.id" 
        class="quest-card"
        :class="{ 
          completed: quest.completed,
          selected: selectedQuest === quest.id 
        }"
        @click="selectQuest(quest.id)"
      >
        <div class="quest-info">
          <h3>{{ quest.title }}</h3>
          <p>{{ quest.description }}</p>
          <div class="quest-meta">
            <span class="reward">+{{ quest.reward }} бонусов</span>
            <span v-if="quest.weekly === 1" class="weekly-tag">Еженедельный</span>
            <span v-else-if="quest.cooldown_days > 1" class="three-day-tag">Раз в {{ quest.cooldown_days }} дня</span>
            <span v-else class="daily-tag">Ежедневный</span>
          </div>
          <div v-if="quest.completed" class="completed-badge">
            Выполнено
          </div>
        </div>
        <button 
          @click.stop="startQuest(quest.id)"
          :disabled="quest.completed"
          :class="{ completed: quest.completed }"
        >
          {{ quest.completed ? 'Выполнено' : 'Выполнить' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const emit = defineEmits(['switchToGame', 'switchToSapper', 'switchToWheel', 'switchToGoldChart'])

const selectedQuest = ref(null)
const quests = ref([])

const selectQuest = (id) => {
  selectedQuest.value = id
  setTimeout(() => {
    if (selectedQuest.value === id) {
      selectedQuest.value = null
    }
  }, 2000)
}

// Сброс всех квестов
const resetAllQuests = () => {
  if (confirm('Сбросить все квесты? Прогресс будет потерян.')) {
    for (let i = 0; i < quests.value.length; i++) {
      quests.value[i].completed = false
    }
    localStorage.setItem('sks_quests', JSON.stringify(quests.value))
    alert('Все квесты сброшены!')
  }
}

const loadQuests = () => {
  const saved = localStorage.getItem('sks_quests')
  const defaultQuests = [
    { id: 1, title: 'Слово дня', description: 'Угадай слово из 5 букв', reward: 30, type: 'wordgame', weekly: 0, cooldown_days: 1, completed: false },
    { id: 2, title: 'Сапёр', description: 'Найди все алмазы и не наступи на мину', reward: 25, type: 'sapper', weekly: 0, cooldown_days: 3, completed: false },
    { id: 3, title: 'Колесо фортуны', description: 'Покрути колесо и получи приз', reward: 25, type: 'wheel', weekly: 1, cooldown_days: 7, completed: false },
    { id: 4, title: 'Трейдер золота', description: 'Угадай движение цены золота', reward: 25, type: 'goldchart', weekly: 0, cooldown_days: 1, completed: false }
  ]
  
  if (saved) {
    const parsed = JSON.parse(saved)
    for (let i = 0; i < defaultQuests.length; i++) {
      defaultQuests[i].completed = parsed[i]?.completed || false
    }
  }
  quests.value = defaultQuests
}

const completeRegularQuest = async (questId) => {
  const quest = quests.value.find(q => q.id === questId)
  if (quest.completed) return
  
  quest.completed = true
  
  let currentBalance = localStorage.getItem('sks_balance')
  currentBalance = currentBalance ? parseInt(currentBalance) : 350
  currentBalance += quest.reward
  localStorage.setItem('sks_balance', currentBalance)
  localStorage.setItem('sks_quests', JSON.stringify(quests.value))
  
  alert(`Квест выполнен! +${quest.reward} бонусов! Баланс: ${currentBalance}`)
}

const startQuest = (questId) => {
  const quest = quests.value.find(q => q.id === questId)
  if (quest.completed) return
  
  switch(quest.type) {
    case 'wordgame':
      emit('switchToGame')
      break
    case 'sapper':
      emit('switchToSapper')
      break
    case 'wheel':
      emit('switchToWheel')
      break
    case 'goldchart':
      emit('switchToGoldChart')
      break
    default:
      completeRegularQuest(questId)
  }
}

window.completeWordGameQuest = async () => {
  const quest = quests.value.find(q => q.id === 1)
  if (quest && !quest.completed) {
    await completeRegularQuest(1)
  }
}

window.completeSapperQuest = async () => {
  const quest = quests.value.find(q => q.id === 2)
  if (quest && !quest.completed) {
    await completeRegularQuest(2)
  }
}

window.completeWheelQuest = async () => {
  const quest = quests.value.find(q => q.id === 3)
  if (quest && !quest.completed) {
    await completeRegularQuest(3)
  }
}

window.completeGoldChartQuest = async () => {
  const quest = quests.value.find(q => q.id === 4)
  if (quest && !quest.completed) {
    await completeRegularQuest(4)
  }
}

onMounted(loadQuests)
</script>

<style scoped>
.reset-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
}

.section-title {
  color: #cc0000;
  font-size: 20px;
  text-align: center;
  margin-bottom: 5px;
  font-weight: bold;
  flex: 1;
}

.reset-all-btn {
  background: #2c3e50;
  color: white;
  border: none;
  padding: 5px 12px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 11px;
  font-weight: bold;
}

.reset-all-btn:hover {
  background: #1a252f;
}

.hint {
  text-align: center;
  font-size: 12px;
  color: #888;
  margin-bottom: 15px;
}

.quest-list { 
  display: flex; 
  flex-direction: column; 
  gap: 10px; 
}

.quest-card { 
  background: white; 
  border-radius: 12px; 
  padding: 12px; 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  flex-wrap: wrap; 
  gap: 10px;
  border: 1px solid #ddd;
  cursor: pointer;
  transition: background 0.1s;
}

.quest-card.selected {
  background: #ffe0e0;
  border-color: #cc0000;
}

.quest-card.completed {
  background: #f5f5f5;
  opacity: 0.8;
}

.quest-info { 
  flex: 1;
}

.quest-info h3 { 
  font-size: 15px; 
  margin-bottom: 4px;
  color: #333;
}

.quest-info p { 
  font-size: 11px; 
  color: #888; 
  margin-bottom: 8px; 
}

.quest-meta {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
}

.reward { 
  background: #cc0000; 
  color: white; 
  padding: 3px 10px; 
  border-radius: 15px; 
  font-size: 11px; 
  font-weight: bold; 
}

.weekly-tag {
  background: #ffe0e0;
  color: #cc0000;
  padding: 2px 8px;
  border-radius: 15px;
  font-size: 9px;
  border: 1px solid #cc0000;
}

.three-day-tag {
  background: #fff0e0;
  color: #e67e22;
  padding: 2px 8px;
  border-radius: 15px;
  font-size: 9px;
  border: 1px solid #e67e22;
}

.daily-tag {
  background: #f0f0f0;
  color: #666;
  padding: 2px 8px;
  border-radius: 15px;
  font-size: 9px;
}

.completed-badge {
  margin-top: 6px;
  font-size: 11px;
  color: #27ae60;
}

button { 
  background: #cc0000; 
  padding: 6px 16px; 
  border-radius: 20px; 
  border: none; 
  color: white; 
  font-weight: bold; 
  cursor: pointer;
  font-size: 12px;
  min-width: 90px;
}

button:hover:not(:disabled) {
  background: #990000;
}

button.completed { 
  background: #aaa; 
  color: white;
  cursor: default;
}

@media (max-width: 480px) {
  .quest-card {
    flex-direction: column;
    text-align: center;
  }
  
  .quest-meta {
    justify-content: center;
  }
  
  button {
    width: 100%;
  }
}
</style>
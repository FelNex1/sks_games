<template>
  <div>
    <h2 class="text-center">Слово дня</h2>
    <p class="text-center text-secondary">Угадай слово из 5 букв</p>

    <div class="wordle-grid">
      <div v-for="(row, rowIndex) in grid" :key="rowIndex" class="word-row">
        <div 
          v-for="(cell, colIndex) in row" 
          :key="colIndex" 
          class="letter-cell"
          :class="cell.status"
        >
          {{ cell.letter }}
        </div>
      </div>
    </div>

    <div class="keyboard">
      <div class="keyboard-row">
        <button v-for="key in row1" :key="key" class="key" @click="addLetter(key)">{{ key }}</button>
      </div>
      <div class="keyboard-row">
        <button v-for="key in row2" :key="key" class="key" @click="addLetter(key)">{{ key }}</button>
      </div>
      <div class="keyboard-row">
        <button class="key delete" @click="deleteLetter">←</button>
        <button v-for="key in row3" :key="key" class="key" @click="addLetter(key)">{{ key }}</button>
        <button class="key enter" @click="submitGuess">✓</button>
      </div>
    </div>

    <div v-if="gameWon" class="message success">Поздравляем! +50 бонусов</div>
    <div v-if="gameOver && !gameWon" class="message error">Слово: {{ secretWord }}</div>

    <button class="btn btn-large" style="width: 100%; margin-top: 15px;" @click="resetGame">Новая игра</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const emit = defineEmits(['gameCompleted'])

const row1 = ['Й','Ц','У','К','Е','Н','Г','Ш','Щ','З','Х','Ъ']
const row2 = ['Ф','Ы','В','А','П','Р','О','Л','Д','Ж','Э']
const row3 = ['Я','Ч','С','М','И','Т','Ь','Б','Ю']

const secretWord = ref('')
const currentGuess = ref('')
const attempts = ref([])
const maxAttempts = 6
const gameWon = ref(false)
const gameOver = ref(false)
const isLoading = ref(true)

const grid = ref([])

const initGrid = () => {
  grid.value = []
  for (let i = 0; i < maxAttempts; i++) {
    grid.value.push([])
    for (let j = 0; j < 5; j++) {
      grid.value[i].push({ letter: '', status: '' })
    }
  }
}

// Загрузка слова из бэкенда
const loadWordFromAPI = async () => {
  isLoading.value = true
  try {
    const response = await fetch('http://localhost:8000/api/wordle/word')
    const data = await response.json()
    secretWord.value = data.word
    console.log('Загаданное слово:', secretWord.value)
  } catch (error) {
    console.error('Ошибка загрузки слова:', error)
    // Запасное слово если бэкенд не работает
    secretWord.value = 'МОНЕТ'
  }
  isLoading.value = false
}

const addLetter = (letter) => {
  if (gameWon.value || gameOver.value || isLoading.value) return
  if (currentGuess.value.length < 5) {
    currentGuess.value += letter
    updateGrid()
  }
}

const deleteLetter = () => {
  if (gameWon.value || gameOver.value || isLoading.value) return
  currentGuess.value = currentGuess.value.slice(0, -1)
  updateGrid()
}

const updateGrid = () => {
  const currentRow = attempts.value.length
  for (let i = 0; i < 5; i++) {
    grid.value[currentRow][i].letter = currentGuess.value[i] || ''
  }
}

const submitGuess = () => {
  if (gameWon.value || gameOver.value || isLoading.value) return
  if (currentGuess.value.length !== 5) {
    alert('Нужно 5 букв')
    return
  }

  const guess = currentGuess.value
  const result = evaluateGuess(guess, secretWord.value)
  
  attempts.value.push({ word: guess, result })
  
  for (let i = 0; i < 5; i++) {
    grid.value[attempts.value.length - 1][i].status = result[i]
  }
  
  if (guess === secretWord.value) {
    gameWon.value = true
    let balance = localStorage.getItem('sks_balance')
    balance = balance ? parseInt(balance) : 350
    balance += 50
    localStorage.setItem('sks_balance', balance)
    if (window.completeWordGameQuest) window.completeWordGameQuest()
    alert('+50 бонусов!')
  } else if (attempts.value.length >= maxAttempts) {
    gameOver.value = true
  }
  
  currentGuess.value = ''
  updateGrid()
}

const evaluateGuess = (guess, secret) => {
  const result = []
  const secretArr = secret.split('')
  const guessArr = guess.split('')
  
  for (let i = 0; i < 5; i++) {
    if (guessArr[i] === secretArr[i]) {
      result[i] = 'correct'
      secretArr[i] = null
      guessArr[i] = null
    } else {
      result[i] = ''
    }
  }
  
  for (let i = 0; i < 5; i++) {
    if (guessArr[i] !== null) {
      const index = secretArr.indexOf(guessArr[i])
      if (index !== -1) {
        result[i] = 'present'
        secretArr[index] = null
      } else {
        result[i] = 'absent'
      }
    }
  }
  
  return result
}

const resetGame = async () => {
  currentGuess.value = ''
  attempts.value = []
  gameWon.value = false
  gameOver.value = false
  initGrid()
  await loadWordFromAPI()
}

onMounted(async () => {
  initGrid()
  await loadWordFromAPI()
})
</script>

<style scoped>
.wordle-grid {
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: center;
  margin-bottom: 20px;
}

.word-row {
  display: flex;
  gap: 8px;
  justify-content: center;
}

.letter-cell {
  width: 50px;
  height: 50px;
  background: white;
  border: 2px solid #ddd;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 20px;
}

.letter-cell.correct {
  background: #2ecc71;
  border-color: #2ecc71;
  color: white;
}

.letter-cell.present {
  background: #f39c12;
  border-color: #f39c12;
  color: white;
}

.letter-cell.absent {
  background: #7f8c8d;
  border-color: #7f8c8d;
  color: white;
}

.keyboard {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 15px;
}

.keyboard-row {
  display: flex;
  justify-content: center;
  gap: 5px;
  margin-bottom: 5px;
}

.key {
  width: 38px;
  height: 42px;
  background: #f0f0f0;
  border: 1px solid #aaa;
  border-radius: 8px;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
}

.key.delete, .key.enter {
  width: 55px;
  background: #e0e0e0;
}

.key:hover {
  background: #ddd;
}

@media (max-width: 480px) {
  .letter-cell { width: 42px; height: 42px; font-size: 18px; }
  .key { width: 32px; height: 38px; font-size: 12px; }
  .key.delete, .key.enter { width: 48px; }
}
</style>
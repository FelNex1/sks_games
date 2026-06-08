<template>
  <div>
    <h2>Слово дня</h2>
    <p class="game-desc">Угадай слово из 5 букв</p>

    <div class="wordle-grid">
      <div v-for="(row, rowIndex) in grid" :key="rowIndex" class="word-row">
        <div 
          v-for="(cell, colIndex) in row" 
          :key="colIndex" 
          class="letter-cell"
          :class="getLetterClass(rowIndex, colIndex)"
        >
          {{ cell.letter }}
        </div>
      </div>
    </div>

    <div class="keyboard" v-if="!gameOver && !gameWon">
      <div class="keyboard-row">
        <button v-for="key in row1" :key="key" class="key" @click="addLetter(key)">{{ key }}</button>
      </div>
      <div class="keyboard-row">
        <button v-for="key in row2" :key="key" class="key" @click="addLetter(key)">{{ key }}</button>
      </div>
      <div class="keyboard-row">
        <button class="key del-btn" @click="deleteLetter">←</button>
        <button v-for="key in row3" :key="key" class="key" @click="addLetter(key)">{{ key }}</button>
        <button class="key ok-btn" @click="submitGuess">✓</button>
      </div>
    </div>

    <div v-if="gameWon" class="game-message win">
      Поздравляем! +50 бонусов
    </div>
    <div v-if="gameOver && !gameWon" class="game-message lose">
      Загаданное слово: {{ secretWord }}
    </div>

    <button v-if="gameOver || gameWon" @click="resetGame" class="reset-btn">
      Новая игра
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const emit = defineEmits(['gameCompleted'])

const row1 = ['Й','Ц','У','К','Е','Н','Г','Ш','Щ','З','Х','Ъ']
const row2 = ['Ф','Ы','В','А','П','Р','О','Л','Д','Ж','Э']
const row3 = ['Я','Ч','С','М','И','Т','Ь','Б','Ю']

const wordsList = [
  'ЗОЛОТО', 'СЛИТОК', 'АЛМАЗ', 'РУБИН', 'САПФИР',
  'ИЗУМРУ', 'БРИЛЛИ', 'ЖЕМЧУ', 'ОПАЛЫ', 'АГАТЫ',
  'ЗАЛОГ', 'ВЫКУП', 'МОНЕТ', 'ЧАСЫ', 'КОЛЬЦ'
]

const secretWord = ref('')
const currentGuess = ref('')
const attempts = ref([])
const maxAttempts = 6
const gameWon = ref(false)
const gameOver = ref(false)

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

const getLetterClass = (row, col) => {
  const cell = grid.value[row]?.[col]
  if (!cell) return ''
  return `status-${cell.status}`
}

const addLetter = (letter) => {
  if (gameWon.value || gameOver.value) return
  if (currentGuess.value.length < 5) {
    currentGuess.value += letter
    updateGrid()
  }
}

const deleteLetter = () => {
  if (gameWon.value || gameOver.value) return
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
  if (gameWon.value || gameOver.value) return
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
    
    let currentBalance = localStorage.getItem('sks_balance')
    currentBalance = currentBalance ? parseInt(currentBalance) : 350
    currentBalance += 50
    localStorage.setItem('sks_balance', currentBalance)
    
    if (window.completeWordGameQuest) {
      window.completeWordGameQuest()
    }
    
    alert('+50 бонусов')
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

const resetGame = () => {
  const randomIndex = Math.floor(Math.random() * wordsList.length)
  secretWord.value = wordsList[randomIndex]
  
  currentGuess.value = ''
  attempts.value = []
  gameWon.value = false
  gameOver.value = false
  
  initGrid()
}

onMounted(() => {
  resetGame()
})
</script>

<style scoped>
* {
  box-sizing: border-box;
}

h2 {
  color: #cc0000;
  font-size: 18px;
  text-align: center;
  margin: 0 0 5px 0;
}

.game-desc {
  text-align: center;
  font-size: 11px;
  color: #666;
  margin-bottom: 15px;
}

/* Поле */
.wordle-grid {
  display: flex;
  flex-direction: column;
  gap: 6px;
  align-items: center;
  margin-bottom: 20px;
}

.word-row {
  display: flex;
  gap: 6px;
}

.letter-cell {
  width: 45px;
  height: 45px;
  border: 1px solid #ccc;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: bold;
  text-transform: uppercase;
}

/* Цвета */
.status-correct {
  background: #2ecc71;
  border-color: #2ecc71;
  color: white;
}

.status-present {
  background: #f39c12;
  border-color: #f39c12;
  color: white;
}

.status-absent {
  background: #7f8c8d;
  border-color: #7f8c8d;
  color: white;
}

/* Клавиатура */
.keyboard {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.keyboard-row {
  display: flex;
  justify-content: center;
  gap: 5px;
  margin-bottom: 5px;
}

.key {
  width: 35px;
  height: 40px;
  background: #f0f0f0;
  border: 1px solid #aaa;
  border-radius: 6px;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
  color: black;
}

.del-btn, .ok-btn {
  width: 50px;
  background: #e0e0e0;
}

.key:hover {
  background: #ddd;
}

/* Сообщения */
.game-message {
  text-align: center;
  padding: 8px;
  margin-top: 12px;
  font-weight: bold;
  font-size: 13px;
}

.game-message.win {
  background: #2ecc71;
  color: white;
}

.game-message.lose {
  background: #cc0000;
  color: white;
}

.reset-btn {
  width: 100%;
  margin-top: 12px;
  padding: 8px;
  background: #cc0000;
  color: white;
  border: none;
  border-radius: 20px;
  font-weight: bold;
  cursor: pointer;
}

/* Мобилки */
@media (max-width: 500px) {
  .letter-cell {
    width: 40px;
    height: 40px;
    font-size: 18px;
  }
  .key {
    width: 30px;
    height: 38px;
    font-size: 12px;
  }
  .del-btn, .ok-btn {
    width: 45px;
  }
}

@media (max-width: 400px) {
  .letter-cell {
    width: 35px;
    height: 35px;
    font-size: 16px;
  }
  .word-row {
    gap: 4px;
  }
  .key {
    width: 26px;
    height: 35px;
    font-size: 11px;
  }
  .del-btn, .ok-btn {
    width: 40px;
  }
}
</style>  
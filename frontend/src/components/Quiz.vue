<template>
  <div>
    <h2>Золотая викторина</h2>
    <p class="quiz-desc">Ответь на вопросы о золоте!</p>

    <div v-if="!quizCompleted && !gameWon" class="quiz-container">
      <div class="question-header">
        <span>Вопрос {{ currentQuestion + 1 }} из {{ questions.length }}</span>
        <span>Счёт: {{ score }} / {{ questions.length }}</span>
      </div>

      <div class="question-card">
        <h3>{{ questions[currentQuestion].question }}</h3>
        <div class="answers">
          <button 
            v-for="(answer, idx) in questions[currentQuestion].answers" 
            :key="idx"
            class="answer-btn"
            @click="checkAnswer(idx)"
            :disabled="answerLocked"
          >
            {{ answer }}
          </button>
        </div>
      </div>
    </div>

    <div v-if="quizCompleted && !gameWon" class="result-card lose">
      <h3>Викторина окончена</h3>
      <p>Результат: {{ score }} из {{ questions.length }}</p>
      <button @click="resetQuiz" class="reset-btn">Попробовать снова</button>
    </div>

    <div v-if="gameWon" class="result-card win">
      <h3>Поздравляю!</h3>
      <p>+25 бонусов за викторину!</p>
      <button @click="resetQuiz" class="reset-btn">Играть ещё</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const emit = defineEmits(['quizCompleted'])

const questions = ref([
  { question: 'Какой металл самый драгоценный?', answers: ['Серебро', 'Платина', 'Золото', 'Бронза'], correct: 2 },
  { question: 'Какая проба золота самая высокая?', answers: ['585', '750', '875', '999'], correct: 3 },
  { question: 'Какой камень самый твёрдый?', answers: ['Рубин', 'Сапфир', 'Изумруд', 'Алмаз'], correct: 3 },
  { question: 'Что такое ломбард?', answers: ['Магазин', 'Банк', 'Кредит под залог', 'Ювелирка'], correct: 2 },
  { question: 'Что означает 750 проба?', answers: ['75% золота', '7.5%', '750%', '0.75%'], correct: 0 },
])

const currentQuestion = ref(0)
const score = ref(0)
const quizCompleted = ref(false)
const gameWon = ref(false)
const answerLocked = ref(false)

const checkAnswer = (idx) => {
  if (answerLocked.value) return
  answerLocked.value = true
  
  const isCorrect = idx === questions.value[currentQuestion.value].correct
  
  if (isCorrect) score.value++
  
  alert(isCorrect ? '✅ Правильно!' : `❌ Неправильно! Правильный ответ: ${questions.value[currentQuestion.value].answers[questions.value[currentQuestion.value].correct]}`)
  
  setTimeout(() => {
    if (currentQuestion.value + 1 < questions.value.length) {
      currentQuestion.value++
      answerLocked.value = false
    } else {
      quizCompleted.value = true
      if (score.value === questions.value.length) {
        gameWon.value = true
        emit('quizCompleted')
        
        let balance = localStorage.getItem('sks_balance')
        balance = balance ? parseInt(balance) : 350
        balance += 25
        localStorage.setItem('sks_balance', balance)
        
        if (window.completeQuizQuest) window.completeQuizQuest()
        alert('🎉 +25 бонусов!')
      }
      answerLocked.value = false
    }
  }, 500)
}

const resetQuiz = () => {
  currentQuestion.value = 0
  score.value = 0
  quizCompleted.value = false
  gameWon.value = false
  answerLocked.value = false
}

onMounted(resetQuiz)
</script>

<style scoped>
h2 { color: #cc0000; text-align: center; }
.question-card { background: white; border-radius: 24px; padding: 25px; border: 2px solid #cc0000; }
.answer-btn { padding: 12px; background: white; border: 2px solid #cc0000; border-radius: 40px; margin: 5px; cursor: pointer; color: #cc0000; font-weight: bold; }
.answer-btn:hover { background: #cc0000; color: white; }
.win { background: #2ecc71; color: white; padding: 20px; border-radius: 20px; text-align: center; }
.lose { background: #e74c3c; color: white; padding: 20px; border-radius: 20px; text-align: center; }
.reset-btn { margin-top: 15px; padding: 10px 20px; background: white; color: #cc0000; border: 2px solid #cc0000; border-radius: 40px; cursor: pointer; }
</style>
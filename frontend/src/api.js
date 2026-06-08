import axios from 'axios'

const API_BASE = 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  }
})

// ========== КЛИЕНТЫ ==========

export const getProfile = (clientId = 1) => 
  api.get(`/clients/${clientId}/profile`)

export const doCheckin = (clientId = 1) => 
  api.post(`/clients/${clientId}/checkin`)

// ========== КВЕСТЫ ==========

export const getQuests = (clientId = 1) => 
  api.get(`/clients/${clientId}/quests`)

export const completeQuest = (clientId = 1, questId) => 
  api.post(`/clients/${clientId}/quests/${questId}/complete`)

// ========== КОЛЕСО ФОРТУНЫ ==========

export const getWheelStatus = (clientId = 1) => 
  api.get(`/clients/${clientId}/wheel/status`)

export const spinWheel = (clientId = 1) => 
  api.post(`/clients/${clientId}/wheel/spin`)

// ========== МАГАЗИН ==========

export const getMarketplaceItems = () => 
  api.get('/marketplace/items')

export const purchaseItem = (clientId = 1, itemId) => 
  api.post(`/clients/${clientId}/purchase`, { item_id: itemId })

// ========== ВИКТОРИНА ==========

export const getQuizQuestions = () => 
  api.get('/quiz/questions')

// ========== WORDLE ==========

export const getWordleWord = () => 
  api.get('/wordle/word')

export default api
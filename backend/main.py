from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import init_db, get_client, do_checkin, get_quests, complete_quest, get_wordle_word, get_wheel_prize

# Создаём базу данных при запуске
init_db()

app = FastAPI()

# Разрешаем запросы с фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== КЛИЕНТЫ ==========
@app.get("/api/client/{client_id}")
def get_client_info(client_id: int):
    client = get_client(client_id)
    if not client:
        raise HTTPException(404, "Клиент не найден")
    return client

@app.post("/api/client/{client_id}/checkin")
def checkin(client_id: int):
    result = do_checkin(client_id)
    if not result:
        raise HTTPException(400, "Уже получали бонус сегодня")
    return result

# ========== КВЕСТЫ ==========
@app.get("/api/client/{client_id}/quests")
def get_client_quests(client_id: int):
    return get_quests(client_id)

@app.post("/api/client/{client_id}/quests/{quest_id}/complete")
def complete_client_quest(client_id: int, quest_id: int):
    result = complete_quest(client_id, quest_id)
    if not result:
        raise HTTPException(400, "Квест уже выполнен")
    return result

# ========== WORDLE ==========
@app.get("/api/wordle/word")
def get_word():
    return {"word": get_wordle_word()}

# ========== КОЛЕСО ==========
@app.get("/api/wheel/prize")
def get_prize():
    return get_wheel_prize()

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
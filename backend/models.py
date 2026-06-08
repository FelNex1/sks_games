from pydantic import BaseModel
from typing import Optional
from datetime import date

class ClientProfile(BaseModel):
    id: int
    phone: str
    name: str
    balance: int
    streak: int
    status_level: str
    can_checkin: bool

class CheckinResponse(BaseModel):
    new_balance: int
    new_streak: int

class QuestCompleteResponse(BaseModel):
    reward: int
    new_balance: int

class SpinResponse(BaseModel):
    name: str
    value: int

class MarketplaceItem(BaseModel):
    id: int
    name: str
    description: str
    price: int
    icon: str
    category: str
    stock: int

class BuyResponse(BaseModel):
    success: bool
    new_balance: int
    item_name: str

class QuizQuestion(BaseModel):
    id: int
    question: str
    answers: list[str]
    correct_answer: int
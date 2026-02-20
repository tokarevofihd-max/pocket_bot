import asyncio
import random
import sqlite3

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

import config

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# ===== БАЗА =====

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    pocket_id TEXT,
    verified INTEGER DEFAULT 0
)
""")
conn.commit()

# ===== FSM =====

class RegisterState(StatesGroup):
    waiting_for_pocket_id = State()

# ===== КНОПКИ =====

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Профиль")],
        [KeyboardButton(text="📈 Получить сигнал")]
    ],
    resize_keyboard=True
)

start_menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="📈 Получить сигнал")]],
    resize_keyboard=True
)

# ===== СТАРТ =====

@dp.message(CommandStart())
async def start(message: types.Message):
    cursor.execute("INSERT OR IGNORE INTO users(user_id) VALUES(?)", (message.from_user.id,))
    conn.commit()

    await message.answer(
        "🔥 PREMIUM SIGNALS\n\nНажми кнопку чтобы получить сигнал 👇",
        reply_markup=start_menu
    )

# ===== ПОЛУЧИТЬ СИГНАЛ / РЕГИСТРАЦИЯ =====

@dp.message(F.text == "📈 Получить сигнал")
async def reg(message: types.Message, state: FSMContext):

    cursor.execute("SELECT verified FROM users WHERE user_id=?", (message.from_user.id,))
    user = cursor.fetchone()

    # если уже есть доступ
    if user and user[0] == 1:
        signal_text = random.choice(signals)
        await message.answer(f"📊 Сигнал:\n\n{signal_text}")
        return

    # если нет доступа — просим ID
    await message.answer(
        f"1️⃣ Зарегистрируйся по ссылке:\n{config.REF_LINK}\n\n"
        f"2️⃣ Отправь свой ID аккаунта"
    )

    await state.set_state(RegisterState.waiting_for_pocket_id)

# ===== ПРИЕМ ID =====

@dp.message(RegisterState.waiting_for_pocket_id)
async def save_id(message: types.Message, state: FSMContext):

    cursor.execute(
        "UPDATE users SET pocket_id=?, verified=1 WHERE user_id=?",
        (message.text, message.from_user.id)
    )
    conn.commit()

    await message.answer("✅ Доступ открыт!", reply_markup=menu)
    await state.clear()

# ===== ПРОФИЛЬ =====

@dp.message(F.text == "📊 Профиль")
async def profile(message: types.Message):

    cursor.execute("SELECT pocket_id, verified FROM users WHERE user_id=?", (message.from_user.id,))
    user = cursor.fetchone()

    if not user:
        await message.answer("Ты не зарегистрирован")
        return

    status = "✅ Есть доступ" if user[1] == 1 else "❌ Нет доступа"

    await message.answer(
        f"👤 Профиль\n\n"
        f"ID: {user[0]}\n"
        f"Статус: {status}"
    )

# ===== СИГНАЛЫ =====

signals = [
    "EUR/USD BUY ⬆️ 1 мин",
    "GBP/USD SELL ⬇️ 5 мин",
    "USD/JPY BUY ⬆️ 3 мин",
    "AUD/USD SELL ⬇️ 2 мин",
    "BTC/USD BUY ⬆️ 1 мин",
    "EUR/JPY SELL ⬇️ 5 мин"
]

# ===== ЗАПУСК =====

async def main():
    print("✅ Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

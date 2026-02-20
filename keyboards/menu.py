from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("📊 Получить сигнал"))
    kb.add(KeyboardButton("👤 Профиль"))
    return kb

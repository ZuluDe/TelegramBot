from aiogram.types import(
    ReplyKeyboardMarkup, 
    KeyboardButton, 
    ReplyKeyboardRemove
)

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Найти друга 🔍"),
            KeyboardButton(text="Показать мой профиль 📋")
        ],
        [
            KeyboardButton(text="Ответы от других пользователей 👁‍🗨")
        ]
    ],
    resize_keyboard=True,
)


rmk = ReplyKeyboardRemove()
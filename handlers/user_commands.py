from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from data.get_id import user_id_in_table
from data.tables import main
from keyboards.reply import main_kb

router = Router()

@router.message(Command('start'))
async def start(message: Message):
    await main()
    if await user_id_in_table(message.from_user.id):
        await message.answer(f"Добро пожаловать, здесь ты можешь найти себе новых друзей 🤜🏼🤛🏼", reply_markup=main_kb)
    else:
        await message.answer(f"У вас нет профиля ❌, воспользуйтесь командной \n/profile")

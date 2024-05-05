from aiogram import Router, F 
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from untils.states import Form
from keyboards.builders import profile
from data.data import new_profile
from data.tables import main
from keyboards import reply
from keyboards.reply import rmk, main_kb

router = Router()



@router.message(Command("back"))
@router.message(F.text.lower()=="назад")
async def back(message: Message, state: FSMContext):
    await message.answer("Вы возвращены")
    await state.clear()

@router.message(Command("profile"))
@router.message(F.text.lower() == "создать анкету")
async def fill_profile(message: Message, state: FSMContext):
    await state.set_state(Form.id_u)
    await state.update_data(id_u=message.from_user.id)
    await state.set_state(Form.username)
    await state.update_data(username=message.from_user.username)
    await state.set_state(Form.name)
    await message.answer(f"Заполни анкету, но если ты вдруг передумаешь, то просто напиши назад или /back")
    await message.answer(
        "Введи имя или используй имя в telegram",
        reply_markup=profile(message.from_user.first_name)
    )

@router.message(Form.name)
async def form_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.age)
    await message.answer("Введи возраст", reply_markup=rmk)

@router.message(Form.age)
async def form_age(message: Message, state: FSMContext):
    if message.text.isdigit():
        if message.text.isdigit():
            if int(message.text) < 12:
                await message.answer(f"Ты слишком маленький(ая)((( \nПодожи до 12")
            elif int(message.text) > 20:
                await message.answer(f"Ты знаешь что это только для школьников?")
            else:
                await state.update_data(age=message.text)
                await state.set_state(Form.clas)
                await message.answer("Введи класс (без параллели)")
    else:
        await message.answer("Введи целое число")
    
@router.message(Form.clas)
async def form_clas(message: Message, state: FSMContext):
    if message.text.isdigit():
        if int(message.text) in range (1, 12):
            await state.update_data(clas=message.text)
            await state.set_state(Form.gender)
            await message.answer(
                "Выбери пол",
                reply_markup=profile(["М","Ж"])
            )
        else:
            await message.answer("1-11")
    else:
        await message.answer("Введите целое число")

@router.message(Form.gender, F.text.lower().in_(["м", "ж"]))
async def form_gender(message: Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await state.set_state(Form.about)
    await message.answer("Расскажи о себе", reply_markup=rmk)

@router.message(Form.gender)
async def incorrect_form_gender(message: Message, state: FSMContext):
    await message.answer(
        "Нажми на кнопку", 
        reply_markup=profile(["М","Ж"]))

@router.message(Form.about)
async def form_about(message: Message, state: FSMContext):
    if len(message.text) < 5:
        await message.answer("Введи что-нибудь поинтереснее")
    else:
        await state.update_data(about=message.text)
        await state.set_state(Form.photo)
        await message.answer("Теперь отпрвь свое фото")

@router.message(Form.photo, F.photo)
async def form_photo(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    await main()
    await new_profile(state)
    await state.clear()
    await message.answer("Вы успешно зарегестрировались", reply_markup=main_kb)

@router.message(Form.photo, ~F.photo)
async def incorrect_form_photo(message: Message, state: FSMContext):
    await message.answer("Отправь фото!")
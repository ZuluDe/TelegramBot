from aiogram import Router, F, types, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode


from config_reader import config



from filters.is_registered import IsRegisteredUser
from data.tables import main
from data.profiles import get_profile, get_random_user_id
from keyboards.inline import assessment_kb
from untils.states import Assessment
from data.liked import assess_profile_like, asses_profile_dislike, reciprocity
from data.awaiting_response import update_awaiting_response


bot= Bot(config.bot_token.get_secret_value())
router = Router()




@router.message(F.text.lower() == "найти друга 🔍", IsRegisteredUser())
async def fiend_friend(message: Message, state: FSMContext):
    await state.set_state(Assessment.id_user)
    await state.update_data(id_user=message.from_user.id)
    await state.set_state(Assessment.id_other)
    await main()
    user = await get_random_user_id(str(message.from_user.id))
    await state.update_data(id_other=user)
    await state.set_state(Assessment.id_user)

    user_data = await get_profile(user)

    if user_data == None:
        await message.answer(f"Пока заявок нет((\nПриходи позже")
    else:
        formatted_text = []
        [
            formatted_text.append(f"<b>{key}:</b> {value}")
            for key, value in user_data.items() if key != "Фото"
        ]
        photo_id = user_data["Фото"]

        await message.answer_photo(
            photo_id,
            "\n".join(formatted_text),
            reply_markup=assessment_kb,
            parse_mode=ParseMode.HTML
        )

@router.callback_query(F.data == "like")
async def liked_profile(callback: CallbackQuery, state: FSMContext):
    await state.update_data(asses="liked")
    await callback.message.edit_reply_markup(reply_markup=None)
    await assess_profile_like(state)
    recip = await reciprocity(state)
    if recip:
        try:
            await bot.send_message(chat_id=recip[0], text="Кто-то ответил вам")
            await update_awaiting_response(recip[0], recip[1])
        except:
            await bot.send_message(chat_id=recip[1], text="Видимо данный пользователь заблокировал бота или удалил аккаунт")

        
        try:
            await bot.send_message(chat_id=recip[1], text="Кто-то ответил вам")
            await update_awaiting_response(recip[1], recip[0])
        except:
            await bot.send_message(chat_id=recip[0], text="Видимо данный пользователь заблокировал бота или удалил аккаунт")

    await state.clear()

@router.callback_query(F.data == "dislike")
async def liked_profile(callback: CallbackQuery, state: FSMContext):
    await state.update_data(asses="disliked")
    await callback.message.edit_reply_markup(reply_markup=None)
    await asses_profile_dislike(state)
    await state.clear()
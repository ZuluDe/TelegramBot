from aiogram import F, Router
from aiogram.types import Message 
from aiogram.enums import ParseMode

from filters.is_registered import IsRegisteredUser

from data.tables import main
from data.profiles import get_profile, get_profile_re
from data.awaiting_response import find_and_extract



router = Router()




@router.message(F.text.lower() == "показать мой профиль 📋", IsRegisteredUser())
async def fiend_friend(message: Message):
    await main()
    user_data = await get_profile(message.from_user.id)

    formatted_text = []
    [
        formatted_text.append(f"<b>{key}:</b> {value}")
        for key, value in user_data.items() if key != "Фото"
    ]
    photo_id = user_data["Фото"]

    await message.answer_photo(
        photo_id,
        "\n".join(formatted_text),
        parse_mode=ParseMode.HTML
    )

@router.message(F.text.lower() == "ответы от других пользователей 👁‍🗨", IsRegisteredUser())
async def aswer_otger_users(message: Message):
    users = await find_and_extract(str(message.from_user.id))
    if users:
        for elements in users:
            user_data = await get_profile_re(elements)

            formatted_text = []
            [
                formatted_text.append(f"<b>{key}:</b> {value}")
                for key, value in user_data.items() if key != "Фото" and key != "Username в Telegram"
            ]
            username = f"||@{user_data['Username в Telegram']}||" if 'Username в Telegram' in user_data else "аноним"


            photo_id = user_data["Фото"]

            await message.answer_photo(
                photo_id,
                "\n".join(formatted_text),
                parse_mode=ParseMode.HTML
            )
            await message.answer(f"**Username в Telegram:** {username}", parse_mode=ParseMode.MARKDOWN_V2)
    else:
        await message.answer("Пока у вас нет никаких ответов")


@router.message(F.text)
async def echo(message: Message):
    await message.answer("Я тебя не понимаю")
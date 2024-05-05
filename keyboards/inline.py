from aiogram.types import(
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


assessment_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="👍🏼", callback_data="like"),
            InlineKeyboardButton(text="👎🏼", callback_data="dislike")
        ]
    ]
)
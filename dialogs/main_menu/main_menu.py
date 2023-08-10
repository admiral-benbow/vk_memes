from typing import List


from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

from aiogram_dialog import DialogManager

router = Router()


@router.message(Command("start", "menu"))
async def meow(message: Message):
    main_kb_buttons: List[List[KeyboardButton]] = [
        [
            KeyboardButton(text="Просмотреть мемы 🎩"),
            KeyboardButton(text="Настроить бота ⚙️")
        ]
    ]
    main_keyboard = ReplyKeyboardMarkup(keyboard=main_kb_buttons, resize_keyboard=True, one_time_keyboard=True)

    await message.answer("Я вас категорически приветствую", reply_markup=main_keyboard)


@router.message(Command("stop"))
async def stop(message: Message, dialog_manager: DialogManager):
    await message.answer("Gut, Bubba schließt das dialog")
    await dialog_manager.done()

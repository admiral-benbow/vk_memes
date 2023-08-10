from typing import List

from aiogram import Router
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, input_file
from aiogram.filters import Command

# from loader import dp


PHOTO_ID = "AgACAgIAAxkBAANXZDmRlKhyAyZmR4Jdl6HfhwLJaF0AAsXNMRvRtNFJVA5bKQkkGbcBAAMCAAN4AAMvBA"

router = Router()


def get_keyboard():
    photo_kb_bts: List[List[InlineKeyboardButton]] = [
        [InlineKeyboardButton(text="Постим пикчу", callback_data="bubba")],
        [InlineKeyboardButton(text="Выкидываем в урну", callback_data="babba")]
    ]
    photo_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=photo_kb_bts)

    return photo_inline_keyboard


@router.message(Command("check"))
async def photo_check(message: Message) -> None:
    hq_photo = message.photo[-1]
    print(hq_photo.file_id)


@router.message(Command("photo"))
async def photo_test(message: Message):
    # Если отправляю по file_id. Что, скорее всего, я использовать всё равно не буду
    # await message.answer_photo(photo=PHOTO_ID, reply_markup=get_keyboard())

    photo_file = input_file.FSInputFile(path=r"C:\Me\Wallpapers\Animation\saitama - ok.jfif")
    # print("Bubba")

    await message.answer_photo(photo=photo_file, reply_markup=get_keyboard())

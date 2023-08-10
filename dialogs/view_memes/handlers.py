import os

from aiogram.types import Message, CallbackQuery
from aiogram.filters import Text

from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import TextInput

from loader import dp
from dialogs.states import ViewMemes


# Старт диалога по просмотру спарсенных мемов
@dp.message(Text("Просмотреть мемы 🎩"))
async def start_veiwing(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=ViewMemes.choose_memes, mode=StartMode.RESET_STACK)


async def from_choose_to_viewing(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, *args) -> None:
    group_id_callback = callback.data.removeprefix("choose_channels_kb:")
    dialog_manager.dialog_data["group_id"] = group_id_callback
    await dialog_manager.next()

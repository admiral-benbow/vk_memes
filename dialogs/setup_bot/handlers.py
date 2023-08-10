import requests

from aiogram.types import Message, CallbackQuery
from aiogram.filters import Text

from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import TextInput

from loader import dp
from dialogs.states import SetupBot


# Старт диалога по настройке бота
@dp.message(Text("Настроить бота ⚙️"))
async def start_bot_setup(message: Message, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(state=SetupBot.choose_public, mode=StartMode.RESET_STACK)


# Part_1: enter the name of a public
def public_validation(name_or_url: str):
    if not name_or_url.startswith("http"):
        name_or_url = "https://vk.com/" + name_or_url

    res = requests.get(url=name_or_url)
    if res.status_code == 404:
        raise ValueError("паблика не существует")

    # Ввести проверку на то, что паблик уже был добавлен / Или ввести её в функции: public_input_success ?

    return name_or_url


async def public_input_success(message: Message, widget: TextInput, dialog_manager: DialogManager, *args) -> None:
    public_input_widget = dialog_manager.find("public_name_input")
    input_text: str = public_input_widget.get_value().removeprefix("https://vk.com/")

    if not dialog_manager.dialog_data.get("publics"):
        dialog_manager.dialog_data["publics"] = [input_text]
        await message.answer("Записал паблик")
        await dialog_manager.next()
    else:
        if input_text not in dialog_manager.dialog_data["publics"]:
            dialog_manager.dialog_data["publics"].append(input_text)
            await message.answer("Записал паблик")
            await dialog_manager.next()
        else:
            await message.answer("Уже есть такой паблик, красавчик")
            await dialog_manager.next()


async def public_input_error(message: Message, widget: TextInput, dialog_manager: DialogManager, *args) -> None:
    await message.reply("Паблик не найден. Проверьте, пожалуйста, введённое название (ссылку)")


# Part_2: enter another public?
async def yes_enter_more_publics(callback: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    await dialog_manager.back()


async def no_enter_more_publics(callback: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    await callback.message.answer("Haha, bubba Kacke")


# Part_3: update time


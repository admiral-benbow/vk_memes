from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Button, Group, Column
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput, MessageInput

from dialogs.states import SetupBot
from . import handlers
from . import getters


# Точка входа в сценарий настройки


# creating a dialog for setting up our Bot

# creating a window to input publics
enter_public_window = Window(
    Const("Введите короткое название паблика (название указывается в vk.com/<u><b>короткое_название</b></u>)\n"
          "Пример ввода: <i>'yobangelion'</i>"),
    TextInput(
        id="public_name_input",
        type_factory=handlers.public_validation,
        on_success=handlers.public_input_success,
        on_error=handlers.public_input_error
    ),
    state=SetupBot.choose_public
)

# creating a window to ask if a user wants to input another public
more_publics_window = Window(
    Const("Добавить ещё один паблик?"),
    Column(
        Button(
            Const("Да"),
            id="yes_more_publics_but",
            on_click=handlers.yes_enter_more_publics
        ),
        Button(
            Const("Не-а, хватит"),
            id="no_more_publics_but",
            on_click=handlers.no_enter_more_publics
        )
    ),
    state=SetupBot.more_publics
)

# Window to ask for update time
# update_window = Window(
#     Const("С какой частотой будем обновлять паблики? Введите время: "),
#     TextInput(
#         id="update_time_input",
#         type_factory=int,
#         # on_success=,
#         # on_error=,
#     )
# )

# Собираем все окна в список
setup_bot_windows = [
    enter_public_window,
    more_publics_window
]

setup_bot_dialog = Dialog(*setup_bot_windows)

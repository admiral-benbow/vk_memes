import operator

from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Button, Group, Column, Row, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.media import StaticMedia, DynamicMedia
from aiogram_dialog.widgets.input import TextInput, MessageInput

from dialogs.states import ViewMemes
from . import handlers
from . import getters


# Точка входа в диалог по просмотру мемов
# creating a dialog for viewing memes

# Part_1: window for dialog beginning
choose_memes_window = Window(
    Const("Выберете мемы для просмотра"),
    Row(
        Button(
            Const("Все мемы "),
            id="choose_all_memes_but",
            # on_click=,
        ),
        Button(
            Const("Избранное ⭐️"),
            id="choose_fav_memes_but",
            # on_click=,
        ),
    ),
    ScrollingGroup(
        Select(
            Format("{item[1]}"),   # В случае обычного "геттера" - просто item без индекса. Если "двойной" список - то item
            id="choose_channels_kb",
            item_id_getter=operator.itemgetter(0),
            items="channels",
            on_click=handlers.from_choose_to_viewing,
        ),
        id="choose_memes_scrolling",
        width=2,
        height=3
    ),
    Row(
        Button(
            Const("Назад ⬅️"),
            id="event_dates_back_but",
            # on_click=
        ),
        Button(
            Const("Стоп 👌"),
            id="event_dates_done_but",
            # on_click=
        )
    ),
    state=ViewMemes.choose_memes,
    getter=getters.test_groups_getter_2   # ACHTUNG! Здесь тестовая функция геттера

)

# Part_2: выбор паблика с мемами и их просмотр
viewing_memes_window = Window(
    Format("Should be a list of memes: {list}"),
    # DynamicMedia("photo"),
    getter=getters.get_list_memes,
    state=ViewMemes.viewing_memes
)

view_memes_windows = [
    choose_memes_window,
    viewing_memes_window
]

view_memes_dialog = Dialog(*view_memes_windows)

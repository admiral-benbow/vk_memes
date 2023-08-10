from aiogram.filters.state import State, StatesGroup


class SetupBot(StatesGroup):
    choose_public = State()
    more_publics = State()
    choose_update_time = State()


class ViewMemes(StatesGroup):
    choose_memes = State()
    viewing_memes = State()

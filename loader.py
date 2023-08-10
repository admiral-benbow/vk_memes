from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN




# creating a memory storage for dialogs and FSM
storage = MemoryStorage()

# creating a bot-оbject and its dispatcher
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(storage=storage)

# from dialogs.main_menu import main_menu
# from dialogs.view_memes import test_send_photo
#
#
# dp.include_routers(main_menu.router, test_send_photo.router)

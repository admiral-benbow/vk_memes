import asyncio
import logging

from aiogram_dialog import setup_dialogs

from loader import bot, dp

# this import is a must-have, because won't work otherwise, or not anymore?
# import dialogs
from dialogs.main_menu import main_menu
from dialogs.view_memes import test_send_photo
from dialogs.setup_bot.dialogs import setup_bot_dialog
from dialogs.view_memes.dialogs import view_memes_dialog


async def main():
    dp.include_routers(
        main_menu.router,
        test_send_photo.router,
        setup_bot_dialog,
        view_memes_dialog
    )
    setup_dialogs(dp)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from bot import dispatcher, handlers


from scrapper.IMDb_scrapper import get_url_random_from_top_250, get_data_for_random, get_genres
# from bot.hendlers import start_handler, cmd_random_Top_250_Movies


GENRES = set()


async def on_startup(_):
    print('bot is online')
    GENRES = get_genres()


if __name__ == '__main__':
    executor.start_polling(dispatcher.dp, skip_updates=True, on_startup=on_startup)

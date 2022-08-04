from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import os
from dotenv import load_dotenv
from scrapper.IMDb_scrapper import get_url_random_from_top_250, get_data_for_random, get_genres
# from bot.hendlers import start_handler, cmd_random_Top_250_Movies

load_dotenv()

TOKEN = os.getenv('TOKEN')
bot = Bot(TOKEN)
dp = Dispatcher(bot)
GENRES = set()


async def on_startup(_):
    print('bot is online')
    GENRES = get_genres()


@dp.message_handler(commands=['start'])
async def start_handler(event: types.Message):
    await event.answer(
        (
            f"Hello, {event.from_user.get_mention(as_html=True)} 👋! \n"
            f"There is the IMDB suggest bot"
        ),
        parse_mode=types.ParseMode.HTML,
    )


@dp.message_handler(commands=['random_Top_250_Movies'])
async def cmd_random_Top_250_Movies(message: types.Message):
    url = get_url_random_from_top_250(message.text[1:])
    data = get_data_for_random(url)
    await bot.send_message(message.chat.id, data)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

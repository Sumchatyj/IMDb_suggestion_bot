from aiogram import types

from .dispatcher import dp
from scrapper.IMDb_scrapper import Title_Single


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
    title = Title_Single(message.text[1:])
    await title.get_data()
    await message.answer(title.title)

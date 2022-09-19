from aiogram import types

from .dispatcher import dp
from scrapper.IMDb_scrapper import Title_Single, Client


@dp.message_handler(commands=["start"])
async def start_handler(event: types.Message):
    await event.answer(
        (
            f"Hello, {event.from_user.get_mention(as_html=True)} 👋! \n"
            f"There is the IMDB suggest bot"
        ),
        parse_mode=types.ParseMode.HTML,
    )


@dp.message_handler(commands=["random_Top_250_Movies"])
async def get_single_title(message: types.Message):
    client = Client()
    title = Title_Single(client, message.text[1:])
    await title.get_data()
    await title.session_close()
    text = (
        f'<i>Title</i>: <b>{title.title}</b>\n'
        f'<i>Genres</i>: {", ".join(title for title in title.genres)}\n'
        f'<i>Relese date</i>: {title.date}\n'
        f'<i>Duration</i>: {title.duration}\n'
        f'<i>Raiting</i>: {title.rating}\n'
        f'<i>Storyline</i>: {title.storyline}\n'
        f'<i>Tags</i>: {", ".join(tag for tag in title.tags)}\n'
    )
    await message.answer_photo(
        photo=title.poster,
        caption=text,
        parse_mode='HTML'
    )

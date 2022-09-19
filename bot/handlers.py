from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from .dispatcher import dp
from .keyboards import (
    MAIN_MENU,
    MOVIE_GENRES,
    MOVIE_GENRES_P1,
    MOVIE_GENRES_P2
)
from scrapper.IMDb_scrapper import Title_Single, Client, GENRES_MOVIE_LIST


@dp.message_handler(commands=["start"])
async def start_handler(event: types.Message):
    await event.answer(
        (
            f"Hello, {event.from_user.get_mention(as_html=True)} 👋! \n"
            f"There is the IMDB suggest bot"
        ),
        parse_mode=types.ParseMode.HTML,
        reply_markup=MAIN_MENU
    )


@dp.message_handler(commands=["menu"])
async def menu_handler(event: types.Message):
    await event.answer(
        "Choose the command",
        reply_markup=MAIN_MENU
    )


@dp.message_handler(commands=["movie_genres"])
async def Movie_Genres_p0_handler(event: types.Message):
    await event.answer(
        "First page of genres",
        reply_markup=MOVIE_GENRES
    )


@dp.message_handler(commands=["movie_genres_p1"])
async def Movie_Genres_p1_handler(event: types.Message):
    await event.answer(
        "Second page of genres",
        reply_markup=MOVIE_GENRES_P1
    )


@dp.message_handler(commands=["movie_genres_p2"])
async def Movie_Genres_p2_handler(event: types.Message):
    await event.answer(
        "Second page of genres",
        reply_markup=MOVIE_GENRES_P2
    )

@dp.message_handler(commands=GENRES_MOVIE_LIST)
async def get_single_title_handler(message: types.Message):
    client = Client()
    title = Title_Single(client, message.text[1:])
    await title.get_data()
    await title.session_close()
    text = (
        f'<i>Title</i> 🎥: <b>{title.title}</b>\n'
        f'<i>Genres</i> 🗂: {", ".join(title for title in title.genres)}\n'
        f'<i>Tags</i> #️⃣: {", ".join(tag for tag in title.tags)}\n'
        f'<i>Relese date</i> 📅: {title.date}\n'
        f'<i>Duration</i> 🕑: {title.duration}\n'
        f'<i>Raiting</i> ⭐: {title.rating}\n'
        f'<i>Storyline</i> 📃: {title.storyline}\n'
    )
    if len(text) > 1080:
        text = text[:1077].rstrip()
        if text[-1] in [',', '.']:
            text = text[:1076]
        text = text + "..."
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=f'{message.text}'),
                KeyboardButton(text='/menu'),
            ]
        ],
        resize_keyboard=True,
    )
    await message.answer_photo(
        photo=title.poster,
        caption=text,
        parse_mode='HTML',
        reply_markup=markup
    )

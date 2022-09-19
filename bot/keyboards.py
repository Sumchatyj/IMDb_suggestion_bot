from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from scrapper.IMDb_scrapper import GENRES_MOVIE_LIST


MAIN_MENU = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='/Top_250_Movie'),
            KeyboardButton(text='/movie_genres'),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

MOVIE_GENRES = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=f'/{GENRES_MOVIE_LIST[1]}'),
            KeyboardButton(text=f'/{GENRES_MOVIE_LIST[2]}'),
            KeyboardButton(text=f'/{GENRES_MOVIE_LIST[3]}'),
        ],
        [
            KeyboardButton(text=f'/{GENRES_MOVIE_LIST[4]}'),
            KeyboardButton(text=f'/{GENRES_MOVIE_LIST[5]}'),
            KeyboardButton(text=f'/{GENRES_MOVIE_LIST[6]}'),
        ],
        [
            KeyboardButton(text=f'/{GENRES_MOVIE_LIST[7]}'),
            KeyboardButton(text=f'/{GENRES_MOVIE_LIST[8]}'),
            KeyboardButton(text=f'/{GENRES_MOVIE_LIST[9]}'),
        ],
        [
            KeyboardButton(text='/menu'),
            KeyboardButton(text='/movie_genres_p1'),
        ]
    ],
    resize_keyboard=True,
)

MOVIE_GENRES_P1 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=f'/{GENRES_MOVIE_LIST[10]}'),
            KeyboardButton(text=f'/{GENRES_MOVIE_LIST[11]}'),
            KeyboardButton(text=f'/{GENRES_MOVIE_LIST[12]}'),
        ],
        [
            KeyboardButton(text=f'/{GENRES_MOVIE_LIST[13]}'),
            KeyboardButton(text=f'/{GENRES_MOVIE_LIST[14]}'),
            KeyboardButton(text=f'/{GENRES_MOVIE_LIST[15]}'),
        ],
        [
            KeyboardButton(text=f'/{GENRES_MOVIE_LIST[16]}'),
            KeyboardButton(text=f'/{GENRES_MOVIE_LIST[17]}'),
            KeyboardButton(text=f'/{GENRES_MOVIE_LIST[18]}'),
        ],
        [
            KeyboardButton(text='/menu'),
            KeyboardButton(text='/movie_genres'),
            KeyboardButton(text='/movie_genres_p2'),
        ]
    ],
    resize_keyboard=True,
)

MOVIE_GENRES_P2 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=f'/{GENRES_MOVIE_LIST[19]}'),
            KeyboardButton(text=f'/{GENRES_MOVIE_LIST[20]}'),
            KeyboardButton(text=f'/{GENRES_MOVIE_LIST[21]}'),
        ],
        [
            KeyboardButton(text='/menu'),
            KeyboardButton(text='/movie_genres_p1'),
        ]
    ],
    resize_keyboard=True,
)

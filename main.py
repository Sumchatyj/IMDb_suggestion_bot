from aiogram.utils import executor
from bot import dispatcher, handlers


from scrapper.IMDb_scrapper import get_genres


GENRES = []


async def on_startup(_):
    print("bot is online")
    GENRES = get_genres()


if __name__ == "__main__":
    executor.start_polling(
        dispatcher.dp, skip_updates=True, on_startup=on_startup
    )

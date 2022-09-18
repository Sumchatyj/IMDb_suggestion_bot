from aiogram.utils import executor
from bot import dispatcher


from scrapper.IMDb_scrapper import get_genres


GENRES = set()


async def on_startup(_):
    print("bot is online")
    GENRES = get_genres()


if __name__ == "__main__":
    executor.start_polling(
        dispatcher.dp, skip_updates=True, on_startup=on_startup
    )

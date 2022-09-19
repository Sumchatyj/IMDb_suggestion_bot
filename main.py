from aiogram.utils import executor
from bot import dispatcher


async def on_startup(_):
    print("bot is online")


if __name__ == "__main__":
    from bot import handlers
    executor.start_polling(
        dispatcher.dp, skip_updates=True, on_startup=on_startup
    )

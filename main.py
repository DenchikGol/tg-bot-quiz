import json

# import logging
from aiogram import Bot, Dispatcher, types

from callbacks import callback_router
from env import API_TOKEN
from handlers import handlers_router

# logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
dp.include_routers(handlers_router, callback_router)


async def process_event(event):
    update = types.Update.model_validate(
        json.loads(event["body"]), context={"bot": bot}
    )
    await dp.feed_update(bot, update)


async def yandex_main(event, context):
    if event["httpMethod"] == "POST":
        await process_event(event)
        return {"statusCode": 200, "body": "ok"}
    return {"statusCode": 405}

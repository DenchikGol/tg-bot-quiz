import asyncio

from aiogram import F, Router, types

from database import get_quiz_current_score, update_quiz_current_score
from utils import check_next_question

callback_router: Router = Router()


@callback_router.callback_query(F.data.startswith("qst-"))
async def right_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None,
    )
    calls_text = ["Верно", "Неверно"]
    calls_split = callback.data.split("-")
    user_id = callback.from_user.id
    current_score = await get_quiz_current_score(user_id)

    await callback.message.answer(calls_split[-1])
    await asyncio.sleep(1)

    if calls_split[1] == "right_answer":
        current_score += 1
        await update_quiz_current_score(user_id, current_score)
        await callback.message.answer(calls_text[0])
    else:
        await callback.message.answer(calls_text[1])

    await callback.message.answer(f"Правильных ответов {current_score}")
    await check_next_question(user_id, callback.message)


# @callback_router.callback_query(F.data.startswith("wrong_answer"))
# async def wrong_answer(callback: types.CallbackQuery):
#     await callback.bot.edit_message_reply_markup(
#         chat_id=callback.from_user.id,
#         message_id=callback.message.message_id,
#         reply_markup=None,
#     )
#     await callback.message.answer(callback.data.split("-")[-1])
#     current_question_index = await get_quiz_index(callback.from_user.id)
#     data = read_json(PATH_TO_JSON)
#     await asyncio.sleep(1)
#     await callback.message.answer(
#         f"Неправильно. Правильный ответ: {data['questions'][current_question_index]['right_answer']}"
#     )
#     await check_next_question(callback.from_user.id, callback.message)

from aiogram import F, Router, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from query_to_database import (
    get_quiz_best_score,
    get_quiz_index,
    get_quiz_length,
    update_quiz_current_score,
    update_quiz_index,
)
from utils import get_question

handlers_router: Router = Router()


# Хэндлер на команду /start
@handlers_router.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(
        types.KeyboardButton(text="Начать игру"),
        types.KeyboardButton(text="Продолжить игру"),
        types.KeyboardButton(text="Лучший счет"),
        types.KeyboardButton(text="Завершить квиз"),
    )
    await message.answer(
        "Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True)
    )


# Хэндлер на команду /quiz
@handlers_router.message(F.text == "Начать игру")
@handlers_router.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    await message.answer("Давайте начнем квиз!")
    await new_quiz(message)


# Хэндлер на команду /stop
@handlers_router.message(F.text == "Завершить квиз")
@handlers_router.message(Command("stop"))
async def cmd_stop_quiz(message: types.Message):
    await message.answer("Если захочешь начать с этого же места, нажми продолжить!")
    await stop_quiz(message)


# Хэндлер на команду /continue
@handlers_router.message(F.text == "Продолжить игру")
@handlers_router.message(Command("continue"))
async def cmd_continue_quiz(message: types.Message):
    await message.answer("Продолжаем...")
    current_index = await get_quiz_index(message.from_user.id)
    theme = "Исторические события."
    quiz_len = await get_quiz_length(theme)
    if quiz_len <= current_index:
        await new_quiz(message)
    else:
        await get_question(message, message.from_user.id, theme, quiz_len)


# Хэндлер на команду /score
@handlers_router.message(F.text == "Лучший счет")
@handlers_router.message(Command("score"))
async def cmd_score_quiz(message: types.Message):
    await message.answer(
        f"Лучший результат: {await get_quiz_best_score(message.from_user.id)}"
    )


async def new_quiz(message: types.Message):
    user_id = message.from_user.id
    current_question_index = 1
    theme = "Исторические события."
    quiz_len = await get_quiz_length(theme)
    await update_quiz_index(user_id, current_question_index)
    await update_quiz_current_score(user_id, 0)
    await get_question(message, user_id, theme, quiz_len)


async def stop_quiz(message: types.Message):
    pass

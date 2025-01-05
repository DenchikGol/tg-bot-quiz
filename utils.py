import json
import random

# import logging
from aiogram import types
from aiogram.utils.formatting import Bold, Text
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database import (
    get_quiz_best_score,
    get_quiz_current_score,
    get_quiz_index,
    update_quiz_best_score,
    update_quiz_index,
)
from env import PATH_TO_JSON


async def check_next_question(user_id: int, message: types.Message):
    current_question_index = await get_quiz_index(user_id)
    current_question_index += 1
    await update_quiz_index(user_id, current_question_index)
    # logging.warning(current_question_index)

    data = read_json(PATH_TO_JSON)
    if current_question_index < len(data["questions"]):
        await get_question(message, user_id)
    else:
        current_score = await get_quiz_current_score(user_id)
        await message.answer("Это был последний вопрос. Квиз завершен!")
        await message.answer(f"Вы набрали {current_score} из {len(data['questions'])}")
        best_score = await get_quiz_best_score(user_id)
        if current_score > best_score:
            await update_quiz_best_score(user_id, current_score)
            await message.answer("Вы обновили свой лучший результат!")


async def get_question(message: types.Message, user_id: int):
    current_question_index = await get_quiz_index(user_id)
    data = read_json(PATH_TO_JSON)
    question_data = data["questions"][current_question_index]
    answers = question_data["answers"]
    r_answer = question_data["right_answer"]
    kb = generate_options_keyboard(answers, r_answer)

    content = Text(
        Bold(f"Вопрос {current_question_index + 1} из {len(data['questions'])}!"),
        f"\n{question_data['question']}",
    )
    await message.answer(**content.as_kwargs(), reply_markup=kb)


def generate_options_keyboard(answer_options: list[str], right_answer: str):
    builder = InlineKeyboardBuilder()
    random.shuffle(answer_options)
    for option in answer_options:
        builder.add(
            types.InlineKeyboardButton(
                text=option,
                callback_data=f"qst-right_answer-{option}"
                if option == right_answer
                else f"qst-wrong_answer-{option}",
            )
        )

    builder.adjust(1)
    return builder.as_markup()


def read_json(path_to_json: str) -> dict:
    with open(path_to_json, "r", encoding="UTF-8") as file:
        data = json.load(file)
    return data

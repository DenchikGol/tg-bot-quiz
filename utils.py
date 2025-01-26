import random

# import logging
from aiogram import types
from aiogram.utils.formatting import Bold, Text
from aiogram.utils.keyboard import InlineKeyboardBuilder

from query_to_database import (
    get_question_row,
    get_quiz_best_score,
    get_quiz_current_score,
    get_quiz_index,
    get_quiz_length,
    update_quiz_best_score,
    update_quiz_index,
)


async def check_next_question(user_id: int, message: types.Message):
    current_question_index = await get_quiz_index(user_id)
    current_question_index += 1
    await update_quiz_index(user_id, current_question_index)
    # logging.warning(current_question_index)
    theme = "Исторические события."
    quiz_length = await get_quiz_length(theme)

    if current_question_index < quiz_length:
        await get_question(message, user_id, theme, quiz_length)
    else:
        current_score = await get_quiz_current_score(user_id)
        await message.answer("Это был последний вопрос. Квиз завершен!")
        await message.answer(f"Вы набрали {current_score} из {quiz_length}")
        best_score = await get_quiz_best_score(user_id)
        if current_score > best_score:
            await update_quiz_best_score(user_id, current_score)
            await message.answer("Вы обновили свой лучший результат!")


async def get_question(message: types.Message, user_id: int, theme: str, quiz_len: int):
    current_question_index = await get_quiz_index(user_id)
    data_row = await get_question_row(current_question_index, theme)
    question_data = data_row["question"]
    answers = data_row["answers"].split(";")
    r_answer = data_row["right_answer"]
    kb = generate_options_keyboard(answers, r_answer)

    content = Text(
        Bold(f"Вопрос {current_question_index + 1} из {quiz_len}!"),
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


# def read_json(path_to_json: str) -> dict:
#     with open(path_to_json, "r", encoding="UTF-8") as file:
#         data = json.load(file)
#     return data

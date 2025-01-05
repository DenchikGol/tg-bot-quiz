import logging

import aiosqlite

from env import DB_NAME


async def create_table():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER, current_score INTEGER, best_score INTEGER)"""
        )
        await db.commit()


async def get_quiz_index(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT question_index FROM quiz_state WHERE user_id = (?)", (user_id,)
        ) as cursor:
            result = await cursor.fetchone()
            if result[0] is not None:
                return result[0]
            else:
                logging.warning(f"Пользователь {user_id} не найден")
                return 1


async def update_quiz_index(user_id: int, index: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "UPDATE quiz_state SET question_index = (?) WHERE user_id = (?)",
            (index, user_id),
        )
        await db.commit()


async def get_quiz_best_score(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT best_score FROM quiz_state WHERE user_id = (?)", (user_id,)
        ) as cursor:
            result = await cursor.fetchone()
            if result[0] is not None:
                return result[0]
            else:
                return 0


async def update_quiz_best_score(user_id: int, best_score: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "UPDATE quiz_state SET best_score = (?) WHERE user_id = (?)",
            (best_score, user_id),
        )
        await db.commit()


async def get_quiz_current_score(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT current_score FROM quiz_state WHERE user_id = (?)", (user_id,)
        ) as cursor:
            result = await cursor.fetchone()
            if result[0] is not None:
                return result[0]
            else:
                return 0


async def update_quiz_current_score(user_id: int, current_score: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "UPDATE quiz_state SET current_score = (?) WHERE user_id = (?)",
            (current_score, user_id),
        )

        await db.commit()

from database import execute_select_query, execute_update_query, pool
from env import YDB_TABLE_QUESTIONS, YDB_TABLE_USER


async def get_quiz_index(user_id):
    get_user_index = f"""
        DECLARE $user_id AS Uint64;

        SELECT question_index
        FROM `{YDB_TABLE_USER}`
        WHERE user_id == $user_id;
    """
    results = execute_select_query(pool, get_user_index, user_id=user_id)

    if len(results) == 0:
        return 0
    if results[0]["question_index"] is None:
        return 0
    return results[0]["question_index"]


async def update_quiz_index(user_id, question_index):
    set_quiz_state = f"""
        DECLARE $user_id AS Uint64;
        DECLARE $question_index AS Uint64;

        UPSERT INTO `{YDB_TABLE_USER}` (`user_id`, `question_index`)
        VALUES ($user_id, $question_index);
    """

    execute_update_query(
        pool,
        set_quiz_state,
        user_id=user_id,
        question_index=question_index,
    )


async def get_quiz_best_score(user_id: int):
    get_user_best_score = f"""
        DECLARE $user_id AS Uint64;

        SELECT best_score
        FROM `{YDB_TABLE_USER}`
        WHERE user_id == $user_id;
    """
    results = execute_select_query(pool, get_user_best_score, user_id=user_id)

    if (len(results) == 0) or (results[0]["best_score"] is None):
        return 0
    return results[0]["best_score"]


async def update_quiz_best_score(user_id: int, best_score: int):
    set_quiz_best_score = f"""
        DECLARE $user_id AS Uint64;
        DECLARE $best_score AS Uint64;

        UPSERT INTO `{YDB_TABLE_USER}` (`user_id`, `best_score`)
        VALUES ($user_id, $best_score);
    """

    execute_update_query(
        pool,
        set_quiz_best_score,
        user_id=user_id,
        best_score=best_score,
    )


async def get_quiz_current_score(user_id: int):
    get_user_current_score = f"""
        DECLARE $user_id AS Uint64;

        SELECT current_score
        FROM `{YDB_TABLE_USER}`
        WHERE user_id == $user_id;
    """
    results = execute_select_query(pool, get_user_current_score, user_id=user_id)

    if (len(results) == 0) or (results[0]["current_score"] is None):
        return 0
    return results[0]["current_score"]


async def update_quiz_current_score(user_id: int, current_score: int):
    set_quiz_current_score = f"""
        DECLARE $user_id AS Uint64;
        DECLARE $current_score AS Uint64;

        UPSERT INTO `{YDB_TABLE_USER}` (`user_id`, `current_score`)
        VALUES ($user_id, $current_score);
    """

    execute_update_query(
        pool,
        set_quiz_current_score,
        user_id=user_id,
        current_score=current_score,
    )


async def get_question_row(question_index: int, theme: str = "Исторические события."):
    query_to_get_question = f"""
        DECLARE $question_index AS Uint64;
        DECLARE $theme AS Utf8;

        SELECT *
        FROM `{YDB_TABLE_QUESTIONS}`
        WHERE question_index == $question_index AND theme == theme;
        """
    result_row = execute_select_query(
        pool, query_to_get_question, question_index, theme
    )
    return result_row[0]


async def get_quiz_length(theme: str):
    query_to_get_length = f"""
    DECLARE $theme AS Utf8;
    
    SELECT COUNT(*) AS length FROM {YDB_TABLE_QUESTIONS} WHERE theme == $theme"
    """

    result = execute_select_query(pool, query_to_get_length, theme)
    return result[0]["length"]

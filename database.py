import ydb

from env import (
    YDB_DATABASE,
    YDB_ENDPOINT,
    YDB_TABLE_QUESTIONS,
    YDB_TABLE_USER,
)


async def create_tables(pool: ydb.aio.SessionPool):
    await pool.execute_with_retries(
        f"""
        CREATE TABLE IF NOT EXIST `{YDB_TABLE_USER}` (
            `user_id` Uint64,
            `question_index` Uint64,
            `current_score` Uint64,
            `best_score` Uint64,
            PRIMARY KEY (`user_id`)
        )
        """
    )

    pool.execute_with_retries(
        f"""
        CREATE TABLE IF NOT EXIST `{YDB_TABLE_QUESTIONS}` (
            `question_id` Uint64,
            `question_index` Uint64,
            `question` Utf8,
            `right_answer` Utf8,
            `answers` List<Int32>,
            `theme` Utf8,
            PRIMARY KEY (`question_id`)
        )
        """
    )


def get_ydb_pool(ydb_endpoint, ydb_database, timeout=30):
    ydb_driver_config = ydb.DriverConfig(
        ydb_endpoint,
        ydb_database,
        credentials=ydb.credentials_from_env_variables(),
        root_certificates=ydb.load_ydb_root_certificate(),
    )

    ydb_driver = ydb.Driver(ydb_driver_config)
    ydb_driver.wait(fail_fast=True, timeout=timeout)
    return ydb.SessionPool(ydb_driver)


def _format_kwargs(kwargs: dict):
    return {"${}".format(key): value for key, value in kwargs.items()}


def execute_update_query(pool, query, **kwargs):
    def callee(session):
        prepared_query = session.prepare(query)
        session.transaction(ydb.SerializableReadWrite()).execute(
            prepared_query, _format_kwargs(kwargs), commit_tx=True
        )

    return pool.retry_operation_sync(callee)


def execute_select_query(pool: ydb.SessionPool, query: str, **kwargs):
    def callee(session):
        prepared_query = session.prepare(query)
        result_sets = session.transaction(ydb.SerializableReadWrite()).execute(
            prepared_query, _format_kwargs(kwargs), commit_tx=True
        )
        return result_sets[0].rows

    return pool.retry_operation_sync(callee)


# Зададим настройки базы данных
pool = get_ydb_pool(YDB_ENDPOINT, YDB_DATABASE)

import ydb

from env import YDB_DATABASE_NAME, YDB_ENDPOINT, YDB_TABLE_QUESTIONS, YDB_TABLE_USER


async def create_tables(pool: ydb.aio.QuerySessionPool):
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

    await pool.execute_with_retries(
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


async def get_ydb_pool(ydb_endpoint: str, ydb_database: str, timeout=30):
    ydb_driver_config = ydb.DriverConfig(
        ydb_endpoint,
        ydb_database,
        credentials=ydb.credentials_from_env_variables(),
        root_certificates=ydb.load_ydb_root_certificate(),
    )
    async with ydb.aio.Driver(driver_config=ydb_driver_config) as driver:
        try:
            await driver.wait(fail_fast=True, timeout=timeout)
        except TimeoutError:
            print("Connect failed to YDB")
            print("Last reported errors by discovery:")
            print(driver.discovery_debug_details())
            exit(1)

        return ydb.aio.QuerySessionPool(driver)


def _format_kwargs(kwargs: dict):
    return {"${}".format(key): value for key, value in kwargs.items()}


async def execute_update_query(pool: ydb.aio.QuerySessionPool, query: str, **kwargs):
    async def callee(session: ydb.aio.QuerySession):
        await session.transaction(ydb.SerializableReadWrite()).execute(
            query=query, parameters=_format_kwargs(kwargs), commit_tx=True
        )

    return await pool.retry_operation_async(callee)


async def execute_select_query(pool: ydb.aio.QuerySessionPool, query: str, **kwargs):
    async def callee(session: ydb.aio.QuerySession):
        async with session.transaction(ydb.SerializableReadWrite()).execute(
            query=query, parameters=_format_kwargs(kwargs), commit_tx=True
        ) as result_sets:
            return result_sets[0].rows

    return await pool.retry_operation_async(callee)


pool = get_ydb_pool(YDB_ENDPOINT, YDB_DATABASE_NAME)

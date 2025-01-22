from dotenv import dotenv_values

config = dotenv_values(".env")
PATH_TO_JSON: str = config["PATH_TO_JSON"]
API_TOKEN: str = config["API_TOKEN"]
DB_NAME: str = config["DB_NAME"]
YDB_ENDPOINT: str = config["YDB_ENDPOINT"]
YDB_DATABASE: str = config["YDB_DATABASE"]
YDB_DATABASE_NAME: str = config["YDB_DATABASE_NAME"]
YDB_TABLE_QUESTIONS: str = config["YDB_TABLE_QUESTIONS"]
YDB_TABLE_USER: str = config["YDB_TABLE_USER"]

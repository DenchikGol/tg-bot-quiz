from dotenv import dotenv_values

config = dotenv_values(".env")
PATH_TO_JSON: str = config["PATH_TO_JSON"]
API_TOKEN: str = config["API_TOKEN"]
DB_NAME: str = config["DB_NAME"]

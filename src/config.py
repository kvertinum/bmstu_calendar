import os
from dotenv import load_dotenv


load_dotenv()

LIST_API_URL = "https://lks.bmstu.ru/lks-back/api/v1/structure"
GROUP_API_URL = "https://lks.bmstu.ru/lks-back/api/v1/schedules/groups/{group_id}/public"

TG_TOKEN = os.getenv("TG_BOT_TOKEN")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
DB_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db/{POSTGRES_DB}"

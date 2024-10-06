import dotenv
import os

dotenv.load_dotenv()

db_type = os.environ.get("DB_TYPE", "postgres")
db_user = os.environ["DB_USER"]
db_password = os.environ["DB_PASSWORD"]
db_host = os.environ["DB_HOST"]
db_port = os.environ["DB_PORT"]
db_database = os.environ["DB_DB"]
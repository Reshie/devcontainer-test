from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from google.cloud.sql.connector import Connector
import pg8000
from dotenv import load_dotenv
import os

### when using docker-compose ###
# engine = create_engine('postgresql://postgres:postgres@docker_workspace_devcontainer-db-1:5432/postgres')

load_dotenv()

db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
db_name = os.getenv("DB_NAME")
instance_connection_name = os.getenv("INSTANCE_CONNECTION_NAME")

connector = Connector()

def getconn() -> pg8000.dbapi.Connection:
    print(db_name)
    conn: pg8000.dbapi.Connection = connector.connect(
        instance_connection_name,
        "pg8000",
        user=db_user,
        password=db_pass,
        db=db_name,
    )
    return conn

engine = create_engine("postgresql+pg8000://", creator=getconn)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
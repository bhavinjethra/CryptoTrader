import os
import sqlalchemy as db

from dotenv import find_dotenv, load_dotenv
from sqlalchemy.orm import sessionmaker

load_dotenv(find_dotenv(raise_error_if_not_found=True))

# Load DB Parameters
host = os.getenv("DB_HOST")
user = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_DATABASE")
port = os.getenv("DB_PORT")

# Connection String
conn_string = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'

# Connect to Database
print(conn_string)
engine = db.create_engine(conn_string, echo=True)

# Obtain a session
Session = sessionmaker(bind=engine)
session = Session()

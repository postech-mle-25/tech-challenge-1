import os
from sqlmodel import Session, SQLModel, create_engine

# 🧠 Caminho absoluto para o arquivo dentro do próprio app
base_dir = os.path.dirname(__file__)
sqlite_file_name = os.path.join(base_dir, "database.db")
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

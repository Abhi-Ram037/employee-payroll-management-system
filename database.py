from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

database_url = "sqlite:///./employee_payroll.db"

engine = create_engine(
    database_url,
    connect_args={"check_same_thread": False}
)

session_local = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

base = declarative_base()


def get_db():
    db = session_local()

    try:
        yield db
    finally:
        db.close()
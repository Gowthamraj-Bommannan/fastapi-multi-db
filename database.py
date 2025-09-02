from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL_A = "postgresql+psycopg://gowthamraj:root@localhost:5433/company_a"
DATABASE_URL_B = "postgresql+psycopg://gowthamraj:root@localhost:5433/company_b"

engine_a = create_engine(DATABASE_URL_A)
engine_b = create_engine(DATABASE_URL_B)

SessionLocal_A = sessionmaker(autocommit=False, autoflush=False, bind=engine_a)
SessionLocal_B = sessionmaker(autocommit=False, autoflush=False, bind=engine_b)

Base = declarative_base()

def get_db(company: str):
    if company == "company_a":
        db = SessionLocal_A()
    elif company == "company_b":
        db = SessionLocal_B()
    else:
        raise ValueError("Invalid company")
    try:
        yield db
    finally:
        db.close()
# app/database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Для Docker-сборки, ищем DATABASE_URL в переменных окружения
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///../test.db")

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

Base = declarative_base()

import os
from sqlalchemy import create_engine

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("❌ DATABASE_URL environment variable not set")

engine = create_engine(DATABASE_URL, echo=False)

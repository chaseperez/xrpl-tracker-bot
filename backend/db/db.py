import os
from sqlalchemy import create_engine

# Read the DATABASE_URL from environment variables
DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("❌ DATABASE_URL environment variable not set")

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=False)

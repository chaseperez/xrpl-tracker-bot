from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from os import getenv
from sqlalchemy import create_engine



#Delete code if no worky
DATABASE_URL = getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
#delete code late if doesnt work^^^^^


# ✅ Get the DATABASE_URL from environment variables
DATABASE_URL = getenv("DATABASE_URL")

# ❗ Throw an error if it's not set (optional safety check)
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set!")

# ✅ Create the engine
engine = create_engine(DATABASE_URL, echo=False)

# ✅ (Optional) Create a sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

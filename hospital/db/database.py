from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database file will be created at the project root, called hospital.db
DATABASE_URL = "sqlite:///hospital.db"

engine = create_engine(DATABASE_URL, echo=False)
# echo=True would print every SQL statement SQLAlchemy runs — useful for
# learning/debugging, but noisy. Flip it to True later if you want to SEE
# the actual SQL being generated.

SessionLocal = sessionmaker(bind=engine)

# Base is what all our table-mapped classes will inherit from.
Base = declarative_base()
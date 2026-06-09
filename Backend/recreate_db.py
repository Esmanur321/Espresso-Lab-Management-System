from database import engine, Base
from models import *

# Drop all tables
Base.metadata.drop_all(bind=engine)

# Recreate all tables
Base.metadata.create_all(bind=engine)

print("Database tables dropped and recreated successfully.")

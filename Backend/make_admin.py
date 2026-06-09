# -*- coding: utf-8 -*-
"""
Make an existing user an administrator.

Usage (from Backend folder):
  .\.venv\Scripts\python.exe make_admin.py admin@espressolab.com
"""
import sys
from database import SessionLocal
from models import User

if len(sys.argv) < 2:
    print("Usage: python make_admin.py <email>")
    sys.exit(1)

email = sys.argv[1].strip()
db = SessionLocal()
user = db.query(User).filter(User.email == email).first()
if not user:
    print(f"User not found: {email}")
    sys.exit(1)

user.is_admin = True
db.commit()
print(f"OK: {email} is now admin (id={user.id})")
db.close()

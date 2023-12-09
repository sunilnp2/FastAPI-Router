from packages.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()
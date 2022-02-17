from .db.session import SessionLocal
import logging


def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        logging.error('Could not write to DB')
        db.rollback()
        raise
    finally:
        db.close()

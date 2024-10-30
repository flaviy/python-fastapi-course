from .database import SessionLocal


def get_db():
    # this function will return the session that we will use to interact with the database
    db = SessionLocal()
    try:
        # we yield the session to the route that needs it, we use generator
        # instead of return to avoid closing the session each time we use it
        # this way we can use the session multiple times
        # finally will always run after the route is done
        yield db
    finally:
        db.close()
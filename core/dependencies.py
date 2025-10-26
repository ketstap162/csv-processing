from db.session import session, SessionCreator
from fastapi import Depends

def get_session():
    def dependency() -> SessionCreator:
        return session
    return Depends(dependency)

import re
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import inspect
from starlette import status


def camel_to_snake(name):
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    name = re.sub("__([A-Z])", r"_\1", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def get_now():
    """Return default now"""
    # if TimeZone.IS_ACTIVE:
    #     return datetime.now(TimeZone.DATETIME_TZ)
    return datetime.now()


def check_loaded(instance, attr_name: str):
    """
    Checks if a relationship attribute is loaded on the given instance.
    Raises an HTTPException if not loaded.
    """
    state = inspect(instance)
    if attr_name not in state.unloaded:
        return
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Relationship '{attr_name}' is not eagerly loaded for {type(instance).__name__}.",
    )

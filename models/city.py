#!/usr/bin/python3
"""Contains City class"""
from models.base_model import BaseModel


class City(BaseModel):
    """Representation of a city"""
    state_id = ""
    name = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

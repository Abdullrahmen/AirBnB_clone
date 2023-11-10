#!/usr/bin/python3
"""Contains State class"""
from models.base_model import BaseModel


class State(BaseModel):
    """Representation of a state"""
    name = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

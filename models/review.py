#!/usr/bin/python3
"""Contains Review class"""
from models.base_model import BaseModel


class Review(BaseModel):
    """Representation of a review"""
    place_id = ""
    user_id = ""
    test = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

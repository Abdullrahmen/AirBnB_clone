#!/usr/bin/python3
"""Contains Amenity class"""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """Representation of a amenity"""
    name = ""

    def __init__(self, *args, **kwargs):
        """init function for the class"""
        super().__init__(*args, **kwargs)

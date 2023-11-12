#!/usr/bin/python3
"""
Contains BaseModel class
"""

import models
from datetime import datetime
import uuid


class BaseModel:
    """The BaseModel class which all future classes will be derived"""
    def __init__(self, *args, **kwargs):
        """init method for the BaseModel class"""
        if (kwargs):
            self.__dict__ = kwargs
            del self.__dict__["__class__"]
            self.updated_at = datetime.strptime(self.updated_at,
                                                "%Y-%m-%dT%H:%M:%S.%f")
            self.created_at = datetime.strptime(self.created_at,
                                                "%Y-%m-%dT%H:%M:%S.%f")
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
            models.storage.new(self)

    def __str__(self):
        """The string of the object"""
        s = f"[{self.__class__.__name__}] ({self.id}) <{self.__dict__}>"
        return (s)

    def save(self):
        """updates the public instance attribute updated_at with
        the current datetime"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """returns a dictionary containing all keys/values of __dict__
        of the instance"""
        dict_ = self.__dict__.copy()
        dict_["__class__"] = self.__class__.__name__
        dict_["created_at"] = self.created_at.isoformat()
        dict_["updated_at"] = self.updated_at.isoformat()
        return (dict_)

#!/usr/bin/python3
"""
Define the BaseModel class.
"""
import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """Represents the BaseModel of the HBnB project."""

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel.
        Args:
            *args (any): To be used.
            **kwargs (dict): Key or value pairs of attributes.
        """
        timeFormat = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        if len(kwargs) != 0:
            for k, v in kwargs.items():
                if k == "created_at" or k == "updated_at":
                    self.__dict__[k] = datetime.strptime(v, timeFormat)
                else:
                    self.__dict__[k] = v
        else:
            models.storage.new(self)

    def save(self):
        """Update updated_at with the current datetime."""
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """
        Return the dictionary of the BaseModel.

        Including the key or value pair __class__ name.
        """
        returnDictionary = self.__dict__.copy()
        returnDictionary["created_at"] = self.created_at.isoformat()
        returnDictionary["updated_at"] = self.updated_at.isoformat()
        returnDictionary["__class__"] = self.__class__.__name__
        return returnDictionary

    def __str__(self):
        """
        Return the string representation of the BaseModel.
        """
        className = self.__class__.__name__
        return "[{}] ({}) {}".format(className, self.id, self.__dict__)

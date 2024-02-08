#!/usr/bin/python3
"""
Define the AirBnB clone Console
"""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


def parser(arg):
    curly_brackets = re.search(r"\{(.*?)\}", arg)
    square_brackets = re.search(r"\[(.*?)\]", arg)
    if curly_brackets is None:
        if square_brackets is None:
            return [x.strip(",") for x in split(arg)]
        else:
            lexicon = split(arg[:square_brackets.span()[0]])
            return_line = [x.strip(",") for x in lexicon]
            return_line.append(square_brackets.group())
            return return_line
    else:
        lexicon = split(arg[:curly_brackets.span()[0]])
        return_line = [x.strip(",") for x in lexicon]
        return_line.append(curly_brackets.group())
        return return_line
class HBNBCommand(cmd.Cmd):
    """
    Defines the AirBnB Clone command interpreter.

    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

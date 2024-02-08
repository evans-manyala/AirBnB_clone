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
            re.search = [x.strip(",") for x in lexicon]
            re.search.append(square_brackets.group())
            return re.search
    else:
        lexicon = split(arg[:curly_brackets.span()[0]])
        re.search = [x.strip(",") for x in lexicon]
        re.search.append(curly_brackets.group())
        return re.search


class AirBnBCommand(cmd.Cmd):
    """
    Defines the AirBnB Clone cmd interpreter.

    Attributes:
        prompt (str): The cmd prompt.
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

    def emptyline(self):
        """
        Do nothing when the prompt is empty without any input.
        """
        pass

    def default(self, arg):
        """
        Define behavior for command module when
        the input from the user is not valid
        """
        arg_dict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            arg_list = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", arg_list[1])
            if match is not None:
                cmd = [arg_list[1][:match.span()[0]], match.group()[1:-1]]
                if cmd[0] in arg_dict.keys():
                    call = "{} {}".format(arg_list[0], cmd[1])
                    return arg_dict[cmd[0]](call)
        print("*** Unknown format: {}".format(arg))
        return False

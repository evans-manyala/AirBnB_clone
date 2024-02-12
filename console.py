#!/usr/bin/python3
"""
Define the AirBnB clone Console
"""
import cmd
import re
from shlex import split
from models.base_model import BaseModel
from models import storage
import models.city
import models.amenity
import models.place
import models.review
import models.state
import models.user


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


class HBNBCommand(cmd.Cmd):
    """
    Defines the AirBnB Clone cmd interpreter.

    Attributes:
        prompt (string): The cmd prompt.
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

    def exit(self, arg):
        """
        Command to quit or exit the program.
        """
        return True

    def EOF(self, arg):
        """
        Process signal to quit the program reaches end of file.
        """
        print("")
        return True

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
            "all": self.doAll,
            "show": self.doShow,
            "destroy": self.doDestroy,
            "count": self.doCount,
            "update": self.doUpdate
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

    def doCreate(self, arg):
        """
        Creates a new instance of a class with a unique ID.
        """
        arg_list = parser(arg)
        if len(arg_list) == 0:
            print("** class name missing **")
        elif arg_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(arg_list[0])().id)
            storage.save()

    def doShow(self, arg):
        """
        Shows the string composition of a class with a unique ID.
        """
        arg_list = parser(arg)
        obj_dict = storage.all()
        if len(arg_list) == 0:
            print("** class name missing **")
        elif arg_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg_list) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_list[0], arg_list[1]) not in obj_dict:
            print("** no instance found **")
        else:
            print(obj_dict["{}.{}".format(arg_list[0], arg_list[1])])

    def doDestroy(self, arg):
        """
        Deletes an instance with a unique ID.
        """
        arg_list = parser(arg)
        obj_dict = storage.all()
        if len(arg_list) == 0:
            print("** class name missing **")
        elif arg_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg_list) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_list[0], arg_list[1]) not in obj_dict.keys():
            print("** no instance found **")
        else:
            del obj_dict["{}.{}".format(arg_list[0], arg_list[1])]
            storage.save()

    def doAll(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        arg_list = parser(arg)
        if len(arg_list) > 0 and arg_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(arg_list) > 0 and arg_list[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(arg_list) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def doCount(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        arg_list = parser(arg)
        count = 0
        for obj in storage.all().values():
            if arg_list[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def doUpdate(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        arg_list = parser(arg)
        obj_dict = storage.all()

        if len(arg_list) == 0:
            print("** Class name missing **")
            return False
        if arg_list[0] not in HBNBCommand.__classes:
            print("** Class does not exist **")
            return False
        if len(arg_list) == 1:
            print("** Instance uniqueID missing **")
            return False
        if "{}.{}".format(arg_list[0], arg_list[1]) not in obj_dict.keys():
            print("** No instance found **")
            return False
        if len(arg_list) == 2:
            print("** Attribute name missing **")
            return False
        if len(arg_list) == 3:
            try:
                type(eval(arg_list[2])) != dict
            except NameError:
                print("** Value missing **")
                return False

        if len(arg_list) == 4:
            obj = obj_dict["{}.{}".format(arg_list[0], arg_list[1])]
            if arg_list[2] in obj.__class__.__dict__.keys():
                valueType = type(obj.__class__.__dict__[arg_list[2]])
                obj.__dict__[arg_list[2]] = valueType(arg_list[3])
            else:
                obj.__dict__[arg_list[2]] = arg_list[3]
        elif type(eval(arg_list[2])) == dict:
            obj = obj_dict["{}.{}".format(arg_list[0], arg_list[1])]
            for k, v in eval(arg_list[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valueType = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valueType(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
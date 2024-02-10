#!/usr/bin/python3
"""
Class defintion for unittests


Unittest classes:

    TestAirBnBCommand_create
    TestAirBnBCommand_update
    TestAirBnBCommand_all
    TestAirBnBCommand_prompt
    TestAirBnBCommand_destroy
    TestAirBnBCommand_exit
    TestAirBnBCommand_show
"""
import os
import sys
import unittest
from console import AirBnBCommand
from models import storage
from models.engine import FileStorage
from io import StringIO
from unittest.mock import patch


class TestAirBnBCommand_prompt(unittest.TestCase):
    """
    Unit tests for checking the prompt of the cmd interpreter.
    """

    def test_prompt_string(self):
        self.assertEqual("(hbnb) ", AirBnBCommand.prompt)

    def test_empty_line(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd(""))
            self.assertEqual("", output.getvalue().strip())


class TestAirBnBCommand_exit(unittest.TestCase):
    """
    Unit tests for checking if exiting from
    the cmd interpreter works.
    """

    def test_quit_exits(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertTrue(AirBnBCommand().onecmd("quit"))

    def test_EOF_exits(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertTrue(AirBnBCommand().onecmd("EOF"))


class TestAirBnBCommand_help(unittest.TestCase):
    """
    Unit tests for checking for if help
    messages on the cmd interpreter works.
    """

    def testHelpExit(self):
        _p = "Quit command to exit the program."
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("help quit"))
            self.assertEqual(_p, output.getvalue().strip())

    def testHelpCreate(self):
        _p = ("Usage: create <class>\n""Create a new class with a unique id.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("help create"))
            self.assertEqual(_p, output.getvalue().strip())

    def testHelpEOF(self):
        _p = "Signal to quit the program."
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("help EOF"))
            self.assertEqual(_p, output.getvalue().strip())

    def testHelpShow(self):
        _p = ("Usage: show <class> <id> or <class>.show(<id>)\n"
              "Show string depiction of a class instance with"" a unique id.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("help show"))
            self.assertEqual(_p, output.getvalue().strip())

    def testHelpDestroy(self):
        _p = ("Usage: destroy <class> <id> or <class>.destroy(<id>)\n"
              "Delete a class instance with a unique id.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("help destroy"))
            self.assertEqual(_p, output.getvalue().strip())

    def testHelpAll(self):
        _p = ("Usage: all or all <class> or <class>.all()\n"
              "Show string depiction of all instances of a class"
              ".\nIf no class is specified, displays all instances of"
              "objects.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("help all"))
            self.assertEqual(_p, output.getvalue().strip())

    def testHelpCount(self):
        _p = ("Usage: count <class> or <class>.count()\n        "
              "Retrieve the number of instances of a given class.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("help count"))
            self.assertEqual(_p, output.getvalue().strip())

    def testHelpUpdate(self):
        _p = ("Usage: update <class> <id> <attribute_name> <attribute_value>or"
              "\n   <class>.update(<id>, <attribute_name>, <attribute_value"
              ">) or\n       <class>.update(<id>, <dictionary>)\n        "
              "Update a class instance of a unique id by adding or updating\n"
              "a given attribute key/value pair or dictionary.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("help update"))
            self.assertEqual(_p, output.getvalue().strip())

    def TestHelp(self):
        _p = ("Documented commands (type help <topic>):\n"
              "****************************************\n"
              "EOF  all  count  create  destroy  help  quit  show  update")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("help"))
            self.assertEqual(_p, output.getvalue().strip())

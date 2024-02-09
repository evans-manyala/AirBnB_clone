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


class AirBnBCommand_prompt(unittest.TestCase):
    """Unittests for testing prompting of the HBNB command interpreter."""

    def test_prompt_string(self):
        self.assertEqual("(hbnb) ", AirBnBCommand.prompt)

    def test_empty_line(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd(""))
            self.assertEqual("", output.getvalue().strip())

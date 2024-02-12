#!/usr/bin/python3
"""
Class defintion for unit tests


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

    def testPromptString(self):
        self.assertEqual("(hbnb) ", AirBnBCommand.prompt)

    def testEmptyLine(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd(""))
            self.assertEqual("", output.getvalue().strip())


class TestAirBnBCommand_exit(unittest.TestCase):
    """
    Unit tests for checking if exiting from
    the cmd interpreter works.
    """

    def testQuitExit(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertTrue(AirBnBCommand().onecmd("quit"))

    def testEOFExit(self):
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


class TestAirBnBCommand_create(unittest.TestCase):
    """
    Unit tests for testing CREATE option of the cmd interpreter.
    """

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def testCreateMissingClass(self):
        correct = "** Missing class name **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create"))
            self.assertEqual(correct, output.getvalue().strip())

    def testCreateInvalidClass(self):
        correct = "** class does not exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create MyModel"))
            self.assertEqual(correct, output.getvalue().strip())

    def testCreateInvalidSyntax(self):
        correct = "*** Incorrect syntax: MyModel.create()"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("MyModel.create()"))
            self.assertEqual(correct, output.getvalue().strip())
        correct = "*** Incorrect syntax: BaseModel.create()"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("BaseModel.create()"))
            self.assertEqual(correct, output.getvalue().strip())

    def testCreateObject(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create BaseModel"))
            self.assertLess(0, len(output.getvalue().strip()))
            testKey = "BaseModel.{}".format(output.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create User"))
            self.assertLess(0, len(output.getvalue().strip()))
            testKey = "User.{}".format(output.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create State"))
            self.assertLess(0, len(output.getvalue().strip()))
            testKey = "State.{}".format(output.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create City"))
            self.assertLess(0, len(output.getvalue().strip()))
            testKey = "City.{}".format(output.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create Amenity"))
            self.assertLess(0, len(output.getvalue().strip()))
            testKey = "Amenity.{}".format(output.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create Place"))
            self.assertLess(0, len(output.getvalue().strip()))
            testKey = "Place.{}".format(output.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create Review"))
            self.assertLess(0, len(output.getvalue().strip()))
            testKey = "Review.{}".format(output.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())


class TestAirBnBCommand_show(unittest.TestCase):
    """
    Unit tests for testing SHOW option of the cmd interpreter
    """

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def testShowMissingClass(self):
        correct = "** Missing class name **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("show"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd(".show()"))
            self.assertEqual(correct, output.getvalue().strip())

    def testShowInvalidClass(self):
        correct = "** class does not exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("show MyModel"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("MyModel.show()"))
            self.assertEqual(correct, output.getvalue().strip())

    def testShowMissingID_space(self):
        correct = "** Class Class Class instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("show BaseModel"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("show User"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("show State"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("show City"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("show Amenity"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("show Place"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("show Review"))
            self.assertEqual(correct, output.getvalue().strip())

    def testShowMissingID_dot(self):
        correct = "** Class Class Class instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("BaseModel.show()"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("User.show()"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("State.show()"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("City.show()"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("Amenity.show()"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("Place.show()"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("Review.show()"))
            self.assertEqual(correct, output.getvalue().strip())

    def testShowNoInstanceFoundSpaceNotation(self):
        correct = "** No matching instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("show BaseModel 1"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("show User 1"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("show State 1"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("show City 1"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("show Amenity 1"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("show Place 1"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("show Review 1"))
            self.assertEqual(correct, output.getvalue().strip())

    def testShowNoInstanceFoundDotSpaceNotation(self):
        correct = "** No matching instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("BaseModel.show(1)"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("User.show(1)"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("State.show(1)"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("City.show(1)"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("Amenity.show(1)"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("Place.show(1)"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("Review.show(1)"))
            self.assertEqual(correct, output.getvalue().strip())

    def testShowObjSpaceNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create BaseModel"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["BaseModel.{}".format(test_ID)]
            command = "show BaseModel {}".format(test_ID)
            self.assertFalse(AirBnBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create User"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["User.{}".format(test_ID)]
            command = "show User {}".format(test_ID)
            self.assertFalse(AirBnBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create State"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["State.{}".format(test_ID)]
            command = "show State {}".format(test_ID)
            self.assertFalse(AirBnBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create Place"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Place.{}".format(test_ID)]
            command = "show Place {}".format(test_ID)
            self.assertFalse(AirBnBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create City"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["City.{}".format(test_ID)]
            command = "show City {}".format(test_ID)
            self.assertFalse(AirBnBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create Amenity"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Amenity.{}".format(test_ID)]
            command = "show Amenity {}".format(test_ID)
            self.assertFalse(AirBnBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create Review"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Review.{}".format(test_ID)]
            command = "show Review {}".format(test_ID)
            self.assertFalse(AirBnBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())

    def testShowObjSpaceNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create BaseModel"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["BaseModel.{}".format(test_ID)]
            command = "BaseModel.show({})".format(test_ID)
            self.assertFalse(AirBnBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create User"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["User.{}".format(test_ID)]
            command = "User.show({})".format(test_ID)
            self.assertFalse(AirBnBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create State"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["State.{}".format(test_ID)]
            command = "State.show({})".format(test_ID)
            self.assertFalse(AirBnBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create Place"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Place.{}".format(test_ID)]
            command = "Place.show({})".format(test_ID)
            self.assertFalse(AirBnBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create City"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["City.{}".format(test_ID)]
            command = "City.show({})".format(test_ID)
            self.assertFalse(AirBnBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create Amenity"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Amenity.{}".format(test_ID)]
            command = "Amenity.show({})".format(test_ID)
            self.assertFalse(AirBnBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create Review"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Review.{}".format(test_ID)]
            command = "Review.show({})".format(test_ID)
            self.assertFalse(AirBnBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())


class TestAirBnBCommand_destroy(unittest.TestCase):
    """
    Unit testing for DESTROY option in cmd interpreter.
    """

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        storage.reload()

    def testDestroyMissingClass(self):
        correct = "** Missing class name  **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("destroy"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd(".destroy()"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_destroy_invalid_class(self):
        correct = "** class does not exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("destroy MyModel"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("MyModel.destroy()"))
            self.assertEqual(correct, output.getvalue().strip())

    def testDestroyIDMissingSpaceNotation(self):
        correct = "** Class Class instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("destroy BaseModel"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("destroy User"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("destroy State"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("destroy City"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("destroy Amenity"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("destroy Place"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("destroy Review"))
            self.assertEqual(correct, output.getvalue().strip())

    def testDestroyIDMissingDotNotation(self):
        correct = "** Class Class instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("BaseModel.destroy()"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("User.destroy()"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("State.destroy()"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("City.destroy()"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("Amenity.destroy()"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("Place.destroy()"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("Review.destroy()"))
            self.assertEqual(correct, output.getvalue().strip())

    def testDestroyInvalidIDSpaceNotation(self):
        correct = "** No matching instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("destroy BaseModel 1"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("destroy User 1"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("destroy State 1"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("destroy City 1"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("destroy Amenity 1"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("destroy Place 1"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("destroy Review 1"))
            self.assertEqual(correct, output.getvalue().strip())

    def testDestroyInvalidDotNotation(self):
        correct = "** No matching instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("BaseModel.destroy(1)"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("User.destroy(1)"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("State.destroy(1)"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("City.destroy(1)"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("Amenity.destroy(1)"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("Place.destroy(1)"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("Review.destroy(1)"))
            self.assertEqual(correct, output.getvalue().strip())

    def testDestroyObjectsSpaceNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create BaseModel"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["BaseModel.{}".format(test_ID)]
            command = "destroy BaseModel {}".format(test_ID)
            self.assertFalse(AirBnBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create User"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["User.{}".format(test_ID)]
            command = "show User {}".format(test_ID)
            self.assertFalse(AirBnBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create State"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["State.{}".format(test_ID)]
            command = "show State {}".format(test_ID)
            self.assertFalse(AirBnBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create Place"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Place.{}".format(test_ID)]
            command = "show Place {}".format(test_ID)
            self.assertFalse(AirBnBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create City"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["City.{}".format(test_ID)]
            command = "show City {}".format(test_ID)
            self.assertFalse(AirBnBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create Amenity"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Amenity.{}".format(test_ID)]
            command = "show Amenity {}".format(test_ID)
            self.assertFalse(AirBnBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create Review"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Review.{}".format(test_ID)]
            command = "show Review {}".format(test_ID)
            self.assertFalse(AirBnBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())

    def testDestroyObjectsDotNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create BaseModel"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["BaseModel.{}".format(test_ID)]
            command = "BaseModel.destroy({})".format(test_ID)
            self.assertFalse(AirBnBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create User"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["User.{}".format(test_ID)]
            command = "User.destroy({})".format(test_ID)
            self.assertFalse(AirBnBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create State"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["State.{}".format(test_ID)]
            command = "State.destroy({})".format(test_ID)
            self.assertFalse(AirBnBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create Place"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Place.{}".format(test_ID)]
            command = "Place.destroy({})".format(test_ID)
            self.assertFalse(AirBnBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create City"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["City.{}".format(test_ID)]
            command = "City.destroy({})".format(test_ID)
            self.assertFalse(AirBnBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create Amenity"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Amenity.{}".format(test_ID)]
            command = "Amenity.destroy({})".format(test_ID)
            self.assertFalse(AirBnBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create Review"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Review.{}".format(test_ID)]
            command = "Review.destory({})".format(test_ID)
            self.assertFalse(AirBnBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())


class TestAirBnBCommand_all(unittest.TestCase):
    """Unit testing for  all of cmd interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def testAllInvalidClass(self):
        correct = "** Class does not exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("all MyModel"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("MyModel.all()"))
            self.assertEqual(correct, output.getvalue().strip())

    def testAllObjectsSpaceNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create BaseModel"))
            self.assertFalse(AirBnBCommand().onecmd("create User"))
            self.assertFalse(AirBnBCommand().onecmd("create State"))
            self.assertFalse(AirBnBCommand().onecmd("create Place"))
            self.assertFalse(AirBnBCommand().onecmd("create City"))
            self.assertFalse(AirBnBCommand().onecmd("create Amenity"))
            self.assertFalse(AirBnBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("all"))
            self.assertIn("BaseModel", output.getvalue().strip())
            self.assertIn("User", output.getvalue().strip())
            self.assertIn("State", output.getvalue().strip())
            self.assertIn("Place", output.getvalue().strip())
            self.assertIn("City", output.getvalue().strip())
            self.assertIn("Amenity", output.getvalue().strip())
            self.assertIn("Review", output.getvalue().strip())

    def testAllObjectsDotNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create BaseModel"))
            self.assertFalse(AirBnBCommand().onecmd("create User"))
            self.assertFalse(AirBnBCommand().onecmd("create State"))
            self.assertFalse(AirBnBCommand().onecmd("create Place"))
            self.assertFalse(AirBnBCommand().onecmd("create City"))
            self.assertFalse(AirBnBCommand().onecmd("create Amenity"))
            self.assertFalse(AirBnBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd(".all()"))
            self.assertIn("BaseModel", output.getvalue().strip())
            self.assertIn("User", output.getvalue().strip())
            self.assertIn("State", output.getvalue().strip())
            self.assertIn("Place", output.getvalue().strip())
            self.assertIn("City", output.getvalue().strip())
            self.assertIn("Amenity", output.getvalue().strip())
            self.assertIn("Review", output.getvalue().strip())

    def testAllSingleObjectSpaceNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create BaseModel"))
            self.assertFalse(AirBnBCommand().onecmd("create User"))
            self.assertFalse(AirBnBCommand().onecmd("create State"))
            self.assertFalse(AirBnBCommand().onecmd("create Place"))
            self.assertFalse(AirBnBCommand().onecmd("create City"))
            self.assertFalse(AirBnBCommand().onecmd("create Amenity"))
            self.assertFalse(AirBnBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("all BaseModel"))
            self.assertIn("BaseModel", output.getvalue().strip())
            self.assertNotIn("User", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("all User"))
            self.assertIn("User", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("all State"))
            self.assertIn("State", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("all City"))
            self.assertIn("City", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("all Amenity"))
            self.assertIn("Amenity", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("all Place"))
            self.assertIn("Place", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("all Review"))
            self.assertIn("Review", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())

    def testAllSingleObjectDotNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create BaseModel"))
            self.assertFalse(AirBnBCommand().onecmd("create User"))
            self.assertFalse(AirBnBCommand().onecmd("create State"))
            self.assertFalse(AirBnBCommand().onecmd("create Place"))
            self.assertFalse(AirBnBCommand().onecmd("create City"))
            self.assertFalse(AirBnBCommand().onecmd("create Amenity"))
            self.assertFalse(AirBnBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("BaseModel.all()"))
            self.assertIn("BaseModel", output.getvalue().strip())
            self.assertNotIn("User", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("User.all()"))
            self.assertIn("User", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("State.all()"))
            self.assertIn("State", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("City.all()"))
            self.assertIn("City", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("Amenity.all()"))
            self.assertIn("Amenity", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("Place.all()"))
            self.assertIn("Place", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("Review.all()"))
            self.assertIn("Review", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())


class TestAirBnBCommand_update(unittest.TestCase):
    """
    Unit testing for UPDATE command of the cmd interpreter.
    """

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def testUpdateMissingClass(self):
        correct = "** Missing class name **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("update"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd(".update()"))
            self.assertEqual(correct, output.getvalue().strip())

    def testUpdateInvalidClass(self):
        correct = "** Class does not exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("update MyModel"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("MyModel.update()"))
            self.assertEqual(correct, output.getvalue().strip())

    def testUpdateMissingInstanceIDSpaceNotation(self):
        correct = "** Class instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("update BaseModel"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("update User"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("update State"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("update City"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("update Amenity"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("update Place"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("update Review"))
            self.assertEqual(correct, output.getvalue().strip())

    def testUpdateMissingIDDotNotation(self):
        correct = "** Class instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("BaseModel.update()"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("User.update()"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("State.update()"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("City.update()"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("Amenity.update()"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("Place.update()"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("Review.update()"))
            self.assertEqual(correct, output.getvalue().strip())

    def testUpdateInvalidIDSpaceNotation(self):
        correct = "** No matching instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("update BaseModel 1"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("update User 1"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("update State 1"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("update City 1"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("update Amenity 1"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("update Place 1"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("update Review 1"))
            self.assertEqual(correct, output.getvalue().strip())

    def testUpdateInvalidIDDotNotation(self):
        correct = "** No matching instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("BaseModel.update(1)"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("User.update(1)"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("State.update(1)"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("City.update(1)"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("Amenity.update(1)"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("Place.update(1)"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("Review.update(1)"))
            self.assertEqual(correct, output.getvalue().strip())

    def testUpdateMissingAttrNameSpaceNotation(self):
        correct = "** Attribute name not found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create BaseModel"))
            test_Id = output.getvalue().strip()
            test_Cmd = "update BaseModel {}".format(test_Id)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create User"))
            test_Id = output.getvalue().strip()
            test_Cmd = "update User {}".format(test_Id)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create State"))
            test_Id = output.getvalue().strip()
            test_Cmd = "update State {}".format(test_Id)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create City"))
            test_Id = output.getvalue().strip()
            test_Cmd = "update City {}".format(test_Id)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create Amenity"))
            test_Id = output.getvalue().strip()
            test_Cmd = "update Amenity {}".format(test_Id)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create Place"))
            test_Id = output.getvalue().strip()
            test_Cmd = "update Place {}".format(test_Id)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())

    def testUpdateMissingAttributeNameDotNotation(self):
        correct = "** Attribute name not found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create BaseModel"))
            test_Id = output.getvalue().strip()
            test_Cmd = "BaseModel.update({})".format(test_Id)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create User"))
            test_Id = output.getvalue().strip()
            test_Cmd = "User.update({})".format(test_Id)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create State"))
            test_Id = output.getvalue().strip()
            test_Cmd = "State.update({})".format(test_Id)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create City"))
            test_Id = output.getvalue().strip()
            test_Cmd = "City.update({})".format(test_Id)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create Amenity"))
            test_Id = output.getvalue().strip()
            test_Cmd = "Amenity.update({})".format(test_Id)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create Place"))
            test_Id = output.getvalue().strip()
            test_Cmd = "Place.update({})".format(test_Id)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())

    def testUpdateMissingAttributeValueSpaceNotation(self):
        correct = "** Missing value **"
        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create BaseModel")
            test_Id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            test_Cmd = "update BaseModel {} attr_name".format(test_Id)
            self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create User")
            test_Id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            test_Cmd = "update User {} attr_name".format(test_Id)
            self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create State")
            test_Id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            test_Cmd = "update State {} attr_name".format(test_Id)
            self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create City")
            test_Id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            test_Cmd = "update City {} attr_name".format(test_Id)
            self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create Amenity")
            test_Id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            test_Cmd = "update Amenity {} attr_name".format(test_Id)
            self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create Place")
            test_Id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            test_Cmd = "update Place {} attr_name".format(test_Id)
            self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create Review")
            test_Id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            test_Cmd = "update Review {} attr_name".format(test_Id)
            self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())

    def testUpdateMissingAttributeValueDotNotation(self):
        correct = "** Missing value **"
        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create BaseModel")
            test_Id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            test_Cmd = "BaseModel.update({}, attr_name)".format(test_Id)
            self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create User")
            test_Id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            test_Cmd = "User.update({}, attr_name)".format(test_Id)
            self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create State")
            test_Id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            test_Cmd = "State.update({}, attr_name)".format(test_Id)
            self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create City")
            test_Id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            test_Cmd = "City.update({}, attr_name)".format(test_Id)
            self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create Amenity")
            test_Id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            test_Cmd = "Amenity.update({}, attr_name)".format(test_Id)
            self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create Place")
            test_Id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            test_Cmd = "Place.update({}, attr_name)".format(test_Id)
            self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create Review")
            test_Id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            test_Cmd = "Review.update({}, attr_name)".format(test_Id)
            self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())

    def testUpdateValidStringAttributeSpaceNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create BaseModel")
            test_Id = output.getvalue().strip()
        test_Cmd = "update BaseModel {} attr_name 'attr_value'".format(test_Id)
        self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
        test_dict = storage.all()["BaseModel.{}".format(test_Id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create User")
            test_Id = output.getvalue().strip()
        test_Cmd = "update User {} attr_name 'attr_value'".format(test_Id)
        self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
        test_dict = storage.all()["User.{}".format(test_Id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create State")
            test_Id = output.getvalue().strip()
        test_Cmd = "update State {} attr_name 'attr_value'".format(test_Id)
        self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
        test_dict = storage.all()["State.{}".format(test_Id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create City")
            test_Id = output.getvalue().strip()
        test_Cmd = "update City {} attr_name 'attr_value'".format(test_Id)
        self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
        test_dict = storage.all()["City.{}".format(test_Id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create Place")
            test_Id = output.getvalue().strip()
        test_Cmd = "update Place {} attr_name 'attr_value'".format(test_Id)
        self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
        test_dict = storage.all()["Place.{}".format(test_Id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create Amenity")
            test_Id = output.getvalue().strip()
        test_Cmd = "update Amenity {} attr_name 'attr_value'".format(test_Id)
        self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
        test_dict = storage.all()["Amenity.{}".format(test_Id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create Review")
            test_Id = output.getvalue().strip()
        test_Cmd = "update Review {} attr_name 'attr_value'".format(test_Id)
        self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
        test_dict = storage.all()["Review.{}".format(test_Id)].__dict__
        self.assertTrue("attr_value", test_dict["attr_name"])

    def testUpdateValidStringAttributeDotNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create BaseModel")
            tId = output.getvalue().strip()
        test_Cmd = "BaseModel.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
        test_dict = storage.all()["BaseModel.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create User")
            tId = output.getvalue().strip()
        test_Cmd = "User.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
        test_dict = storage.all()["User.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create State")
            tId = output.getvalue().strip()
        test_Cmd = "State.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
        test_dict = storage.all()["State.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create City")
            tId = output.getvalue().strip()
        test_Cmd = "City.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
        test_dict = storage.all()["City.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create Place")
            tId = output.getvalue().strip()
        test_Cmd = "Place.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
        test_dict = storage.all()["Place.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create Amenity")
            tId = output.getvalue().strip()
        test_Cmd = "Amenity.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
        test_dict = storage.all()["Amenity.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create Review")
            tId = output.getvalue().strip()
        test_Cmd = "Review.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
        test_dict = storage.all()["Review.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

    def testUpdateValidIntegerStringSpaceNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create Place")
            test_Id = output.getvalue().strip()
        test_Cmd = "update Place {} max_guest 98".format(test_Id)
        self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
        test_dict = storage.all()["Place.{}".format(test_Id)].__dict__
        self.assertEqual(98, test_dict["max_guest"])

    def testUpdateValidIntegerAttributeDotNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create Place")
            tId = output.getvalue().strip()
        test_Cmd = "Place.update({}, max_guest, 98)".format(tId)
        self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
        test_dict = storage.all()["Place.{}".format(tId)].__dict__
        self.assertEqual(98, test_dict["max_guest"])

    def testUpdateValidFloatAttributeSpaceNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create Place")
            test_Id = output.getvalue().strip()
        test_Cmd = "update Place {} latitude 7.2".format(test_Id)
        self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
        test_dict = storage.all()["Place.{}".format(test_Id)].__dict__
        self.assertEqual(7.2, test_dict["latitude"])

    def testUpdateValidFloatAttributeDotNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create Place")
            tId = output.getvalue().strip()
        test_Cmd = "Place.update({}, latitude, 7.2)".format(tId)
        self.assertFalse(AirBnBCommand().onecmd(test_Cmd))
        test_dict = storage.all()["Place.{}".format(tId)].__dict__
        self.assertEqual(7.2, test_dict["latitude"])

    def testupdateValidDictionarySpaceNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create BaseModel")
            test_Id = output.getvalue().strip()
        test_Cmd = "update BaseModel {} ".format(test_Id)
        test_Cmd += "{'attr_name': 'attr_value'}"
        AirBnBCommand().onecmd(test_Cmd)
        test_dict = storage.all()["BaseModel.{}".format(test_Id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create User")
            test_Id = output.getvalue().strip()
        test_Cmd = "update User {} ".format(test_Id)
        test_Cmd += "{'attr_name': 'attr_value'}"
        AirBnBCommand().onecmd(test_Cmd)
        test_dict = storage.all()["User.{}".format(test_Id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create State")
            test_Id = output.getvalue().strip()
        test_Cmd = "update State {} ".format(test_Id)
        test_Cmd += "{'attr_name': 'attr_value'}"
        AirBnBCommand().onecmd(test_Cmd)
        test_dict = storage.all()["State.{}".format(test_Id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create City")
            test_Id = output.getvalue().strip()
        test_Cmd = "update City {} ".format(test_Id)
        test_Cmd += "{'attr_name': 'attr_value'}"
        AirBnBCommand().onecmd(test_Cmd)
        test_dict = storage.all()["City.{}".format(test_Id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create Place")
            test_Id = output.getvalue().strip()
        test_Cmd = "update Place {} ".format(test_Id)
        test_Cmd += "{'attr_name': 'attr_value'}"
        AirBnBCommand().onecmd(test_Cmd)
        test_dict = storage.all()["Place.{}".format(test_Id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create Amenity")
            test_Id = output.getvalue().strip()
        test_Cmd = "update Amenity {} ".format(test_Id)
        test_Cmd += "{'attr_name': 'attr_value'}"
        AirBnBCommand().onecmd(test_Cmd)
        test_dict = storage.all()["Amenity.{}".format(test_Id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create Review")
            test_Id = output.getvalue().strip()
        test_Cmd = "update Review {} ".format(test_Id)
        test_Cmd += "{'attr_name': 'attr_value'}"
        AirBnBCommand().onecmd(test_Cmd)
        test_dict = storage.all()["Review.{}".format(test_Id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

    def testUpdateValidDictionaryDotNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create BaseModel")
            test_Id = output.getvalue().strip()
        test_Cmd = "BaseModel.update({}".format(test_Id)
        test_Cmd += "{'attr_name': 'attr_value'})"
        AirBnBCommand().onecmd(test_Cmd)
        test_dict = storage.all()["BaseModel.{}".format(test_Id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create User")
            test_Id = output.getvalue().strip()
        test_Cmd = "User.update({}, ".format(test_Id)
        test_Cmd += "{'attr_name': 'attr_value'})"
        AirBnBCommand().onecmd(test_Cmd)
        test_dict = storage.all()["User.{}".format(test_Id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create State")
            test_Id = output.getvalue().strip()
        test_Cmd = "State.update({}, ".format(test_Id)
        test_Cmd += "{'attr_name': 'attr_value'})"
        AirBnBCommand().onecmd(test_Cmd)
        test_dict = storage.all()["State.{}".format(test_Id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create City")
            test_Id = output.getvalue().strip()
        test_Cmd = "City.update({}, ".format(test_Id)
        test_Cmd += "{'attr_name': 'attr_value'})"
        AirBnBCommand().onecmd(test_Cmd)
        test_dict = storage.all()["City.{}".format(test_Id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create Place")
            test_Id = output.getvalue().strip()
        test_Cmd = "Place.update({}, ".format(test_Id)
        test_Cmd += "{'attr_name': 'attr_value'})"
        AirBnBCommand().onecmd(test_Cmd)
        test_dict = storage.all()["Place.{}".format(test_Id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create Amenity")
            test_Id = output.getvalue().strip()
        test_Cmd = "Amenity.update({}, ".format(test_Id)
        test_Cmd += "{'attr_name': 'attr_value'})"
        AirBnBCommand().onecmd(test_Cmd)
        test_dict = storage.all()["Amenity.{}".format(test_Id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create Review")
            test_Id = output.getvalue().strip()
        test_Cmd = "Review.update({}, ".format(test_Id)
        test_Cmd += "{'attr_name': 'attr_value'})"
        AirBnBCommand().onecmd(test_Cmd)
        test_dict = storage.all()["Review.{}".format(test_Id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

    def testUpdateValidDictionaryWithIntegerSpaceNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create Place")
            test_Id = output.getvalue().strip()
        test_Cmd = "update Place {} ".format(test_Id)
        test_Cmd += "{'max_guest': 98})"
        AirBnBCommand().onecmd(test_Cmd)
        test_dict = storage.all()["Place.{}".format(test_Id)].__dict__
        self.assertEqual(98, test_dict["max_guest"])

    def testUpdateValidDictionaryWithIntegerDotNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create Place")
            test_Id = output.getvalue().strip()
        test_Cmd = "Place.update({}, ".format(test_Id)
        test_Cmd += "{'max_guest': 98})"
        AirBnBCommand().onecmd(test_Cmd)
        test_dict = storage.all()["Place.{}".format(test_Id)].__dict__
        self.assertEqual(98, test_dict["max_guest"])

    def testUpdateValidDictionaryWithFloatSpaceNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create Place")
            test_Id = output.getvalue().strip()
        test_Cmd = "update Place {} ".format(test_Id)
        test_Cmd += "{'latitude': 9.8})"
        AirBnBCommand().onecmd(test_Cmd)
        test_dict = storage.all()["Place.{}".format(test_Id)].__dict__
        self.assertEqual(9.8, test_dict["latitude"])

    def testUpdateValidDictionaryWithFloatDotNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            AirBnBCommand().onecmd("create Place")
            test_Id = output.getvalue().strip()
        test_Cmd = "Place.update({}, ".format(test_Id)
        test_Cmd += "{'latitude': 9.8})"
        AirBnBCommand().onecmd(test_Cmd)
        test_dict = storage.all()["Place.{}".format(test_Id)].__dict__
        self.assertEqual(9.8, test_dict["latitude"])


class TestAirBnBCommand_count(unittest.TestCase):
    """
    Unit testing COUNT method of cmd interpreter.
    """

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def testCountInvalidClass(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("MyModel.count()"))
            self.assertEqual("0", output.getvalue().strip())

    def testCountObjects(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create BaseModel"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("BaseModel.count()"))
            self.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create User"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("User.count()"))
            self.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create State"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("State.count()"))
            self.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create Place"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("Place.count()"))
            self.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create City"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("City.count()"))
            self.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create Amenity"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("Amenity.count()"))
            self.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(AirBnBCommand().onecmd("Review.count()"))
            self.assertEqual("1", output.getvalue().strip())


if __name__ == "__main__":
    unittest.main()

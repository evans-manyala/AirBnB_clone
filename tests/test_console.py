#!/usr/bin/python3
"""
Class defintion for unit tests


Unittest classes:

    TestHBNBCommandCreate
    TestHBNBCommandUpdate
    TestHBNBCommandAll
    TestHBNBCommandPrompt
    TestHBNBCommandDestroy
    TestHBNBCommandExit
    TestHBNBCommandShow
"""
import os
import sys
import unittest
from console import HBNBCommand
from models import storage
from models.engine import FileStorage
from io import StringIO
from unittest.mock import patch


class TestHBNBCommandPrompt(unittest.TestCase):
    """
    Unit tests for checking the prompt of the cmd interpreter.
    """

    def testPromptString(self):
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)

    def testEmptyLine(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(""))
            self.assertEqual("", output.getvalue().strip())


class TestHBNBCommandExit(unittest.TestCase):
    """
    Unit tests for checking if exiting from
    the cmd interpreter works.
    """

    def testQuitExit(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertTrue(HBNBCommand().onecmd("quit"))

    def testEOFExit(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertTrue(HBNBCommand().onecmd("EOF"))


class TestHBNBCommandHelp(unittest.TestCase):
    """
    Unit tests for checking for if help
    messages on the cmd interpreter works.
    """

    def testHelpExit(self):
        _p = "Quit command to exit the program."
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help quit"))
            self.assertEqual(_p, output.getvalue().strip())

    def testHelpCreate(self):
        _p = ("Usage: create <class>\n""Create a new class with a unique id.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help create"))
            self.assertEqual(_p, output.getvalue().strip())

    def testHelpEOF(self):
        _p = "Signal to quit the program."
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help EOF"))
            self.assertEqual(_p, output.getvalue().strip())

    def testHelpShow(self):
        _p = ("Usage: show <class> <id> or <class>.show(<id>)\n"
              "Show string depiction of a class instance with"" a unique id.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help show"))
            self.assertEqual(_p, output.getvalue().strip())

    def testHelpDestroy(self):
        _p = ("Usage: destroy <class> <id> or <class>.destroy(<id>)\n"
              "Delete a class instance with a unique id.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help destroy"))
            self.assertEqual(_p, output.getvalue().strip())

    def testHelpAll(self):
        _p = ("Usage: all or all <class> or <class>.all()\n"
              "Show string depiction of all instances of a class"
              ".\nIf no class is specified, displays all instances of"
              "objects.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help all"))
            self.assertEqual(_p, output.getvalue().strip())

    def testHelpCount(self):
        _p = ("Usage: count <class> or <class>.count()\n        "
              "Retrieve the number of instances of a given class.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help count"))
            self.assertEqual(_p, output.getvalue().strip())

    def testHelpUpdate(self):
        _p = ("Usage: update <class> <id> <attribute_name> <attribute_value>or"
              "\n   <class>.update(<id>, <attribute_name>, <attribute_value"
              ">) or\n       <class>.update(<id>, <dictionary>)\n        "
              "Update a class instance of a unique id by adding or updating\n"
              "a given attribute key/value pair or dictionary.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help update"))
            self.assertEqual(_p, output.getvalue().strip())

    def testHelp(self):
        _p = ("Documented commands (type help <topic>):\n"
              "****************************************\n"
              "EOF  all  count  create  destroy  help  quit  show  update")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help"))
            self.assertEqual(_p, output.getvalue().strip())


class TestHBNBCommandCreate(unittest.TestCase):
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
            self.assertFalse(HBNBCommand().onecmd("create"))
            self.assertEqual(correct, output.getvalue().strip())

    def testCreateInvalidClass(self):
        correct = "** class does not exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create MyModel"))
            self.assertEqual(correct, output.getvalue().strip())

    def testCreateInvalidSyntax(self):
        correct = "*** Incorrect syntax: MyModel.create()"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.create()"))
            self.assertEqual(correct, output.getvalue().strip())
        correct = "*** Incorrect syntax: BaseModel.create()"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.create()"))
            self.assertEqual(correct, output.getvalue().strip())

    def testCreateObject(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertLess(0, len(output.getvalue().strip()))
            testKey = "BaseModel.{}".format(output.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertLess(0, len(output.getvalue().strip()))
            testKey = "User.{}".format(output.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertLess(0, len(output.getvalue().strip()))
            testKey = "State.{}".format(output.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertLess(0, len(output.getvalue().strip()))
            testKey = "City.{}".format(output.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertLess(0, len(output.getvalue().strip()))
            testKey = "Amenity.{}".format(output.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertLess(0, len(output.getvalue().strip()))
            testKey = "Place.{}".format(output.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            self.assertLess(0, len(output.getvalue().strip()))
            testKey = "Review.{}".format(output.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())


class TestHBNBCommandShow(unittest.TestCase):
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
            self.assertFalse(HBNBCommand().onecmd("show"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(".show()"))
            self.assertEqual(correct, output.getvalue().strip())

    def testShowInvalidClass(self):
        correct = "** class does not exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show MyModel"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.show()"))
            self.assertEqual(correct, output.getvalue().strip())

    def testShowMissingID_space(self):
        correct = "** Class Class Class instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show User"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show State"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show City"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Amenity"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Place"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Review"))
            self.assertEqual(correct, output.getvalue().strip())

    def testShowMissingID_dot(self):
        correct = "** Class Class Class instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.show()"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.show()"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.show()"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.show()"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.show()"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.show()"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.show()"))
            self.assertEqual(correct, output.getvalue().strip())

    def testShowNoInstanceFoundSpaceNotation(self):
        correct = "** No matching instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel 1"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show User 1"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show State 1"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show City 1"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Amenity 1"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Place 1"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Review 1"))
            self.assertEqual(correct, output.getvalue().strip())

    def testShowNoInstanceFoundDotSpaceNotation(self):
        correct = "** No matching instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.show(1)"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.show(1)"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.show(1)"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.show(1)"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.show(1)"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.show(1)"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.show(1)"))
            self.assertEqual(correct, output.getvalue().strip())

    def testShowObjSpaceNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["BaseModel.{}".format(test_ID)]
            command = "show BaseModel {}".format(test_ID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["User.{}".format(test_ID)]
            command = "show User {}".format(test_ID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["State.{}".format(test_ID)]
            command = "show State {}".format(test_ID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Place.{}".format(test_ID)]
            command = "show Place {}".format(test_ID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["City.{}".format(test_ID)]
            command = "show City {}".format(test_ID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Amenity.{}".format(test_ID)]
            command = "show Amenity {}".format(test_ID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Review.{}".format(test_ID)]
            command = "show Review {}".format(test_ID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())

    def testShowObjSpaceNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["BaseModel.{}".format(test_ID)]
            command = "BaseModel.show({})".format(test_ID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["User.{}".format(test_ID)]
            command = "User.show({})".format(test_ID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["State.{}".format(test_ID)]
            command = "State.show({})".format(test_ID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Place.{}".format(test_ID)]
            command = "Place.show({})".format(test_ID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["City.{}".format(test_ID)]
            command = "City.show({})".format(test_ID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Amenity.{}".format(test_ID)]
            command = "Amenity.show({})".format(test_ID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Review.{}".format(test_ID)]
            command = "Review.show({})".format(test_ID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())


class TestHBNBCommandDestroy(unittest.TestCase):
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
            self.assertFalse(HBNBCommand().onecmd("destroy"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(".destroy()"))
            self.assertEqual(correct, output.getvalue().strip())

    def testDestroyInvalidClass(self):
        correct = "** class does not exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy MyModel"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.destroy()"))
            self.assertEqual(correct, output.getvalue().strip())

    def testDestroyIDMissingSpaceNotation(self):
        correct = "** Class Class instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy BaseModel"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy User"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy State"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy City"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Amenity"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Place"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Review"))
            self.assertEqual(correct, output.getvalue().strip())

    def testDestroyIDMissingDotNotation(self):
        correct = "** Class Class instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.destroy()"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.destroy()"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.destroy()"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.destroy()"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.destroy()"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.destroy()"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.destroy()"))
            self.assertEqual(correct, output.getvalue().strip())

    def testDestroyInvalidIDSpaceNotation(self):
        correct = "** No matching instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy BaseModel 1"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy User 1"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy State 1"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy City 1"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Amenity 1"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Place 1"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Review 1"))
            self.assertEqual(correct, output.getvalue().strip())

    def testDestroyInvalidDotNotation(self):
        correct = "** No matching instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.destroy(1)"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.destroy(1)"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.destroy(1)"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.destroy(1)"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.destroy(1)"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.destroy(1)"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.destroy(1)"))
            self.assertEqual(correct, output.getvalue().strip())

    def testDestroyObjectsSpaceNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["BaseModel.{}".format(test_ID)]
            command = "destroy BaseModel {}".format(test_ID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["User.{}".format(test_ID)]
            command = "show User {}".format(test_ID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["State.{}".format(test_ID)]
            command = "show State {}".format(test_ID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Place.{}".format(test_ID)]
            command = "show Place {}".format(test_ID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["City.{}".format(test_ID)]
            command = "show City {}".format(test_ID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Amenity.{}".format(test_ID)]
            command = "show Amenity {}".format(test_ID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Review.{}".format(test_ID)]
            command = "show Review {}".format(test_ID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())

    def testDestroyObjectsDotNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["BaseModel.{}".format(test_ID)]
            command = "BaseModel.destroy({})".format(test_ID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["User.{}".format(test_ID)]
            command = "User.destroy({})".format(test_ID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["State.{}".format(test_ID)]
            command = "State.destroy({})".format(test_ID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Place.{}".format(test_ID)]
            command = "Place.destroy({})".format(test_ID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["City.{}".format(test_ID)]
            command = "City.destroy({})".format(test_ID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Amenity.{}".format(test_ID)]
            command = "Amenity.destroy({})".format(test_ID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Review.{}".format(test_ID)]
            command = "Review.destory({})".format(test_ID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())


class TestHBNBCommandAll(unittest.TestCase):
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
            self.assertFalse(HBNBCommand().onecmd("all MyModel"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.all()"))
            self.assertEqual(correct, output.getvalue().strip())

    def testAllObjectsSpaceNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all"))
            self.assertIn("BaseModel", output.getvalue().strip())
            self.assertIn("User", output.getvalue().strip())
            self.assertIn("State", output.getvalue().strip())
            self.assertIn("Place", output.getvalue().strip())
            self.assertIn("City", output.getvalue().strip())
            self.assertIn("Amenity", output.getvalue().strip())
            self.assertIn("Review", output.getvalue().strip())

    def testAllObjectsDotNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(".all()"))
            self.assertIn("BaseModel", output.getvalue().strip())
            self.assertIn("User", output.getvalue().strip())
            self.assertIn("State", output.getvalue().strip())
            self.assertIn("Place", output.getvalue().strip())
            self.assertIn("City", output.getvalue().strip())
            self.assertIn("Amenity", output.getvalue().strip())
            self.assertIn("Review", output.getvalue().strip())

    def testAllSingleObjectSpaceNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all BaseModel"))
            self.assertIn("BaseModel", output.getvalue().strip())
            self.assertNotIn("User", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all User"))
            self.assertIn("User", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all State"))
            self.assertIn("State", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all City"))
            self.assertIn("City", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all Amenity"))
            self.assertIn("Amenity", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all Place"))
            self.assertIn("Place", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all Review"))
            self.assertIn("Review", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())

    def testAllSingleObjectDotNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.all()"))
            self.assertIn("BaseModel", output.getvalue().strip())
            self.assertNotIn("User", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.all()"))
            self.assertIn("User", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.all()"))
            self.assertIn("State", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.all()"))
            self.assertIn("City", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.all()"))
            self.assertIn("Amenity", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.all()"))
            self.assertIn("Place", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.all()"))
            self.assertIn("Review", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())


class TestHBNBCommandUpdate(unittest.TestCase):
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
            self.assertFalse(HBNBCommand().onecmd("update"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(".update()"))
            self.assertEqual(correct, output.getvalue().strip())

    def testUpdateInvalidClass(self):
        correct = "** Class does not exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update MyModel"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.update()"))
            self.assertEqual(correct, output.getvalue().strip())

    def testUpdateMissingInstanceIDSpaceNotation(self):
        correct = "** Class instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update BaseModel"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update User"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update State"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update City"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Amenity"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Place"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Review"))
            self.assertEqual(correct, output.getvalue().strip())

    def testUpdateMissingIDDotNotation(self):
        correct = "** Class instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.update()"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.update()"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.update()"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.update()"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.update()"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.update()"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.update()"))
            self.assertEqual(correct, output.getvalue().strip())

    def testUpdateInvalidIDSpaceNotation(self):
        correct = "** No matching instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update BaseModel 1"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update User 1"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update State 1"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update City 1"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Amenity 1"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Place 1"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Review 1"))
            self.assertEqual(correct, output.getvalue().strip())

    def testUpdateInvalidIDDotNotation(self):
        correct = "** No matching instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.update(1)"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.update(1)"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.update(1)"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.update(1)"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.update(1)"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.update(1)"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.update(1)"))
            self.assertEqual(correct, output.getvalue().strip())

    def testUpdateMissingAttrNameSpaceNotation(self):
        correct = "** Attribute name not found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            test_Id = output.getvalue().strip()
            test_Cmd = "update BaseModel {}".format(test_Id)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            test_Id = output.getvalue().strip()
            test_Cmd = "update User {}".format(test_Id)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            test_Id = output.getvalue().strip()
            test_Cmd = "update State {}".format(test_Id)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            test_Id = output.getvalue().strip()
            test_Cmd = "update City {}".format(test_Id)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            test_Id = output.getvalue().strip()
            test_Cmd = "update Amenity {}".format(test_Id)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            test_Id = output.getvalue().strip()
            test_Cmd = "update Place {}".format(test_Id)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())

    def testUpdateMissingAttributeNameDotNotation(self):
        correct = "** Attribute name not found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            test_Id = output.getvalue().strip()
            test_Cmd = "BaseModel.update({})".format(test_Id)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            test_Id = output.getvalue().strip()
            test_Cmd = "User.update({})".format(test_Id)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            test_Id = output.getvalue().strip()
            test_Cmd = "State.update({})".format(test_Id)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            test_Id = output.getvalue().strip()
            test_Cmd = "City.update({})".format(test_Id)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            test_Id = output.getvalue().strip()
            test_Cmd = "Amenity.update({})".format(test_Id)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            test_Id = output.getvalue().strip()
            test_Cmd = "Place.update({})".format(test_Id)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())

    def testUpdateMissingAttributeValueSpaceNotation(self):
        correct = "** Missing value **"
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            test_Id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            test_Cmd = "update BaseModel {} attr_name".format(test_Id)
            self.assertFalse(HBNBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            test_Id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            test_Cmd = "update User {} attr_name".format(test_Id)
            self.assertFalse(HBNBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            test_Id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            test_Cmd = "update State {} attr_name".format(test_Id)
            self.assertFalse(HBNBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            test_Id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            test_Cmd = "update City {} attr_name".format(test_Id)
            self.assertFalse(HBNBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            test_Id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            test_Cmd = "update Amenity {} attr_name".format(test_Id)
            self.assertFalse(HBNBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            test_Id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            test_Cmd = "update Place {} attr_name".format(test_Id)
            self.assertFalse(HBNBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            test_Id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            test_Cmd = "update Review {} attr_name".format(test_Id)
            self.assertFalse(HBNBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())

    def testUpdateMissingAttributeValueDotNotation(self):
        correct = "** Missing value **"
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            test_Id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            test_Cmd = "BaseModel.update({}, attr_name)".format(test_Id)
            self.assertFalse(HBNBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            test_Id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            test_Cmd = "User.update({}, attr_name)".format(test_Id)
            self.assertFalse(HBNBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            test_Id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            test_Cmd = "State.update({}, attr_name)".format(test_Id)
            self.assertFalse(HBNBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            test_Id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            test_Cmd = "City.update({}, attr_name)".format(test_Id)
            self.assertFalse(HBNBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            test_Id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            test_Cmd = "Amenity.update({}, attr_name)".format(test_Id)
            self.assertFalse(HBNBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            test_Id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            test_Cmd = "Place.update({}, attr_name)".format(test_Id)
            self.assertFalse(HBNBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            test_Id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            test_Cmd = "Review.update({}, attr_name)".format(test_Id)
            self.assertFalse(HBNBCommand().onecmd(test_Cmd))
            self.assertEqual(correct, output.getvalue().strip())

    def testUpdateValidStringAttributeSpaceNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            test_Id = output.getvalue().strip()
        test_Cmd = "update BaseModel {} attr_name 'attr_value'".format(test_Id)
        self.assertFalse(HBNBCommand().onecmd(test_Cmd))
        test_dict = storage.all()["BaseModel.{}".format(test_Id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            test_Id = output.getvalue().strip()
        test_Cmd = "update User {} attr_name 'attr_value'".format(test_Id)
        self.assertFalse(HBNBCommand().onecmd(test_Cmd))
        test_dict = storage.all()["User.{}".format(test_Id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            test_Id = output.getvalue().strip()
        test_Cmd = "update State {} attr_name 'attr_value'".format(test_Id)
        self.assertFalse(HBNBCommand().onecmd(test_Cmd))
        test_dict = storage.all()["State.{}".format(test_Id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            test_Id = output.getvalue().strip()
        test_Cmd = "update City {} attr_name 'attr_value'".format(test_Id)
        self.assertFalse(HBNBCommand().onecmd(test_Cmd))
        test_dict = storage.all()["City.{}".format(test_Id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            test_Id = output.getvalue().strip()
        test_Cmd = "update Place {} attr_name 'attr_value'".format(test_Id)
        self.assertFalse(HBNBCommand().onecmd(test_Cmd))
        test_dict = storage.all()["Place.{}".format(test_Id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            test_Id = output.getvalue().strip()
        test_Cmd = "update Amenity {} attr_name 'attr_value'".format(test_Id)
        self.assertFalse(HBNBCommand().onecmd(test_Cmd))
        test_dict = storage.all()["Amenity.{}".format(test_Id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            test_Id = output.getvalue().strip()
        test_Cmd = "update Review {} attr_name 'attr_value'".format(test_Id)
        self.assertFalse(HBNBCommand().onecmd(test_Cmd))
        test_dict = storage.all()["Review.{}".format(test_Id)].__dict__
        self.assertTrue("attr_value", test_dict["attr_name"])

    def testUpdateValidStringAttributeDotNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            tId = output.getvalue().strip()
        test_Cmd = "BaseModel.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(test_Cmd))
        test_dict = storage.all()["BaseModel.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            tId = output.getvalue().strip()
        test_Cmd = "User.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(test_Cmd))
        test_dict = storage.all()["User.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            tId = output.getvalue().strip()
        test_Cmd = "State.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(test_Cmd))
        test_dict = storage.all()["State.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            tId = output.getvalue().strip()
        test_Cmd = "City.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(test_Cmd))
        test_dict = storage.all()["City.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tId = output.getvalue().strip()
        test_Cmd = "Place.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(test_Cmd))
        test_dict = storage.all()["Place.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            tId = output.getvalue().strip()
        test_Cmd = "Amenity.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(test_Cmd))
        test_dict = storage.all()["Amenity.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            tId = output.getvalue().strip()
        test_Cmd = "Review.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(test_Cmd))
        test_dict = storage.all()["Review.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

    def testUpdateValidIntegerStringSpaceNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            test_Id = output.getvalue().strip()
        test_Cmd = "update Place {} max_guest 98".format(test_Id)
        self.assertFalse(HBNBCommand().onecmd(test_Cmd))
        test_dict = storage.all()["Place.{}".format(test_Id)].__dict__
        self.assertEqual(98, test_dict["max_guest"])

    def testUpdateValidIntegerAttributeDotNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tId = output.getvalue().strip()
        test_Cmd = "Place.update({}, max_guest, 98)".format(tId)
        self.assertFalse(HBNBCommand().onecmd(test_Cmd))
        test_dict = storage.all()["Place.{}".format(tId)].__dict__
        self.assertEqual(98, test_dict["max_guest"])

    def testUpdateValidFloatAttributeSpaceNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            test_Id = output.getvalue().strip()
        test_Cmd = "update Place {} latitude 7.2".format(test_Id)
        self.assertFalse(HBNBCommand().onecmd(test_Cmd))
        test_dict = storage.all()["Place.{}".format(test_Id)].__dict__
        self.assertEqual(7.2, test_dict["latitude"])

    def testUpdateValidFloatAttributeDotNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tId = output.getvalue().strip()
        test_Cmd = "Place.update({}, latitude, 7.2)".format(tId)
        self.assertFalse(HBNBCommand().onecmd(test_Cmd))
        test_dict = storage.all()["Place.{}".format(tId)].__dict__
        self.assertEqual(7.2, test_dict["latitude"])

    def testupdateValidDictionarySpaceNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            test_Id = output.getvalue().strip()
        test_Cmd = "update BaseModel {} ".format(test_Id)
        test_Cmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(test_Cmd)
        test_dict = storage.all()["BaseModel.{}".format(test_Id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            test_Id = output.getvalue().strip()
        test_Cmd = "update User {} ".format(test_Id)
        test_Cmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(test_Cmd)
        test_dict = storage.all()["User.{}".format(test_Id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            test_Id = output.getvalue().strip()
        test_Cmd = "update State {} ".format(test_Id)
        test_Cmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(test_Cmd)
        test_dict = storage.all()["State.{}".format(test_Id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            test_Id = output.getvalue().strip()
        test_Cmd = "update City {} ".format(test_Id)
        test_Cmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(test_Cmd)
        test_dict = storage.all()["City.{}".format(test_Id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            test_Id = output.getvalue().strip()
        test_Cmd = "update Place {} ".format(test_Id)
        test_Cmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(test_Cmd)
        test_dict = storage.all()["Place.{}".format(test_Id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            test_Id = output.getvalue().strip()
        test_Cmd = "update Amenity {} ".format(test_Id)
        test_Cmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(test_Cmd)
        test_dict = storage.all()["Amenity.{}".format(test_Id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            test_Id = output.getvalue().strip()
        test_Cmd = "update Review {} ".format(test_Id)
        test_Cmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(test_Cmd)
        test_dict = storage.all()["Review.{}".format(test_Id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

    def testUpdateValidDictionaryDotNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            test_Id = output.getvalue().strip()
        test_Cmd = "BaseModel.update({}".format(test_Id)
        test_Cmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(test_Cmd)
        test_dict = storage.all()["BaseModel.{}".format(test_Id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            test_Id = output.getvalue().strip()
        test_Cmd = "User.update({}, ".format(test_Id)
        test_Cmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(test_Cmd)
        test_dict = storage.all()["User.{}".format(test_Id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            test_Id = output.getvalue().strip()
        test_Cmd = "State.update({}, ".format(test_Id)
        test_Cmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(test_Cmd)
        test_dict = storage.all()["State.{}".format(test_Id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            test_Id = output.getvalue().strip()
        test_Cmd = "City.update({}, ".format(test_Id)
        test_Cmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(test_Cmd)
        test_dict = storage.all()["City.{}".format(test_Id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            test_Id = output.getvalue().strip()
        test_Cmd = "Place.update({}, ".format(test_Id)
        test_Cmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(test_Cmd)
        test_dict = storage.all()["Place.{}".format(test_Id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            test_Id = output.getvalue().strip()
        test_Cmd = "Amenity.update({}, ".format(test_Id)
        test_Cmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(test_Cmd)
        test_dict = storage.all()["Amenity.{}".format(test_Id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            test_Id = output.getvalue().strip()
        test_Cmd = "Review.update({}, ".format(test_Id)
        test_Cmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(test_Cmd)
        test_dict = storage.all()["Review.{}".format(test_Id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

    def testUpdateValidDictionaryWithIntegerSpaceNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            test_Id = output.getvalue().strip()
        test_Cmd = "update Place {} ".format(test_Id)
        test_Cmd += "{'max_guest': 98})"
        HBNBCommand().onecmd(test_Cmd)
        test_dict = storage.all()["Place.{}".format(test_Id)].__dict__
        self.assertEqual(98, test_dict["max_guest"])

    def testUpdateValidDictionaryWithIntegerDotNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            test_Id = output.getvalue().strip()
        test_Cmd = "Place.update({}, ".format(test_Id)
        test_Cmd += "{'max_guest': 98})"
        HBNBCommand().onecmd(test_Cmd)
        test_dict = storage.all()["Place.{}".format(test_Id)].__dict__
        self.assertEqual(98, test_dict["max_guest"])

    def testUpdateValidDictionaryWithFloatSpaceNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            test_Id = output.getvalue().strip()
        test_Cmd = "update Place {} ".format(test_Id)
        test_Cmd += "{'latitude': 9.8})"
        HBNBCommand().onecmd(test_Cmd)
        test_dict = storage.all()["Place.{}".format(test_Id)].__dict__
        self.assertEqual(9.8, test_dict["latitude"])

    def testUpdateValidDictionaryWithFloatDotNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            test_Id = output.getvalue().strip()
        test_Cmd = "Place.update({}, ".format(test_Id)
        test_Cmd += "{'latitude': 9.8})"
        HBNBCommand().onecmd(test_Cmd)
        test_dict = storage.all()["Place.{}".format(test_Id)].__dict__
        self.assertEqual(9.8, test_dict["latitude"])


class TestHBNBCommandCount(unittest.TestCase):
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
            self.assertFalse(HBNBCommand().onecmd("MyModel.count()"))
            self.assertEqual("0", output.getvalue().strip())

    def testCountObjects(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.count()"))
            self.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.count()"))
            self.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.count()"))
            self.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.count()"))
            self.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.count()"))
            self.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.count()"))
            self.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.count()"))
            self.assertEqual("1", output.getvalue().strip())


if __name__ == "__main__":
    unittest.main()

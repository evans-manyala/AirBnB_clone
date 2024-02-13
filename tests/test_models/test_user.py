#!/usr/bin/python3
"""
Defines unit tests for models/user.py.

Unittest classes:
    TestUserInitialization
    TestUserSave
    TestUserToDictionary
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.user import User


class TestUserInitialization(unittest.TestCase):
    """
    Unit testing Initialization of the User class.
    """

    def testNoArgsInitialization(self):
        self.assertEqual(User, type(User()))

    def testNewInstanceStoredInObjects(self):
        self.assertIn(User(), models.storage.all().values())

    def testIDIsPublicString(self):
        self.assertEqual(str, type(User().id))

    def testCreatedAtIsPublicDateTime(self):
        self.assertEqual(datetime, type(User().created_at))

    def testUpdatedAtIsPublicDateTime(self):
        self.assertEqual(datetime, type(User().updated_at))

    def testEmailIsPublicSring(self):
        self.assertEqual(str, type(User.email))

    def testPasswordIsPublicString(self):
        self.assertEqual(str, type(User.password))

    def testFirstNameIsPublicString(self):
        self.assertEqual(str, type(User.first_name))

    def testLastNameIsPublicString(self):
        self.assertEqual(str, type(User.last_name))

    def testTwoUserUniqueIDs(self):
        user1 = User()
        user2 = User()
        self.assertNotEqual(user1.id, user2.id)

    def testTwoUsersDiffCreatedAt(self):
        user1 = User()
        sleep(0.05)
        user2 = User()
        self.assertLess(user1.created_at, user2.created_at)

    def testTwoUsersDiffUpdatedAt(self):
        user1 = User()
        sleep(0.05)
        user2 = User()
        self.assertLess(user1.updated_at, user2.updated_at)

    def testStringRepresentation(self):
        dateTime = datetime.today()
        dateTime_repr = repr(dateTime)
        user = User()
        user.id = "123456"
        user.created_at = user.updated_at = dateTime
        user_str = user.__str__()
        self.assertIn("[User] (123456)", user_str)
        self.assertIn("'id': '123456'", user_str)
        self.assertIn("'created_at': " + dateTime_repr, user_str)
        self.assertIn("'updated_at': " + dateTime_repr, user_str)

    def testArgsUnused(self):
        user = User(None)
        self.assertNotIn(None, user.__dict__.values())

    def testInitializationWithKwargs(self):
        dateTime = datetime.today()
        dateTime_iso = dateTime.isoformat()
        user = User(id="345", created_at=dateTime_iso, updated_at=dateTime_iso)
        self.assertEqual(user.id, "345")
        self.assertEqual(user.created_at, dateTime)
        self.assertEqual(user.updated_at, dateTime)

    def testInitializationWithNoneKwargs(self):
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)


class TestUserSave(unittest.TestCase):
    """
    Unit testing SAVE method of the  class.
    """

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def testOneSave(self):
        user = User()
        sleep(0.05)
        first_updated_at = user.updated_at
        user.save()
        self.assertLess(first_updated_at, user.updated_at)

    def testTwoSave(self):
        user = User()
        sleep(0.05)
        first_updated_at = user.updated_at
        user.save()
        second_updated_at = user.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        user.save()
        self.assertLess(second_updated_at, user.updated_at)

    def testSaveWithArg(self):
        user = User()
        with self.assertRaises(TypeError):
            user.save(None)

    def testSaveUpdatesFile(self):
        user = User()
        user.save()
        user_id = "User." + user.id
        with open("file.json", "r") as f:
            self.assertIn(user_id, f.read())


class TestUserToDictionary(unittest.TestCase):
    """
    Unit testing ToDictionary method of the User class.
    """

    def testToDictionaryType(self):
        self.assertTrue(dict, type(User().to_dict()))

    def testToDictionaryContainsCorrectKeys(self):
        user = User()
        self.assertIn("id", user.to_dict())
        self.assertIn("created_at", user.to_dict())
        self.assertIn("updated_at", user.to_dict())
        self.assertIn("__class__", user.to_dict())

    def testToDictionaryContainsAddedAttr(self):
        user = User()
        user.middle_name = "Holberton"
        user.my_number = 98
        self.assertEqual("Holberton", user.middle_name)
        self.assertIn("my_number", user.to_dict())

    def testToDictionaryDateTimeAttrAreStrings(self):
        user = User()
        user_dict = user.to_dict()
        self.assertEqual(str, type(user_dict["id"]))
        self.assertEqual(str, type(user_dict["created_at"]))
        self.assertEqual(str, type(user_dict["updated_at"]))

    def testToDictionaryOutput(self):
        dateTime = datetime.today()
        user = User()
        user.id = "123456"
        user.created_at = user.updated_at = dateTime
        tdict = {
            'id': '123456',
            '__class__': 'User',
            'created_at': dateTime.isoformat(),
            'updated_at': dateTime.isoformat(),
        }
        self.assertDictEqual(user.to_dict(), tdict)

    def testContrastToDictionaryDunderDictionary(self):
        user = User()
        self.assertNotEqual(user.to_dict(), user.__dict__)

    def testToDictionaryWithArg(self):
        user = User()
        with self.assertRaises(TypeError):
            user.to_dict(None)


if __name__ == "__main__":
    unittest.main()

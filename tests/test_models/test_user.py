#!/usr/bin/python3
"""
Defines unit tests for models/user.py.

Unittest classes:
    TestUSerInitialization
    TestUserSave
    TestUserToDictionary
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.user import User


class TestUSerInitialization(unittest.TestCase):
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
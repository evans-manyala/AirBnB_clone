#!/usr/bin/python3
"""
Defines unit tests for models/state.py.

Unittest classes:
    TestStateInitialization
    TestStateSave
    TestStateToDictionary
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.state import State


class TestStateInitialization(unittest.TestCase):
    """
    Unit testing Initialization of the State class.
    """

    def testNoArgsInitialization(self):
        self.assertEqual(State, type(State()))

    def testNewInstanceStoredInObjects(self):
        self.assertIn(State(), models.storage.all().values())

    def testIDIsPublicString(self):
        self.assertEqual(str, type(State().id))

    def testCreatedAtIsPublicDateTime(self):
        self.assertEqual(datetime, type(State().created_at))

    def testUpdatedAtIsPublicDateTime(self):
        self.assertEqual(datetime, type(State().updated_at))

    def testNameisPublicClassAttr(self):
        state = State()
        self.assertEqual(str, type(State.name))
        self.assertIn("name", dir(state))
        self.assertNotIn("name", state.__dict__)

    def testTwoStatesUninqueIDs(self):
        state1 = State()
        state2 = State()
        self.assertNotEqual(state1.id, state2.id)

    def testTwoStateDiffCreatedAt(self):
        state1 = State()
        sleep(0.05)
        state2 = State()
        self.assertLess(state1.created_at, state2.created_at)

    def testTwoStateDiffUpdatedAt(self):
        state1 = State()
        sleep(0.05)
        state2 = State()
        self.assertLess(state1.updated_at, state2.updated_at)

    def testStringRepresentation(self):
        dateTime = datetime.today()
        dateTime_repr = repr(dateTime)
        state = State()
        state.id = "123456"
        state.created_at = state.updated_at = dateTime
        state_str = state.__str__()
        self.assertIn("[State] (123456)", state_str)
        self.assertIn("'id': '123456'", state_str)
        self.assertIn("'created_at': " + dateTime_repr, state_str)
        self.assertIn("'updated_at': " + dateTime_repr, state_str)

    def testArgsUnused(self):
        state = State(None)
        self.assertNotIn(None, state.__dict__.values())

    def testInitializationWithKwargs(self):
        dateTime = datetime.today()
        dateTime_iso = dateTime.isoformat()
        state = State(id="345", created_at=dateTime_iso,
                      updated_at=dateTime_iso)
        self.assertEqual(state.id, "345")
        self.assertEqual(state.created_at, dateTime)
        self.assertEqual(state.updated_at, dateTime)

    def testInitializationWithNoneKwargs(self):
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)


class TestStateSave(unittest.TestCase):
    """
    Unit testing SAVE method of the State class.
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
        state = State()
        sleep(0.05)
        first_updated_at = state.updated_at
        state.save()
        self.assertLess(first_updated_at, state.updated_at)

    def testTwoSaves(self):
        state = State()
        sleep(0.05)
        first_updated_at = state.updated_at
        state.save()
        second_updated_at = state.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        state.save()
        self.assertLess(second_updated_at, state.updated_at)

    def testSaveWithArg(self):
        state = State()
        with self.assertRaises(TypeError):
            state.save(None)

    def testSaveUpdatesFile(self):
        state = State()
        state.save()
        stid = "State." + state.id
        with open("file.json", "r") as f:
            self.assertIn(stid, f.read())


class TestStateToDictionary(unittest.TestCase):
    """
    Unit testing ToDictionary method of the State class.
    """

    def testToDictionaryType(self):
        self.assertTrue(dict, type(State().to_dict()))

    def testToDictionaryContainsCorrectKeys(self):
        state = State()
        self.assertIn("id", state.to_dict())
        self.assertIn("created_at", state.to_dict())
        self.assertIn("updated_at", state.to_dict())
        self.assertIn("__class__", state.to_dict())

    def testToDictionaryContainsAddedAttr(self):
        state = State()
        state.middle_name = "Holberton"
        state.my_number = 98
        self.assertEqual("Holberton", state.middle_name)
        self.assertIn("my_number", state.to_dict())

    def testToDictionaryDateTimeAttrAreStrings(self):
        state = State()
        st_dict = state.to_dict()
        self.assertEqual(str, type(st_dict["id"]))
        self.assertEqual(str, type(st_dict["created_at"]))
        self.assertEqual(str, type(st_dict["updated_at"]))

    def testToDictionaryOutput(self):
        dateTime = datetime.today()
        state = State()
        state.id = "123456"
        state.created_at = state.updated_at = dateTime
        tdict = {
            'id': '123456',
            '__class__': 'State',
            'created_at': dateTime.isoformat(),
            'updated_at': dateTime.isoformat(),
        }
        self.assertDictEqual(state.to_dict(), tdict)

    def testContrastToDictionaryDunderDict(self):
        state = State()
        self.assertNotEqual(state.to_dict(), state.__dict__)

    def testToDictionaryWith_arg(self):
        state = State()
        with self.assertRaises(TypeError):
            state.to_dict(None)


if __name__ == "__main__":
    unittest.main()

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



class TestState_instantiation(unittest.TestCase):
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



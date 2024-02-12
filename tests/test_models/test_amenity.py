#!/usr/bin/python3
"""
Defines unit tests for models/amenity.py.

Unittest classes:
    TestAmenityInstantiation
    TestAmenitySave
    TestAmenity_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.amenity import Amenity


class TestAmenityInstantiation(unittest.TestCase):
    """
    Unit testing class instantiation.
    """

    def testNoArgInstantiation(self):
        self.assertEqual(Amenity, type(Amenity()))

    def testNewInstanceStoredInObjects(self):
        self.assertIn(Amenity(), models.storage.all().values())

    def testIDIsPublicString(self):
        self.assertEqual(str, type(Amenity().id))

    def testCreatedAtIsPublicDateTime(self):
        self.assertEqual(datetime, type(Amenity().created_at))

    def testUpdateAtIsPublicDateTime(self):
        self.assertEqual(datetime, type(Amenity().updated_at))

    def testNameIsPublicClassAttribute(self):
        am = Amenity()
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(Amenity()))
        self.assertNotIn("name", am.__dict__)

    def testTwoAmenitiesUniqueIDs(self):
        am1 = Amenity()
        am2 = Amenity()
        self.assertNotEqual(am1.id, am2.id)

    def testTwoAmenitiesDifferentCreatedAt(self):
        am1 = Amenity()
        sleep(0.05)
        am2 = Amenity()
        self.assertLess(am1.created_at, am2.created_at)

    def testTwoAmenitiesDifferentUpdatedAt(self):
        am1 = Amenity()
        sleep(0.05)
        am2 = Amenity()
        self.assertLess(am1.updated_at, am2.updated_at)

    def testStringRepresentation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        am = Amenity()
        am.id = "123456"
        am.created_at = am.updated_at = dt
        amstr = am.__str__()
        self.assertIn("[Amenity] (123456)", amstr)
        self.assertIn("'id': '123456'", amstr)
        self.assertIn("'created_at': " + dt_repr, amstr)
        self.assertIn("'updated_at': " + dt_repr, amstr)

    def testArgsUnused(self):
        am = Amenity(None)
        self.assertNotIn(None, am.__dict__.values())

    def testInstantiationWithKwargs(self):
        """
        Instantiation with kwargs test method
        """
        dt = datetime.today()
        dt_iso = dt.isoformat()
        am = Amenity(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(am.id, "345")
        self.assertEqual(am.created_at, dt)
        self.assertEqual(am.updated_at, dt)

    def testInstantiationWithNoKwargs(self):
        """
        Instantiation with no kwargs test method
        """
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)


class TestAmenitySave(unittest.TestCase):
    """
    Unit testing for testing SAVE method of the Amenity class.
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
        am = Amenity()
        sleep(0.05)
        first_updated_at = am.updated_at
        am.save()
        self.assertLess(first_updated_at, am.updated_at)

    def TestTwoSaves(self):
        am = Amenity()
        sleep(0.05)
        first_updated_at = am.updated_at
        am.save()
        second_updated_at = am.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        am.save()
        self.assertLess(second_updated_at, am.updated_at)

    def testSaveWithArguments(self):
        am = Amenity()
        with self.assertRaises(TypeError):
            am.save(None)

    def testSaveUpdateFile(self):
        am = Amenity()
        am.save()
        amid = "Amenity." + am.id
        with open("file.json", "r") as f:
            self.assertIn(amid, f.read())

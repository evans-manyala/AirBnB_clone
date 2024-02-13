#!/usr/bin/python3
"""
Defines unit tests for models/city.py.

Unit test classes:
    TestCityInitialization
    TestCitySave
    TestCityToDictionary
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.city import City


class TestCityInitialization(unittest.TestCase):
    """
    Unit testing Initialization of the City class.
    """

    def testNoArgumentsInitialization(self):
        self.assertEqual(City, type(City()))

    def testNewInstanceStoredInObjects(self):
        self.assertIn(City(), models.storage.all().values())

    def testIDIsPublicString(self):
        self.assertEqual(str, type(City().id))

    def testCreatedAtIsPublicDateTime(self):
        self.assertEqual(datetime, type(City().created_at))

    def testUpdatedAtIsPublicDateTime(self):
        self.assertEqual(datetime, type(City().updated_at))

    def testStateIsPublicClassAttr(self):
        city = City()
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(city))
        self.assertNotIn("state_id", city.__dict__)

    def testNameIsPublicClassAttr(self):
        city = City()
        self.assertEqual(str, type(City.name))
        self.assertIn("name", dir(city))
        self.assertNotIn("name", city.__dict__)

    def testTwoCitiesUniqueIDs(self):
        city1 = City()
        city2 = City()
        self.assertNotEqual(city1.id, city2.id)

    def testTwoCitiesDifferentCreatedAt(self):
        city1 = City()
        sleep(0.05)
        city2 = City()
        self.assertLess(city1.created_at, city2.created_at)

    def testTwoCitiesDiffUpdatedAt(self):
        city1 = City()
        sleep(0.05)
        city2 = City()
        self.assertLess(city1.updated_at, city2.updated_at)

    def testStringRep(self):
        dateTime = datetime.today()
        dt_repr = repr(dateTime)
        city = City()
        city.id = "123456"
        city.created_at = city.updated_at = dateTime
        citystr = city.__str__()
        self.assertIn("[City] (123456)", citystr)
        self.assertIn("'id': '123456'", citystr)
        self.assertIn("'created_at': " + dt_repr, citystr)
        self.assertIn("'updated_at': " + dt_repr, citystr)

    def testArgumenentsUnused(self):
        city = City(None)
        self.assertNotIn(None, city.__dict__.values())

    def testInitializationWithKwargs(self):
        dateTime = datetime.today()
        dt_iso = dateTime.isoformat()
        city = City(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(city.id, "345")
        self.assertEqual(city.created_at, dateTime)
        self.assertEqual(city.updated_at, dateTime)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)


class TestCitySave(unittest.TestCase):
    """
    Unit testing SAVE method of the City class.
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
        city = City()
        sleep(0.05)
        first_updated_at = city.updated_at
        city.save()
        self.assertLess(first_updated_at, city.updated_at)

    def tesTwoSaves(self):
        city = City()
        sleep(0.05)
        first_updated_at = city.updated_at
        city.save()
        second_updated_at = city.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        city.save()
        self.assertLess(second_updated_at, city.updated_at)

    def testSaveWithArgs(self):
        city = City()
        with self.assertRaises(TypeError):
            city.save(None)

    def testSaveUpdatesFile(self):
        city = City()
        city.save()
        cityid = "City." + city.id
        with open("file.json", "r") as f:
            self.assertIn(cityid, f.read())

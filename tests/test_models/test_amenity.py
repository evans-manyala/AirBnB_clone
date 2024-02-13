#!/usr/bin/python3
"""
Defines unit tests for models/amenity.py.

Unittest classes:
    TestAmenityInitialization
    TestAmenitySave
    TestAmenityToDictionary
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.amenity import Amenity


class TestAmenityInitialization(unittest.TestCase):
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
        amenity = Amenity()
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(Amenity()))
        self.assertNotIn("name", amenity.__dict__)

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
        dateTime = datetime.today()
        dateTime_repr = repr(dateTime)
        amenity = Amenity()
        amenity.id = "123456"
        amenity.created_at = amenity.updated_at = dateTime
        amstr = amenity.__str__()
        self.assertIn("[Amenity] (123456)", amstr)
        self.assertIn("'id': '123456'", amstr)
        self.assertIn("'created_at': " + dateTime_repr, amstr)
        self.assertIn("'updated_at': " + dateTime_repr, amstr)

    def testArgsUnused(self):
        amenity = Amenity(None)
        self.assertNotIn(None, amenity.__dict__.values())

    def testInstantiationWithKwargs(self):
        """
        Instantiation with kwargs test method
        """
        dateTime = datetime.today()
        dateTime_iso = dateTime.isoformat()
        amenity = Amenity(id="345", created_at=dateTime_iso,
                          updated_at=dateTime_iso)
        self.assertEqual(amenity.id, "345")
        self.assertEqual(amenity.created_at, dateTime)
        self.assertEqual(amenity.updated_at, dateTime)

    def testInstantiationWithNoKwargs(self):
        """
        Instantiation with no kwargs test method
        """
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)


class TestAmenitySave(unittest.TestCase):
    """
    Unit testing for SAVE method of the Amenity class.
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
        amenity = Amenity()
        sleep(0.05)
        first_updated_at = amenity.updated_at
        amenity.save()
        self.assertLess(first_updated_at, amenity.updated_at)

    def testTwoSaves(self):
        amenity = Amenity()
        sleep(0.05)
        first_updated_at = amenity.updated_at
        amenity.save()
        second_updated_at = amenity.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        amenity.save()
        self.assertLess(second_updated_at, amenity.updated_at)

    def testSaveWithArguments(self):
        amenity = Amenity()
        with self.assertRaises(TypeError):
            amenity.save(None)

    def testSaveUpdateFile(self):
        amenity = Amenity()
        amenity.save()
        amid = "Amenity." + amenity.id
        with open("file.json", "r") as f:
            self.assertIn(amid, f.read())


class TestAmenityToDictionary(unittest.TestCase):
    """
    Unit testing for To_Dict method of the Amenity class.
    """

    def testToDictionaryType(self):
        self.assertTrue(dict, type(Amenity().to_dict()))

    def testToDictionaryContainingCorrectKeys(self):
        amenity = Amenity()
        self.assertIn("id", amenity.to_dict())
        self.assertIn("created_at", amenity.to_dict())
        self.assertIn("updated_at", amenity.to_dict())
        self.assertIn("__class__", amenity.to_dict())

    def testToDictionaryContainsAddedAtrr(self):
        amenity = Amenity()
        amenity.middle_name = "ALX"
        amenity.my_number = 98
        self.assertEqual("ALX", amenity.middle_name)
        self.assertIn("my_number", amenity.to_dict())

    def testToDictionaryDateTimeAttrAreStrings(self):
        amenity = Amenity()
        am_dict = amenity.to_dict()
        self.assertEqual(str, type(am_dict["id"]))
        self.assertEqual(str, type(am_dict["created_at"]))
        self.assertEqual(str, type(am_dict["updated_at"]))

    def testToDictionaryOutput(self):
        dateTime = datetime.today()
        amenity = Amenity()
        amenity.id = "123456"
        amenity.created_at = amenity.updated_at = dateTime
        tdict = {
            'id': '123456',
            '__class__': 'Amenity',
            'created_at': dateTime.isoformat(),
            'updated_at': dateTime.isoformat(),
        }
        self.assertDictEqual(amenity.to_dict(), tdict)

    def testContrastToDictionaryDunderDictionary(self):
        amenity = Amenity()
        self.assertNotEqual(amenity.to_dict(), amenity.__dict__)

    def testToDictionaryWithArguments(self):
        amenity = Amenity()
        with self.assertRaises(TypeError):
            amenity.to_dict(None)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/python3
"""
Defines unit tests for models/place.py.

Unittest classes:
    TestPlaceInitialization
    TestPlaceSave
    TestPlaceToDictionary
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.place import Place


class TestPlaceInitialization(unittest.TestCase):
    """
    Unit testing Initialization of the Place class.
    """

    def testNoArgsInitialization(self):
        self.assertEqual(Place, type(Place()))

    def testNewInstanceStoredInObjects(self):
        self.assertIn(Place(), models.storage.all().values())

    def testIDIsPublicString(self):
        self.assertEqual(str, type(Place().id))

    def testCreatedAtIsPublicDateTime(self):
        self.assertEqual(datetime, type(Place().created_at))

    def testUpdatedAtIsPublicDateTime(self):
        self.assertEqual(datetime, type(Place().updated_at))

    def testCityIDIsPublicClassAttribute(self):
        place = Place()
        self.assertEqual(str, type(Place.city_id))
        self.assertIn("city_id", dir(place))
        self.assertNotIn("city_id", place.__dict__)

    def testUserIDIsPublicCalssAttribute(self):
        place = Place()
        self.assertEqual(str, type(Place.user_id))
        self.assertIn("user_id", dir(place))
        self.assertNotIn("user_id", place.__dict__)

    def testNameIsPublicClassAttribute(self):
        place = Place()
        self.assertEqual(str, type(Place.name))
        self.assertIn("name", dir(place))
        self.assertNotIn("name", place.__dict__)

    def testDescIsPublicClassAttribute(self):
        place = Place()
        self.assertEqual(str, type(Place.description))
        self.assertIn("description", dir(place))
        self.assertNotIn("desctiption", place.__dict__)

    def testNoOfRoomsIsPublicCalssAttr(self):
        place = Place()
        self.assertEqual(int, type(Place.number_rooms))
        self.assertIn("number_rooms", dir(place))
        self.assertNotIn("number_rooms", place.__dict__)

    def testNoOfBathroomsIsPublicClassAttr(self):
        place = Place()
        self.assertEqual(int, type(Place.number_bathrooms))
        self.assertIn("number_bathrooms", dir(place))
        self.assertNotIn("number_bathrooms", place.__dict__)

    def testMaxGuestIsPublicClassAttr(self):
        place = Place()
        self.assertEqual(int, type(Place.max_guest))
        self.assertIn("max_guest", dir(place))
        self.assertNotIn("max_guest", place.__dict__)

    def testPriceByNightIsPublicClassAttr(self):
        place = Place()
        self.assertEqual(int, type(Place.price_by_night))
        self.assertIn("price_by_night", dir(place))
        self.assertNotIn("price_by_night", place.__dict__)

    def testLatitudeIsPublicClassAttr(self):
        place = Place()
        self.assertEqual(float, type(Place.latitude))
        self.assertIn("latitude", dir(place))
        self.assertNotIn("latitude", place.__dict__)

    def testLongitudeIsPublicClassAttr(self):
        place = Place()
        self.assertEqual(float, type(Place.longitude))
        self.assertIn("longitude", dir(place))
        self.assertNotIn("longitude", place.__dict__)

    def testAmenityIDsIsPublicClassAttr(self):
        place = Place()
        self.assertEqual(list, type(Place.amenity_ids))
        self.assertIn("amenity_ids", dir(place))
        self.assertNotIn("amenity_ids", place.__dict__)

    def testTwoPlacesUniqueIDs(self):
        place1 = Place()
        place2 = Place()
        self.assertNotEqual(place1.id, place2.id)

    def testTwoPlacesDiffCreatedAt(self):
        place1 = Place()
        sleep(0.05)
        place2 = Place()
        self.assertLess(place1.created_at, place2.created_at)

    def testTwoPlacesDiffUpdatedAt(self):
        place1 = Place()
        sleep(0.05)
        place2 = Place()
        self.assertLess(place1.updated_at, place2.updated_at)

    def testStringRepresentation(self):
        dateTime = datetime.today()
        dateTime_repr = repr(dateTime)
        place = Place()
        place.id = "123456"
        place.created_at = place.updated_at = dateTime
        plstr = place.__str__()
        self.assertIn("[Place] (123456)", plstr)
        self.assertIn("'id': '123456'", plstr)
        self.assertIn("'created_at': " + dateTime_repr, plstr)
        self.assertIn("'updated_at': " + dateTime_repr, plstr)

    def testArgsUnused(self):
        place = Place(None)
        self.assertNotIn(None, place.__dict__.values())

    def testInitializationWithKwargs(self):
        dateTime = datetime.today()
        dateTime_iso = dateTime.isoformat()
        place = Place(id="345", created_at=dateTime_iso,
                      updated_at=dateTime_iso)
        self.assertEqual(place.id, "345")
        self.assertEqual(place.created_at, dateTime)
        self.assertEqual(place.updated_at, dateTime)

    def testInitializationWithNoneKwargs(self):
        with self.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)


class TestPlaceSave(unittest.TestCase):
    """
    Unit testing SAVE method of the Place class.
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
        place = Place()
        sleep(0.05)
        first_updated_at = place.updated_at
        place.save()
        self.assertLess(first_updated_at, place.updated_at)

    def testTwoSaves(self):
        place = Place()
        sleep(0.05)
        first_updated_at = place.updated_at
        place.save()
        second_updated_at = place.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        place.save()
        self.assertLess(second_updated_at, place.updated_at)

    def testSaveWithArgs(self):
        place = Place()
        with self.assertRaises(TypeError):
            place.save(None)

    def testSaveUpdatesFile(self):
        place = Place()
        place.save()
        placeID = "Place." + place.id
        with open("file.json", "r") as f:
            self.assertIn(placeID, f.read())


class TestPlaceToDictionary(unittest.TestCase):
    """
    Unit testing ToDictionary method of the Place class.
    """

    def testToDictionaryType(self):
        self.assertTrue(dict, type(Place().to_dict()))

    def testToDictionaryContainsCorrectKeys(self):
        place = Place()
        self.assertIn("id", place.to_dict())
        self.assertIn("created_at", place.to_dict())
        self.assertIn("updated_at", place.to_dict())
        self.assertIn("__class__", place.to_dict())

    def testToDictionaryContainsAddedAttr(self):
        place = Place()
        place.middle_name = "Holberton"
        place.my_number = 98
        self.assertEqual("Holberton", place.middle_name)
        self.assertIn("my_number", place.to_dict())

    def testToDictionaryDateTimeAttrAreStrings(self):
        place = Place()
        place_dict = place.to_dict()
        self.assertEqual(str, type(place_dict["id"]))
        self.assertEqual(str, type(place_dict["created_at"]))
        self.assertEqual(str, type(place_dict["updated_at"]))

    def testToDictionaryOutput(self):
        dateTime = datetime.today()
        place = Place()
        place.id = "123456"
        place.created_at = place.updated_at = dateTime
        tdict = {
            'id': '123456',
            '__class__': 'Place',
            'created_at': dateTime.isoformat(),
            'updated_at': dateTime.isoformat(),
        }
        self.assertDictEqual(place.to_dict(), tdict)

    def testContrastToDictionaryDunderDictionary(self):
        place = Place()
        self.assertNotEqual(place.to_dict(), place.__dict__)

    def testToDictionaryWithArgs(self):
        place = Place()
        with self.assertRaises(TypeError):
            place.to_dict(None)


if __name__ == "__main__":
    unittest.main()

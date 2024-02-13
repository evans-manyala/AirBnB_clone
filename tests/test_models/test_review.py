#!/usr/bin/python3
"""
Defines unit tests for models/review.py.

Unittest classes:
    TestReviewInitialization
    TestReviewSave
    TestReviewToDictionary
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.review import Review


class TestReview_instantiation(unittest.TestCase):
    """
    Unit testing Initialization of the Review class."""

    def testNoArgsInitialization(self):
        self.assertEqual(Review, type(Review()))

    def testNewInstanceStoredInObjects(self):
        self.assertIn(Review(), models.storage.all().values())

    def testIDIsPublicString(self):
        self.assertEqual(str, type(Review().id))

    def testCreatedAtIsPublicDateTime(self):
        self.assertEqual(datetime, type(Review().created_at))

    def testUpdateAtIsPublicDateTime(self):
        self.assertEqual(datetime, type(Review().updated_at))

    def testPlaceIDIsPublicClassAttr(self):
        re_view = Review()
        self.assertEqual(str, type(Review.place_id))
        self.assertIn("place_id", dir(re_view))
        self.assertNotIn("place_id", re_view.__dict__)

    def testUserIDIsPublicClassAttr(self):
        re_view = Review()
        self.assertEqual(str, type(Review.user_id))
        self.assertIn("user_id", dir(re_view))
        self.assertNotIn("user_id", re_view.__dict__)

    def testTextIsPublicClassAttr(self):
        re_view = Review()
        self.assertEqual(str, type(Review.text))
        self.assertIn("text", dir(re_view))
        self.assertNotIn("text", re_view.__dict__)

    def testTwoReviewsUniqueIDs(self):
        re_view1 = Review()
        re_view2 = Review()
        self.assertNotEqual(re_view1.id, re_view2.id)

    def testTwoReviewsDiffCreatedAt(self):
        re_view1 = Review()
        sleep(0.05)
        re_view2 = Review()
        self.assertLess(re_view1.created_at, re_view2.created_at)

    def testTwoReviewsDiffUpdatedAt(self):
        re_view1 = Review()
        sleep(0.05)
        re_view2 = Review()
        self.assertLess(re_view1.updated_at, re_view2.updated_at)

    def testStringRepresentation(self):
        dateTime = datetime.today()
        dateTime_repr = repr(dateTime)
        re_view = Review()
        re_view.id = "123456"
        re_view.created_at = re_view.updated_at = dateTime
        re_viewstr = re_view.__str__()
        self.assertIn("[Review] (123456)", re_viewstr)
        self.assertIn("'id': '123456'", re_viewstr)
        self.assertIn("'created_at': " + dateTime_repr, re_viewstr)
        self.assertIn("'updated_at': " + dateTime_repr, re_viewstr)

    def testArgsUnused(self):
        re_view = Review(None)
        self.assertNotIn(None, re_view.__dict__.values())

    def testInitializationWithKwargs(self):
        dateTime = datetime.today()
        dateTime_iso = dateTime.isoformat()
        re_view = Review(id="345", created_at=dateTime_iso,
                         updated_at=dateTime_iso)
        self.assertEqual(re_view.id, "345")
        self.assertEqual(re_view.created_at, dateTime)
        self.assertEqual(re_view.updated_at, dateTime)

    def testInitializationNoneKwargs(self):
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)


class TestPlaceSave(unittest.TestCase):
    """
    Unit testing SAVE method of the Review class.
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
        re_view = Review()
        sleep(0.05)
        first_updated_at = re_view.updated_at
        re_view.save()
        self.assertLess(first_updated_at, re_view.updated_at)

    def testTwoSaves(self):
        re_view = Review()
        sleep(0.05)
        first_updated_at = re_view.updated_at
        re_view.save()
        second_updated_at = re_view.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        re_view.save()
        self.assertLess(second_updated_at, re_view.updated_at)

    def testSaveWithArg(self):
        re_view = Review()
        with self.assertRaises(TypeError):
            re_view.save(None)

    def testSaveUpdatesFile(self):
        re_view = Review()
        re_view.save()
        re_viewid = "Review." + re_view.id
        with open("file.json", "r") as f:
            self.assertIn(re_viewid, f.read())


class TestPlaceToDictionary(unittest.TestCase):
    """
    Unit testing ToDictionary method of the Review class.
    """

    def testToDictionaryType(self):
        self.assertTrue(dict, type(Review().to_dict()))

    def testToDictionaryContainsCorrectKeys(self):
        re_view = Review()
        self.assertIn("id", re_view.to_dict())
        self.assertIn("created_at", re_view.to_dict())
        self.assertIn("updated_at", re_view.to_dict())
        self.assertIn("__class__", re_view.to_dict())

    def testToDictionaryContainsAddedAttr(self):
        re_view = Review()
        re_view.middle_name = "Holberton"
        re_view.my_number = 98
        self.assertEqual("Holberton", re_view.middle_name)
        self.assertIn("my_number", re_view.to_dict())

    def testToDictionaryDateTimeAttrAreStrings(self):
        re_view = Review()
        re_view_dict = re_view.to_dict()
        self.assertEqual(str, type(re_view_dict["id"]))
        self.assertEqual(str, type(re_view_dict["created_at"]))
        self.assertEqual(str, type(re_view_dict["updated_at"]))

    def testToDictionaryOutput(self):
        dateTime = datetime.today()
        re_view = Review()
        re_view.id = "123456"
        re_view.created_at = re_view.updated_at = dateTime
        tdict = {
            'id': '123456',
            '__class__': 'Review',
            'created_at': dateTime.isoformat(),
            'updated_at': dateTime.isoformat(),
        }
        self.assertDictEqual(re_view.to_dict(), tdict)

    def testContrastToDictionaryDunderDictionary(self):
        re_view = Review()
        self.assertNotEqual(re_view.to_dict(), re_view.__dict__)

    def testPlaceToDictionaryWithArg(self):
        re_view = Review()
        with self.assertRaises(TypeError):
            re_view.to_dict(None)


if __name__ == "__main__":
    unittest.main()

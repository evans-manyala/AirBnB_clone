#!/usr/bin/python3
"""
Defines unit tests for models/review.py.

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
        re_view = Review(id="345", created_at=dateTime_iso, updated_at=dateTime_iso)
        self.assertEqual(re_view.id, "345")
        self.assertEqual(re_view.created_at, dateTime)
        self.assertEqual(re_view.updated_at, dateTime)

    def testInitializationNoneKwargs(self):
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)
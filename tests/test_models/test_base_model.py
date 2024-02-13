#!/usr/bin/python3
"""
Defines unit tests for models/base_model.py.

Unittest classes:
    TestBaseModelInitialization
    TestBaseModelSave
    TestBaseModelToDictionary
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class TestBaseModelBaseModelInitialization(unittest.TestCase):
    """
    Unit testing for initialization of the BaseModel class.
    """

    def testNoArgsInstantiates(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def testNewInstanceStoredInObjects(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def testIDIsPublicString(self):
        self.assertEqual(str, type(BaseModel().id))

    def testCreatedAtIsPublicDateTime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def testUpdatedAtIsPublicDateTime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def testTwoModelsUniqueIDs(self):
        baseModel1 = BaseModel()
        baseModel2 = BaseModel()
        self.assertNotEqual(baseModel1.id, baseModel2.id)

    def testTwoModelsDiffCreatedAt(self):
        baseModel1 = BaseModel()
        sleep(0.05)
        baseModel2 = BaseModel()
        self.assertLess(baseModel1.created_at, baseModel2.created_at)

    def testTwoModelsDiffUpdatedAt(self):
        baseModel1 = BaseModel()
        sleep(0.05)
        baseModel2 = BaseModel()
        self.assertLess(baseModel1.updated_at, baseModel2.updated_at)

    def testStringRep(self):
        dateTime = datetime.today()
        dateTime_repr = repr(dateTime)
        baseModel = BaseModel()
        baseModel.id = "123456"
        baseModel.created_at = baseModel.updated_at = dateTime
        baseModelstr = baseModel.__str__()
        self.assertIn("[BaseModel] (123456)", baseModelstr)
        self.assertIn("'id': '123456'", baseModelstr)
        self.assertIn("'created_at': " + dateTime_repr, baseModelstr)
        self.assertIn("'updated_at': " + dateTime_repr, baseModelstr)

    def testArgsUnused(self):
        baseModel = BaseModel(None)
        self.assertNotIn(None, baseModel.__dict__.values())

    def testInitializationWithKwargs(self):
        dateTime = datetime.today()
        dateTime_iso = dateTime.isoformat()
        baseModel = BaseModel(id="345", created_at=dateTime_iso,
                              updated_at=dateTime_iso)
        self.assertEqual(baseModel.id, "345")
        self.assertEqual(baseModel.created_at, dateTime)
        self.assertEqual(baseModel.updated_at, dateTime)

    def testInitializationNoneKwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def testInitializationWithArgsAndKwargs(self):
        dateTime = datetime.today()
        dateTime_iso = dateTime.isoformat()
        baseModel = BaseModel("12", id="345", created_at=dateTime_iso,
                              updated_at=dateTime_iso)
        self.assertEqual(baseModel.id, "345")
        self.assertEqual(baseModel.created_at, dateTime)
        self.assertEqual(baseModel.updated_at, dateTime)

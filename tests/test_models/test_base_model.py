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


class TestBaseModelSave(unittest.TestCase):
    """
    Unit testing SAVE method of the BaseModel class.
    """

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
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
        baseModel = BaseModel()
        sleep(0.05)
        first_updated_at = baseModel.updated_at
        baseModel.save()
        self.assertLess(first_updated_at, baseModel.updated_at)

    def testTwoSaves(self):
        baseModel = BaseModel()
        sleep(0.05)
        first_updated_at = baseModel.updated_at
        baseModel.save()
        second_updated_at = baseModel.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        baseModel.save()
        self.assertLess(second_updated_at, baseModel.updated_at)

    def testSaveWithArguments(self):
        baseModel = BaseModel()
        with self.assertRaises(TypeError):
            baseModel.save(None)

    def testSaveUpdatesFile(self):
        baseModel = BaseModel()
        baseModel.save()
        baseModelid = "BaseModel." + baseModel.id
        with open("file.json", "r") as f:
            self.assertIn(baseModelid, f.read())


class TestBaseModelToDictionary(unittest.TestCase):
    """
    Unit testing ToDictionary method of the BaseModel class.
    """

    def testToDictionaryType(self):
        baseModel = BaseModel()
        self.assertTrue(dict, type(baseModel.to_dict()))

    def testToDictionaryContainsCorrectKeys(self):
        baseModel = BaseModel()
        self.assertIn("id", baseModel.to_dict())
        self.assertIn("created_at", baseModel.to_dict())
        self.assertIn("updated_at", baseModel.to_dict())
        self.assertIn("__class__", baseModel.to_dict())

    def testToDictionaryContainsAddedAtrr(self):
        baseModel = BaseModel()
        baseModel.name = "Holberton"
        baseModel.my_number = 98
        self.assertIn("name", baseModel.to_dict())
        self.assertIn("my_number", baseModel.to_dict())

    def testToDictionaryDateTimeAttrAreStrings(self):
        baseModel = BaseModel()
        baseModel_dict = baseModel.to_dict()
        self.assertEqual(str, type(baseModel_dict["created_at"]))
        self.assertEqual(str, type(baseModel_dict["updated_at"]))

    def testToDictionaryOutput(self):
        dateTime = datetime.today()
        baseModel = BaseModel()
        baseModel.id = "123456"
        baseModel.created_at = baseModel.updated_at = dateTime
        tdict = {
            'id': '123456',
            '__class__': 'BaseModel',
            'created_at': dateTime.isoformat(),
            'updated_at': dateTime.isoformat()
        }
        self.assertDictEqual(baseModel.to_dict(), tdict)

    def testContrastToDictionaryDunderDictionary(self):
        baseModel = BaseModel()
        self.assertNotEqual(baseModel.to_dict(), baseModel.__dict__)

    def testToDictionaryWithArguments(self):
        baseModel = BaseModel()
        with self.assertRaises(TypeError):
            baseModel.to_dict(None)


if __name__ == "__main__":
    unittest.main()

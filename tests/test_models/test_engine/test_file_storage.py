#!/usr/bin/python3
"""
Defines unit tests for models/engine/file_storage.py.

Unittest classes:
    TestFileStorageInitialization
    TestFileStorageMethods
"""

import os
import json
import models
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.engine.FileStorage import FileStorage
import models.amenity
import models.place
import models.review
import models.state
import models.user
import models.city

class TestFileStorageInitialization(unittest.TestCase):
    """
    Unit testing Initialization of the FileStorage class.
    """

    def testFileStorageInitializationWithArgs(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def testFileStorageInitializationNoArgs(self):
        self.assertEqual(type(FileStorage()), FileStorage)

    def testFileStorageFilePathIsPrivateString(self):
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def testFileStorageObjectsIsPrivateDictionary(self):
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def testStorageInitialization(self):
        self.assertEqual(type(models.storage), FileStorage)
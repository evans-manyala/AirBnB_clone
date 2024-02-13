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
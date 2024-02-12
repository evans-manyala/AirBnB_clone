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

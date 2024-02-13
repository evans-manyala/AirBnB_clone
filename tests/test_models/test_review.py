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
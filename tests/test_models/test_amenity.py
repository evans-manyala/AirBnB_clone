#!/usr/bin/python3
"""Defines unit tests for models/amenity.py.

Unittest classes:
    TestAmenityCreateInstance
    TestAmenitysave
    TestAmenityToDictionary
"""

import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.amenity import Amenity
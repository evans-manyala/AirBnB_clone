#!/usr/bin/python3
"""
Defines unit tests for models/state.py.

Unittest classes:
    TestCityInitialization
    TestCitySave
    TestCityToDictionary
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.state import State
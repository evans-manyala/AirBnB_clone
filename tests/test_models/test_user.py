#!/usr/bin/python3
"""
Defines unit tests for models/user.py.

Unittest classes:
    TestUSerInitialization
    TestUserSave
    TestUserToDictionary
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.user import User
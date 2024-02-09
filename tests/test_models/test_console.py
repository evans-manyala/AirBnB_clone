#!/usr/bin/python3
"""
Class defintion for unittests


Unittest classes:

    TestAirBnBCommand_create
    TestAirBnBCommand_update
    TestAirBnBCommand_all
    TestAirBnBCommand_prompt
    TestAirBnBCommand_destroy
    TestAirBnBCommand_exit
    TestAirBnBCommand_show
"""
import os
import sys
import unittest
from models import storage
from models.engine import FileStorage
from io import StringIO
from unittest.mock import patch

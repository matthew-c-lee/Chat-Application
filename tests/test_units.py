import re

import pytest

import os
import tempfile
import unittest


from unittest import TestCase
from website.auth import *

from website import views

def test_form_requirements():
    assert validate_sign_up('bad!username', 'badpw', 'badpw2', 'Good answer')[0] == False
    assert validate_sign_up('good_username', 'UnequalPassword1!', 'UnequalPassword2!', 'Good answer')[0] == False
    assert validate_sign_up('good_username', 'GoodPassword1!', 'GoodPassword1!', 'Good answer')[0] == True

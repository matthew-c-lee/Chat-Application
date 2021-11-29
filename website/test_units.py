# test_with_unittest.py
import re

from unittest import TestCase

class TryTesting(TestCase):
    def test_always_passes(self):
        self.assertTrue(True)

    # def test_always_fails(self):
    #     self.assertTrue(False)

    def test_form_requirements(self):
        username = 'bad!username'
        password1 = 'badpw'
        password2 = 'badpw2'
        answer = 'Good answer'




        if len(username) < 4:  # username is too short
            username_passes = False
        elif len(username) > 14:  # username is too long
            username_passes = False
        elif not(re.match(r'^\w+$', username)):
            username_passes = False
        elif re.search(r"\s", username):
            username_passes = False
        
        if len(password1) < 7:
            password_passes = False
        elif not(re.search('[a-zA-Z]', password1)):
            password_passes = False
        elif not(any(map(str.isdigit, password1))):
            password_passes = False
        elif password1.isalnum():
            password_passes = False
        elif re.search(r"\s", password1):
            password_passes = False
        elif password1 !=  password2:
            password_passes = False
        if len(answer) < 1:
            answer_passes = False
        
        self.assertFalse(username_passes)
        self.assertFalse(password_passes)
        self.assertTrue(answer_passes)
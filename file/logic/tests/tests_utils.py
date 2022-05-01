import re
from django.test import TestCase

from ..utils import randomWord, prependTimeAndSlug

class TestsInfra(TestCase):
    def test_success_random_string(self):
        regext = r'[a-z]+'

        word = randomWord() # word with default length
        self.assertTrue(len(word) > 0)
        self.assertTrue(re.fullmatch(regext, word))

        word8Char = randomWord(8)
        self.assertTrue(len(word8Char) == 8)
        self.assertTrue(re.fullmatch(regext, word8Char))

    # prependTimeAndSlug
    def test_success_prepend_time_and_slug(self):
        testName = 'lorem-ipsum.ext'
        regex = re.compile('[0-9]{10}-[a-z]{6}-' + testName)

        fullName = prependTimeAndSlug(testName)
        self.assertTrue(regex.fullmatch(fullName))

    def test_failure_prepend_time_and_slug(self):
        with self.assertRaises(Exception):
            prependTimeAndSlug()
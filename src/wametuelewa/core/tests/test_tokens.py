from doctest import DocTestSuite
from unittest import TestCase

class ModuleTests(TestCase):
    def __new__(self, test):
        return getattr(self, test)()

    @classmethod
    def test_tokens(cls):
        from wametuelewa.core import tokens
        return DocTestSuite(tokens)

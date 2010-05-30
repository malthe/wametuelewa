from unittest import TestCase
from doctest import DocTestSuite

class ModuleTests(TestCase):
    def __new__(self, test):
        return getattr(self, test)()

    @classmethod
    def test_tokens(cls):
        from wametuelewa.core import parser
        return DocTestSuite(parser)

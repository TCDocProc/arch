from django.test import TestCase

class TestTestCase(TestCase):
    def setUp(self):
        self.truthy = True

    def test_true(self):
        """Ensures that the value of true holds"""
        self.assertEqual(self.truthy, False)
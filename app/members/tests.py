from django.test import TestCase

class TestTestCase(TestCase):
    def setUp(self):
        self.truthy = True

    def test_check_true_is_true(self):
        self.assertEqual(self.truthy, True)
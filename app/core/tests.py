from django.test import TestCase
from website.helpers.integrate import IntegrateTestCase

class CoreTestCase(IntegrateTestCase):
    def setUp(self):
        super(CoreTestCase, self).setUp()

    def test_selenium(self):
        self.run_integrate_test("test")
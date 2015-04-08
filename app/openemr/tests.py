from django.test import TestCase, Client
from website.helpers.integrate import IntegrateTestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
class ProcessesTestCase(TestCase):

    USERNAME = 'napoli'
    EMAIL = 'coffee@me.com'
    PASSWORD = 'flapjack'

    PATHWAY_SAMPLE_XML = 'app/static/xml/pathways.xml'

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username=self.USERNAME, email=self.EMAIL, password=self.PASSWORD)

    def test_logged_in(self):
        logged_in = self.client.login(username=self.USERNAME, password=self.PASSWORD)
        self.assertEqual(logged_in, True)
        response = self.client.get(reverse('index'), follow=True)
        self.assertTrue(len(response.redirect_chain) >= 1)
        self.assertEqual(response.redirect_chain[0], ('http://testserver%s' % reverse('add_pathway'), 301))

    def test_index_logged_out_success(self):
        response = self.client.post(reverse('openemr_signup'), {'username': 'Demo2', 'password': 'DemoPatient'}, follow=True)
        self.assertEqual(response.redirect_chain[0], ('http://testserver/', 302))

    def test_index_logged_out_fail(self):
        response = self.client.post(reverse('openemr_signup'), {'username': 'Demo2', 'password': 'WrongPassword'})
        self.assertEqual(response.status_code, 200)
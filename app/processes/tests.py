from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class ProcessesTestCase(TestCase):

    USERNAME = 'napoli'
    EMAIL = 'coffee@me.com'
    PASSWORD = 'flapjack'

    PATHWAY_SAMPLE_XML = 'app/static/xml/pathways.xml'

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username=self.USERNAME, email=self.EMAIL, password=self.PASSWORD)

    def test_index_not_logged_in(self):
        response = self.client.get(reverse('index'), follow=True)
        self.assertTrue(len(response.redirect_chain) >= 1)
        self.assertEqual(response.redirect_chain[0], ('http://testserver%s' % reverse('add_pathway'), 301))

    def test_index_logged_in_no_pathways(self):
        logged_in = self.client.login(username=self.USERNAME, password=self.PASSWORD)
        self.assertEqual(logged_in, True)

        response = self.client.get(reverse('index'))
        self.assertRedirects(response, reverse('add_pathway'), status_code=301)

    def test_index_logged_in_has_json_extension(self):
        logged_in = self.client.login(username=self.USERNAME, password=self.PASSWORD)
        self.assertEqual(logged_in, True)

        self.__upload_sample_xml()

        response = self.client.get('/processes/user/%s.json' % str(self.user.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_index_logged_in_has_context(self):
        logged_in = self.client.login(username=self.USERNAME, password=self.PASSWORD)
        self.assertEqual(logged_in, True)

        self.__upload_sample_xml()

        response = self.client.get('/processes/user/%s/0' % str(self.user.id))
        self.assertEqual(response.status_code, 200)

    def __upload_sample_xml(self):
        with open(self.PATHWAY_SAMPLE_XML) as fp:
            response = self.client.post(reverse('add_pathway'), {'pathway_xml': fp})
            self.assertRedirects(response, '/processes/user/%s' % str(self.user.id), status_code=302)

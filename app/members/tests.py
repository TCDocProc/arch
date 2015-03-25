from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class PathwaysTestCase(TestCase):

    USERNAME = 'napoli'
    EMAIL = 'coffee@me.com'
    PASSWORD = 'flapjack'

    PATHWAY_SAMPLE_XML = 'app/static/xml/pathways.xml'
    PATHWAY_SAMPLE_NOT_XML = 'app/static/xml/not_xml.doc'
    PATHWAY_SAMPLE_BAD_XML = 'app/static/xml/bad_xml.xml'

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username=self.USERNAME, email=self.EMAIL, password=self.PASSWORD)

    def test_add_pathway_not_logged_in(self):
        response = self.client.get(reverse('add_pathway'))
        self.assertRedirects(response, '/accounts/signup/?next=%s' % (reverse('add_pathway')), status_code=302)

    def test_add_pathway_logged_in_no_pathways(self):
        logged_in = self.client.login(username=self.USERNAME, password=self.PASSWORD)
        self.assertEqual(logged_in, True)

        response = self.client.get(reverse('add_pathway'))
        self.assertEqual(response.status_code, 200)

    def test_add_pathway_logged_in_no_pathways_upload_xml(self):
        logged_in = self.client.login(username=self.USERNAME, password=self.PASSWORD)
        self.assertEqual(logged_in, True)

        self.__upload_sample_xml()

    def test_add_pathway_logged_in_no_pathways_upload_not_xml(self):
        logged_in = self.client.login(username=self.USERNAME, password=self.PASSWORD)
        self.assertEqual(logged_in, True)

        with open(self.PATHWAY_SAMPLE_NOT_XML) as fp:
            response = self.client.post(reverse('add_pathway'), {'pathway_xml': fp})
            self.assertEqual(response.status_code, 200)

    def test_add_pathway_logged_in_no_pathways_upload_bad_xml(self):
        logged_in = self.client.login(username=self.USERNAME, password=self.PASSWORD)
        self.assertEqual(logged_in, True)

        with open(self.PATHWAY_SAMPLE_BAD_XML) as fp:
            response = self.client.post(reverse('add_pathway'), {'pathway_xml': fp})
            self.assertEqual(response.status_code, 200)

    def test_add_pathway_logged_in_has_pathway(self):
        logged_in = self.client.login(username=self.USERNAME, password=self.PASSWORD)
        self.assertEqual(logged_in, True)

        self.__upload_sample_xml()

        response = self.client.get(reverse('add_pathway'))
        self.assertRedirects(response, '/processes', status_code=302)

    def __upload_sample_xml(self):
        with open(self.PATHWAY_SAMPLE_XML) as fp:
            response = self.client.post(reverse('add_pathway'), {'pathway_xml': fp})
            self.assertRedirects(response, '/processes', status_code=302)

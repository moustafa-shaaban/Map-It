from django.test import TestCase
from django.urls import reverse

from applications.core.utils import AuthenticatedTestCase

class MapPageTests(AuthenticatedTestCase):
    url_name = "places:places-map"
    def test_url_exists_at_correct_location(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "places_map.html")


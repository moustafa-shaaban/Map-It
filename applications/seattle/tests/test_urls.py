from django.test import TestCase
from django.urls import reverse

from applications.core.utils import AuthenticatedTestCase

class HomepageTests(AuthenticatedTestCase):
    url_name = "seattle:seattle-homepage"

    def test_url_exists_at_correct_location(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "seattle/seattle_homepage.html")

class MapPageTests(AuthenticatedTestCase):
    url_name = "seattle:seattle-map"

    def test_url_exists_at_correct_location(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "seattle/map.html")


class HospitalsDataImportPageTests(AuthenticatedTestCase):
    url_name = "seattle:import-hospitals"

    def test_url_exists_at_correct_location(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "seattle/import_hospitals_data.html")

class HospitalsDataExporttPageTests(AuthenticatedTestCase):
    url_name = "seattle:export-hospitals"

    def test_url_exists_at_correct_location(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "seattle/export_hospitals_data.html")

class SchoolsDataImportPageTests(AuthenticatedTestCase):
    url_name = "seattle:import-schools"

    def test_url_exists_at_correct_location(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "seattle/import_schools_data.html")

class SchoolsDataExporttPageTests(AuthenticatedTestCase):
    url_name = "seattle:export-schools"

    def test_url_exists_at_correct_location(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "seattle/export_schools_data.html")


class LibrariesDataImportPageTests(AuthenticatedTestCase):
    url_name = "seattle:import-libraries"

    def test_url_exists_at_correct_location(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "seattle/import_libraries_data.html")

class LibrariesDataExporttPageTests(AuthenticatedTestCase):
    url_name = "seattle:export-libraries"

    def test_url_exists_at_correct_location(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "seattle/export_libraries_data.html")
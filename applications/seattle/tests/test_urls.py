from django.test import TestCase
from django.urls import reverse


class HomepageTests(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/seattle/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("seattle:seattle-homepage"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("seattle:seattle-homepage"))
        self.assertTemplateUsed(response, "seattle/seattle_homepage.html")

class MapPageTests(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/seattle/map/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("seattle:seattle-map"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("seattle:seattle-map"))
        self.assertTemplateUsed(response, "seattle/map.html")


class HospitalsDataImportPageTests(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/seattle/import-hospitals/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("seattle:import-hospitals"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("seattle:import-hospitals"))
        self.assertTemplateUsed(response, "seattle/import_hospitals_data.html")

class HospitalsDataExporttPageTests(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/seattle/export-hospitals/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("seattle:export-hospitals"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("seattle:export-hospitals"))
        self.assertTemplateUsed(response, "seattle/export_hospitals_data.html")

class SchoolsDataImportPageTests(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/seattle/import-schools/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("seattle:import-schools"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("seattle:import-schools"))
        self.assertTemplateUsed(response, "seattle/import_schools_data.html")

class SchoolsDataExporttPageTests(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/seattle/export-schools/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("seattle:export-schools"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("seattle:export-schools"))
        self.assertTemplateUsed(response, "seattle/export_schools_data.html")


class LibrariesDataImportPageTests(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/seattle/import-libraries/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("seattle:import-libraries"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("seattle:import-libraries"))
        self.assertTemplateUsed(response, "seattle/import_libraries_data.html")

class LibrariesDataExporttPageTests(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/seattle/export-libraries/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("seattle:export-libraries"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("seattle:export-libraries"))
        self.assertTemplateUsed(response, "seattle/export_libraries_data.html")
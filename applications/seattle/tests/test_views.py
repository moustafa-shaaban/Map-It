from django.test import RequestFactory, TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.contrib.messages import get_messages

import json
import csv
import io

from applications.seattle.models import School
# from applications.seattle.views import MapView


# class MapViewTests(TestCase):

#     def setUp(self):
#         self.url = reverse("seattle:seattle-map")  # update to your URL name

#         # Create test data
#         School.objects.create(
#             name="Test School",
#             address="123 Street",
#             latitude=47.60,
#             longitude=-122.33,
#         )

#     def test_map_view_loads(self):
#         response = self.client.get(self.url)

#         self.assertEqual(response.status_code, 200)
#         self.assertIn("map", response.context)
#         self.assertIn("count", response.context)

#     def test_map_contains_results(self):
#         response = self.client.get(self.url)

#         self.assertEqual(response.context["count"], 1)

#     def test_query_filters_results(self):
#         response = self.client.get(self.url, {"q": "Nonexistent"})

#         self.assertEqual(response.context["count"], 0)

#     def test_query_returns_results(self):
#         response = self.client.get(self.url, {"q": "Test"})

#         self.assertEqual(response.context["count"], 1)

#     def test_map_html_rendered(self):
#         response = self.client.get(self.url)

#         self.assertIn("<div", response.context["map"])


# class MarkerRenderingTests(TestCase):

#     def setUp(self):
#         self.factory = RequestFactory()

#     def test_render_does_not_crash(self):
#         request = self.factory.get("/")

#         view = MapView()
#         view.request = request

#         context = view.get_context_data()

#         self.assertIn("map", context)


def create_csv_file(content: list[list[str]]) -> bytes:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerows(content)
    return output.getvalue().encode('utf-8')


def create_excel_file(rows: list[list]):
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    for row in rows:
        ws.append(row)
    
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return output.getvalue()


def create_json_file(data: list[dict]) -> bytes:
    return json.dumps(data, indent=2).encode('utf-8')


class ImportHospitalsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('seattle:import-hospitals')

    def test_uploading_csv_file(self):
        csv_data = [
            ['facility', 'address', 'latitude', 'longitude'],
            ['UW Medical Center - Northwest', '1550 N 115th ST', 47.714248, -122.336888]
        ]
        file_content = create_csv_file(csv_data)

        uploaded_file = SimpleUploadedFile(
            "hospitals_data.csv",
            file_content,
            content_type="text/csv"
        )

        response = self.client.post(self.url, {'import_file': uploaded_file})

        self.assertIn('result', response.context)

        self.assertIn('import_data_cache', self.client.session)

    def test_uploading_excel_file(self):
        """Test uploading a real XLSX file → dry-run is performed and data is cached in session."""
        excel_data = [
            ['facility', 'address', 'latitude', 'longitude'],
            ['UW Medical Center - Northwest', '1550 N 115th ST', 47.714248, -122.336888]
        ]
        file_content = create_excel_file(excel_data)

        uploaded_file = SimpleUploadedFile(
            "hospitals_data.xlsx",
            file_content,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        response = self.client.post(self.url, {'import_file': uploaded_file})

        self.assertEqual(response.status_code, 200)

        form = response.context.get('form')
        if form and not form.is_valid():
            print("Form errors:", form.errors)
            print("Non-field errors:", form.non_field_errors())

        self.assertIn('result', response.context, 
                    "No 'result' in context → form was invalid or exception occurred")

        self.assertIn('import_data_cache', self.client.session,
                    "import_data_cache not set in session. Check parse_file() or resource.import_data()")
        
        cached_data = self.client.session['import_data_cache']
        self.assertGreater(len(cached_data), 0)

    def test_uploading_json_file(self):
        json_data = [{
            "facility": "University of Washington Medical Center",
            "address": "1959 NE Pacific St",
            "latitude": "47.650344",
            "longitude": "-122.309072"
        }]
        file_content = create_json_file(json_data)

        uploaded_file = SimpleUploadedFile(
            "test.json",
            file_content,
            content_type="application/json"
        )

        response = self.client.post(self.url, {'import_file': uploaded_file})
        self.assertEqual(response.status_code, 200)

    def test_submitting_csv_file(self):
        csv_data = [
            ['facility', 'address', 'latitude', 'longitude'],
            ['UW Medical Center - Northwest', '1550 N 115th ST', 47.714248, -122.336888]
        ]
        file_content = create_csv_file(csv_data)

        uploaded_file = SimpleUploadedFile("csv_data.csv", file_content, content_type="text/csv")
        self.client.post(self.url, {'import_file': uploaded_file})

        session = self.client.session
        session['import_data_cache'] = [
            {"id": "1", "name": "Confirmed Hospital"}
        ]
        session.save()

        response = self.client.post(self.url, {
            'confirm_import': 'true',
            'selected_rows': ['0']
        })

        self.assertRedirects(response, '/seattle/import-hospitals/')

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Import finished" in str(m) for m in messages))


    def test_submitting_excel_file(self):
        excel_data = [
            ['facility', 'address', 'latitude', 'longitude'],
            ['UW Medical Center - Northwest', '1550 N 115th ST', 47.714248, -122.336888]
        ]
        file_content = create_excel_file(excel_data)

        uploaded_file = SimpleUploadedFile("excel_data.xlsx", file_content, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        self.client.post(self.url, {'import_file': uploaded_file})

        session = self.client.session
        session['import_data_cache'] = [
            {"facility": "UW Medical Center - Northwest", "address": "1550 N 115th ST", "latitude": 47.714248, "longitude": -122.336888}
        ]
        session.save()
        response = self.client.post(self.url, {
            'confirm_import': 'true',
            'selected_rows': ['0']
        })

        self.assertRedirects(response, '/seattle/import-hospitals/')

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Import finished" in str(m) for m in messages))

    def test_submitting_json_file(self):
        json_data = [{
            "facility": "University of Washington Medical Center",
            "address": "1959 NE Pacific St",
            "latitude": "47.650344",
            "longitude": "-122.309072"
        }]
        file_content = create_json_file(json_data)

        uploaded_file = SimpleUploadedFile("json_data.csv", file_content, content_type="application/json")
        self.client.post(self.url, {'import_file': uploaded_file})

        session = self.client.session
        session['import_data_cache'] = [
            {"facility": "UW Medical Center - Northwest", "address": "1550 N 115th ST", "latitude": 47.714248, "longitude": -122.336888}
        ]
        session.save()
        response = self.client.post(self.url, {
            'confirm_import': 'true',
            'selected_rows': ['0']
        })

        self.assertRedirects(response, '/seattle/import-hospitals/')

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Import finished" in str(m) for m in messages))

    def test_csv_file_size_is_to_large(self):
        large_content = b"csv content" * (10 * 1024 * 1024)
        uploaded_file = SimpleUploadedFile("large_csv_file_size.csv", large_content, content_type="text/csv")

        response = self.client.post(self.url, {'import_file': uploaded_file})
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn("File exceeded the maximum size. Max size is 5MB.", str(form.errors))

    def test_excel_file_size_is_to_large(self):
        large_content = b"content" * (10 * 1024 * 1024)
        uploaded_file = SimpleUploadedFile("large_excel_file_size.xlsx", large_content, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        response = self.client.post(self.url, {'import_file': uploaded_file})
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn("File exceeded the maximum size. Max size is 5MB.", str(form.errors))

    def test_json_file_size_is_to_large(self):
        large_content = b"content" * (10 * 1024 * 1024)
        uploaded_file = SimpleUploadedFile("large_json_file_size.jsox", large_content, content_type="application/json")

        response = self.client.post(self.url, {'import_file': uploaded_file})
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn("File exceeded the maximum size. Max size is 5MB.", str(form.errors))


class ImportSchoolsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('seattle:import-schools')

    def test_uploading_csv_file(self):
        csv_data = [
            ['name', 'address', 'latitude', 'longitude'],
            ['Louisa Boren STEM', '1431 2nd Ave N', 47.548620, -122.362141]
        ]
        file_content = create_csv_file(csv_data)

        uploaded_file = SimpleUploadedFile(
            "schools_data.csv",
            file_content,
            content_type="text/csv"
        )

        response = self.client.post(self.url, {'import_file': uploaded_file})

        self.assertIn('result', response.context)

        self.assertIn('import_data_cache', self.client.session)

    def test_uploading_excel_file(self):
        excel_data = [
            ['name', 'address', 'latitude', 'longitude'],
            ['Louisa Boren STEM', '1431 2nd Ave N', 47.548620, -122.362141]
        ]
        file_content = create_excel_file(excel_data)

        uploaded_file = SimpleUploadedFile(
            "schools_data.xlsx",
            file_content,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        response = self.client.post(self.url, {'import_file': uploaded_file})

        self.assertEqual(response.status_code, 200)

        form = response.context.get('form')
        if form and not form.is_valid():
            print("Form errors:", form.errors)
            print("Non-field errors:", form.non_field_errors())

        self.assertIn('result', response.context, 
                    "No 'result' in context → form was invalid or exception occurred")

        self.assertIn('import_data_cache', self.client.session,
                    "import_data_cache not set in session. Check parse_file() or resource.import_data()")
        
        cached_data = self.client.session['import_data_cache']
        self.assertGreater(len(cached_data), 0)

    def test_uploading_json_file(self):
        json_data = [{
            "name": "Louisa Boren STEM",
            "address": "5950 Delridge Way SW",
            "latitude": "47.548620",
            "longitude": "-122.362141"
        }]
        file_content = create_json_file(json_data)

        uploaded_file = SimpleUploadedFile(
            "schools_data.json",
            file_content,
            content_type="application/json"
        )

        response = self.client.post(self.url, {'import_file': uploaded_file})
        self.assertEqual(response.status_code, 200)

    def test_submitting_csv_file(self):
        csv_data = [
            ['name', 'address', 'latitude', 'longitude'],
            ['Louisa Boren STEM', '1431 2nd Ave N', 47.548620, -122.362141]
        ]
        file_content = create_csv_file(csv_data)

        uploaded_file = SimpleUploadedFile("csv_data.csv", file_content, content_type="text/csv")
        self.client.post(self.url, {'import_file': uploaded_file})

        session = self.client.session
        session['import_data_cache'] = [
            {
                "name": "Louisa Boren STEM",
                "address": "5950 Delridge Way SW",
                "latitude": "47.548620",
                "longitude": "-122.362141"
            }
        ]
        session.save()

        response = self.client.post(self.url, {
            'confirm_import': 'true',
            'selected_rows': ['0']
        })

        self.assertRedirects(response, '/seattle/import-schools/')

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Import finished" in str(m) for m in messages))
    
    def test_submitting_excel_file(self):
        excel_data = [
            ['name', 'address', 'latitude', 'longitude'],
            ['Louisa Boren STEM', '1431 2nd Ave N', 47.548620, -122.362141]
        ]
        file_content = create_excel_file(excel_data)

        uploaded_file = SimpleUploadedFile("excel_data.xlsx", file_content, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        self.client.post(self.url, {'import_file': uploaded_file})

        session = self.client.session
        session['import_data_cache'] = [
            {
                "name": "Louisa Boren STEM",
                "address": "5950 Delridge Way SW",
                "latitude": "47.548620",
                "longitude": "-122.362141"
            }
        ]
        session.save()

        response = self.client.post(self.url, {
            'confirm_import': 'true',
            'selected_rows': ['0']
        })

        self.assertRedirects(response, '/seattle/import-schools/')

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Import finished" in str(m) for m in messages))
    
    def test_submitting_json_file(self):
        json_data = [{
            "facility": "Louisa Boren STEM",
            "address": "5950 Delridge Way SW",
            "latitude": "47.548620",
            "longitude": "-122.362141"
        }]
        file_content = create_json_file(json_data)

        uploaded_file = SimpleUploadedFile("json_data.csv", file_content, content_type="application/json")
        self.client.post(self.url, {'import_file': uploaded_file})

        session = self.client.session
        session['import_data_cache'] = [
            {"facility": "Louisa Boren STEM", "address": "5950 Delridge Way SW", "latitude": 47.548620, "longitude": -122.362141}
        ]
        session.save()
        response = self.client.post(self.url, {
            'confirm_import': 'true',
            'selected_rows': ['0']
        })

        self.assertRedirects(response, '/seattle/import-schools/')

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Import finished" in str(m) for m in messages))
    
    def test_csv_file_size_is_to_large(self):
        large_content = b"content" * (10 * 1024 * 1024)
        uploaded_file = SimpleUploadedFile("big.csv", large_content, content_type="text/csv")

        response = self.client.post(self.url, {'import_file': uploaded_file})
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn("File exceeded the maximum size. Max size is 5MB.", str(form.errors))

    def test_excel_file_size_is_to_large(self):
        large_content = b"content" * (10 * 1024 * 1024)
        uploaded_file = SimpleUploadedFile("large_excel_file_size.xlsx", large_content, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        response = self.client.post(self.url, {'import_file': uploaded_file})
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn("File exceeded the maximum size. Max size is 5MB.", str(form.errors))

    def test_json_file_size_is_to_large(self):
        large_content = b"content" * (10 * 1024 * 1024)
        uploaded_file = SimpleUploadedFile("large_json_file_size.jsox", large_content, content_type="application/json")

        response = self.client.post(self.url, {'import_file': uploaded_file})
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn("File exceeded the maximum size. Max size is 5MB.", str(form.errors))


class ImportLibrariesTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('seattle:import-libraries')

    def test_uploading_csv_file(self):
        csv_data = [
            ['name', 'address', 'latitude', 'longitude'],
            ['BROADVIEW', '12755 GREENWOOD AV N', 47.723004, -122.356032]
        ]
        file_content = create_csv_file(csv_data)

        uploaded_file = SimpleUploadedFile(
            "libraries_data.csv",
            file_content,
            content_type="text/csv"
        )

        response = self.client.post(self.url, {'import_file': uploaded_file})

        self.assertIn('result', response.context)
        self.assertIn('import_data_cache', self.client.session)

    def test_uploading_excel_file(self):
        excel_data = [
            ['name', 'address', 'latitude', 'longitude'],
            ['BROADVIEW', '12755 GREENWOOD AV N', 47.723004, -122.356032]
        ]
        file_content = create_excel_file(excel_data)

        uploaded_file = SimpleUploadedFile(
            "libraries_data.xlsx",
            file_content,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        response = self.client.post(self.url, {'import_file': uploaded_file})

        self.assertEqual(response.status_code, 200)

        form = response.context.get('form')
        if form and not form.is_valid():
            print("Form errors:", form.errors)
            print("Non-field errors:", form.non_field_errors())

        self.assertIn('result', response.context, 
                    "No 'result' in context → form was invalid or exception occurred")

        self.assertIn('import_data_cache', self.client.session,
                    "import_data_cache not set in session. Check parse_file() or resource.import_data()")
        
        cached_data = self.client.session['import_data_cache']
        self.assertGreater(len(cached_data), 0)

    def test_uploading_json_file(self):
        json_data = [{
            "name": "BROADVIEW",
            "address": "12755 GREENWOOD AV N",
            "latitude": "47.723004",
            "longitude": "-122.356032"
        }]
        file_content = create_json_file(json_data)

        uploaded_file = SimpleUploadedFile(
            "libraries_data.json",
            file_content,
            content_type="application/json"
        )

        response = self.client.post(self.url, {'import_file': uploaded_file})
        self.assertEqual(response.status_code, 200)

    def test_submitting_csv_file(self):
        csv_data = [
            ['name', 'address', 'latitude', 'longitude'],
            ['BROADVIEW', '12755 GREENWOOD AV N', 47.723004, -122.356032]
        ]
        file_content = create_csv_file(csv_data)

        uploaded_file = SimpleUploadedFile("csv_data.csv", file_content, content_type="text/csv")
        self.client.post(self.url, {'import_file': uploaded_file})

        session = self.client.session
        session['import_data_cache'] = [
            {
                "name": "BROADVIEW",
                "address": "12755 GREENWOOD AV N",
                "latitude": "47.723004",
                "longitude": "-122.356032"
            }
        ]
        session.save()

        response = self.client.post(self.url, {
            'confirm_import': 'true',
            'selected_rows': ['0']
        })

        self.assertRedirects(response, '/seattle/import-libraries/')

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Import finished" in str(m) for m in messages))
    
    def test_submitting_excel_file(self):
        excel_data = [
            ['name', 'address', 'latitude', 'longitude'],
            ['BROADVIEW', '12755 GREENWOOD AV N', 47.723004, -122.356032]
        ]
        file_content = create_excel_file(excel_data)

        uploaded_file = SimpleUploadedFile("excel_data.xlsx", file_content, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        self.client.post(self.url, {'import_file': uploaded_file})

        session = self.client.session
        session['import_data_cache'] = [
            {
                "name": "BROADVIEW",
                "address": "12755 GREENWOOD AV N",
                "latitude": "47.723004",
                "longitude": "-122.356032"
            }
        ]
        session.save()

        response = self.client.post(self.url, {
            'confirm_import': 'true',
            'selected_rows': ['0']
        })

        self.assertRedirects(response, '/seattle/import-libraries/')

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Import finished" in str(m) for m in messages))
    
    def test_submitting_json_file(self):
        json_data = [            {
                "name": "BROADVIEW",
                "address": "12755 GREENWOOD AV N",
                "latitude": "47.723004",
                "longitude": "-122.356032"
        }]
        file_content = create_json_file(json_data)

        uploaded_file = SimpleUploadedFile("json_data.csv", file_content, content_type="application/json")
        self.client.post(self.url, {'import_file': uploaded_file})

        session = self.client.session
        session['import_data_cache'] = [
            {
                "name": "BROADVIEW",
                "address": "12755 GREENWOOD AV N",
                "latitude": "47.723004",
                "longitude": "-122.356032"
            }
        ]
        session.save()
        response = self.client.post(self.url, {
            'confirm_import': 'true',
            'selected_rows': ['0']
        })

        self.assertRedirects(response, '/seattle/import-libraries/')

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Import finished" in str(m) for m in messages))
    
    def test_csv_file_size_is_to_large(self):
        large_content = b"content" * (10 * 1024 * 1024)
        uploaded_file = SimpleUploadedFile("big.csv", large_content, content_type="text/csv")

        response = self.client.post(self.url, {'import_file': uploaded_file})
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn("File exceeded the maximum size. Max size is 5MB.", str(form.errors))

    def test_excel_file_size_is_to_large(self):
        large_content = b"content" * (10 * 1024 * 1024)
        uploaded_file = SimpleUploadedFile("large_excel_file_size.xlsx", large_content, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        response = self.client.post(self.url, {'import_file': uploaded_file})
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn("File exceeded the maximum size. Max size is 5MB.", str(form.errors))

    def test_json_file_size_is_to_large(self):
        large_content = b"content" * (10 * 1024 * 1024)
        uploaded_file = SimpleUploadedFile("large_json_file_size.jsox", large_content, content_type="application/json")

        response = self.client.post(self.url, {'import_file': uploaded_file})
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn("File exceeded the maximum size. Max size is 5MB.", str(form.errors))

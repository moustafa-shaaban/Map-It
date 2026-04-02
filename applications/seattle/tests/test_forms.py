import tempfile
import json
import csv
from io import BytesIO, StringIO
from unittest.mock import patch, MagicMock

from django.forms import ValidationError
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages import get_messages
from django.contrib.auth.models import User
from django.conf import settings

from applications.seattle.forms import UploadFileForm, validate_file_size, validate_file_type
from applications.seattle.models import Hospital, School, Library
from applications.seattle.resources import HospitalResource, SchoolResource, LibraryResource
from applications.seattle.resources import HospitalResource, SchoolResource, LibraryResource


class UploadFileFormTest(TestCase):
    """Test cases for UploadFileForm"""

    def setUp(self):
        """Set up test data"""
        self.valid_csv_content = b"name,address,city\nHospital1,123 Main St,Seattle\nHospital2,456 Oak Ave,Portland"
        self.valid_json_content = b'[{"name": "Hospital1", "address": "123 Main St", "city": "Seattle"}]'

    def create_temp_file(self, content, filename, content_type):
        """Helper to create a temporary file for testing"""
        return SimpleUploadedFile(
            filename,
            content,
            content_type=content_type
        )
    
    def test_valid_csv_file(self):
        """Test form accepts valid CSV file"""
        file = self.create_temp_file(
            self.valid_csv_content,
            'test.csv',
            'text/csv'
        )
        form = UploadFileForm(
            {'import_file': file},
            {'import_file': file}
        )
        # Mock the file type validation to avoid magic dependency
        with patch('applications.seattle.forms.validate_file_type') as mock_validate:
            mock_validate.return_value = None
            self.assertTrue(form.is_valid())

    def test_valid_json_file(self):
        """Test form accepts valid JSON file"""
        file = self.create_temp_file(
            self.valid_json_content,
            'test.json',
            'application/json'
        )
        form = UploadFileForm(
            {'import_file': file},
            {'import_file': file}
        )
        with patch('applications.seattle.forms.validate_file_type') as mock_validate:
            mock_validate.return_value = None
            self.assertTrue(form.is_valid())
    
    def test_invalid_file_extension(self):
        """Test form rejects invalid file extensions"""
        file = self.create_temp_file(
            b"invalid content",
            'test.txt',
            'text/plain'
        )
        form = UploadFileForm(
            {'import_file': file},
            {'import_file': file}
        )
        with patch('applications.seattle.forms.validate_file_type') as mock_validate:
            mock_validate.return_value = None
            self.assertFalse(form.is_valid())
            self.assertIn('import_file', form.errors)
    
    def test_empty_file(self):
        """Test form rejects empty file"""
        file = SimpleUploadedFile(
            'empty.csv',
            b'',
            content_type='text/csv'
        )
        form = UploadFileForm(
            {'import_file': file},
            {'import_file': file}
        )
        self.assertFalse(form.is_valid())

    def test_file_size_validator(self):
        # Create a mock file with size within limit
        small_file = MagicMock()
        small_file.size = 4 * 1024 * 1024  # 4MB

        try:
            validate_file_size(small_file)
        except Exception as e:
            self.fail(f"validate_file_size raised unexpectedly: {e}")

        large_file = MagicMock()
        large_file.size = 6 * 1024 * 1024  # 6MB
        with self.assertRaises(ValidationError) as context:
            validate_file_size(large_file)
        self.assertIn("exceeded the maximum size", str(context.exception))
    

class FileTypeValidationTest(TestCase):
    """Test cases for file type validation"""
    @patch('applications.seattle.forms.magic')
    def test_valid_csv_mime_type(self, mock_magic):
        """Test validation passes for CSV MIME type"""
        
        mock_magic.from_buffer.return_value = 'text/csv'
        file = BytesIO(b"name,address\nHospital1,123 Main St")
        file.name = 'test.csv'
        
        try:
            validate_file_type(file)
        except ValidationError as e:
            self.fail(f"validate_file_type raised unexpectedly: {e}")
    
    @patch('applications.seattle.forms.magic')
    def test_invalid_mime_type(self, mock_magic):
        """Test validation fails for invalid MIME type"""
        
        mock_magic.from_buffer.return_value = 'application/octet-stream'
        file = BytesIO(b"invalid content")
        file.name = 'test.csv'
        
        with self.assertRaises(ValidationError) as context:
            validate_file_type(file)
        self.assertIn("does not match the allowed types", str(context.exception))
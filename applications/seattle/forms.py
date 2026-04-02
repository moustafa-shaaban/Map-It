from django import forms
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

import magic

extension_validators = [
    'csv',
    'xlsx',
    'json'
]

def validate_file_size(file):
    max_size = 5 * 1024 * 1024  # 5MB
    if file.size > max_size:
        raise ValidationError(f'File exceeded the maximum size. Max size is 5MB.')
    

def validate_file_type(file):
    file_content = file.read(4096)
    file.seek(0)
    mime = magic.from_buffer(file_content, mime=True)
    
    allowed_mimes = [
        'text/csv', 
        'application/json',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'text/plain',
        'application/zip',
    ]
    if mime not in allowed_mimes:
        raise ValidationError('The file content does not match the allowed types, (.csv, .xlsx, .json)')
    

class UploadFileForm(forms.Form):
    import_file = forms.FileField(
        label='Select file',
        validators=[FileExtensionValidator(allowed_extensions=extension_validators), validate_file_size, validate_file_type],
        widget=forms.FileInput(
            attrs={
                'name': 'import_file',
                'class': 'form-control', 
                'accept': '.csv,.xlsx,.json',
            }
        )
    )


class ExportForm(forms.Form):
    FORMAT_CHOICES = [
        ('csv', 'Comma Separated Values (CSV)'),
        ('xlsx', 'Microsoft Excel (XLSX)'),
        ('json', 'JavaScript Object Notation (JSON)'),
    ]

    format = forms.ChoiceField(
        choices=FORMAT_CHOICES,
        label='Choose Format'
    )
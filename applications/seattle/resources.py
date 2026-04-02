from import_export import resources
from .models import Hospital, School, Library
from .utils import normalize_text

class HospitalResource(resources.ModelResource):
    class Meta:
        model = Hospital
        exclude = ('id',)
        import_id_fields = ('facility',)
        skip_unchanged = True
        report_skipped = True

    def before_import_row(self, row, **kwargs):
        if row.get('facility'):
            row['facility'] = normalize_text(row['facility'])
        if row.get('address'):
            row['address'] = normalize_text(row['address'])
    


class SchoolResource(resources.ModelResource):
    class Meta:
        model = School
        import_id_fields = ('name',)
        skip_unchanged = True
        report_skipped = True

    def before_import_row(self, row, **kwargs):
        if row.get('name'):
            row['name'] = normalize_text(row['name'])
        if row.get('address'):
            row['address'] = normalize_text(row['address'])


class LibraryResource(resources.ModelResource):
    class Meta:
        model = Library
        import_id_field = ('name',)
        skip_unchanged = True
        report_skipped = True

    def before_import_row(self, row, **kwargs):
        if row.get('name'):
            row['name'] = normalize_text(row['name'])
        if row.get('address'):
            row['address'] = normalize_text(row['address'])
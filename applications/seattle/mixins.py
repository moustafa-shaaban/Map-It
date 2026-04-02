from datetime import datetime
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib import messages
from django.views import View
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext as _
from django.http import HttpResponse
from tablib import Dataset

from import_export.results import RowResult

from .forms import UploadFileForm, ExportForm

class BaseDataImport(View):
    """
    Reusable import view for any model + resource.

    Subclass this and override:
        - template_name
        - resource_class
        - success_redirect_url
        - import_success_message
    """
    model = None
    template_name = None
    resource_class = None
    success_url = None
    import_success_message = "Import completed successfully."

    def add_success_message(self, result, request):
        if not result.has_errors() and result.total_rows == 0:
            messages.warning(request, _("Import completed, but no records were changed."))
            return
        if not self.model:
            # Fallback if model isn't defined: use a generic name
            plural_name = "records"
        else:
            plural_name = self.model._meta.verbose_name_plural
        success_message = _(
            "Import finished: {} new, {} updated, {} deleted and {} skipped {}."
        ).format(
            result.totals.get(RowResult.IMPORT_TYPE_NEW, 0),
            result.totals.get(RowResult.IMPORT_TYPE_UPDATE, 0),
            result.totals.get(RowResult.IMPORT_TYPE_DELETE, 0),
            result.totals.get(RowResult.IMPORT_TYPE_SKIP, 0),
            plural_name,
        )
        messages.success(request, success_message)

    def get_success_url(self):
        return self.success_url
    
    
    def get(self, request):
        form = UploadFileForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        resource = self.resource_class()

        if 'cancel_import' in request.POST:
            if 'import_data_cache' in request.session:
                del request.session['import_data_cache']
            messages.info(request, "Import cancelled and temporary data cleared.")
            return redirect(request.path)

        if 'confirm_import' in request.POST:
            return self.handle_confirmation(request, resource)
        
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            import_file = form.cleaned_data['import_file']
            
            try:
                dataset = self.parse_file(import_file)
                
                request.session['import_data_cache'] = dataset.dict
                
                result = resource.import_data(dataset, dry_run=True)
                return render(request, self.template_name, {
                    'result': result,
                    'form': form
                })
            except Exception as e:
                messages.error(request, f"Parsing error: {str(e)}")
                return render(request, self.template_name, {'form': form})
            
        else:
            return render(request, self.template_name, {'form': form})

    def parse_file(self, import_file):
        dataset = Dataset()
        extension = import_file.name.split('.')[-1].lower()
        content = import_file.read()
        
        if extension == 'csv':
            dataset.load(content.decode('utf-8'), format='csv')
        elif extension == 'xlsx':
            dataset.load(content, format='xlsx')
        elif extension == 'json':
            dataset.load(content.decode('utf-8'), format='json')
        else:
            raise ValueError("Unsupported extension.")
        return dataset

    def handle_confirmation(self, request, resource):
        import_data = request.session.get('import_data_cache')
        selected_indices = request.POST.getlist('selected_rows')

        if not import_data or not selected_indices:
            messages.error(request, "Session expired or no rows selected.")
            return redirect(request.path)

        filtered_data = [import_data[int(i)] for i in selected_indices]
        dataset = Dataset()
        dataset.dict = filtered_data
        
        result = resource.import_data(dataset, dry_run=False)
        del request.session['import_data_cache']
        self.add_success_message(result, request)
        return redirect(self.success_url)
    

class BaseDataExport(View):
    resource_class = None
    filename = 'export'
    template_name = 'export.html'

    def get_resource(self):
        if not self.resource_class:
            raise ImproperlyConfigured('resource_class is required.')
        return self.resource_class()

    def get_queryset(self):
        raise NotImplementedError

    def get(self, request, *args, **kwargs):
        form = ExportForm()
        count = self.get_queryset().count()
        context = {
            'form': form,
            'count': count,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = ExportForm(request.POST)

        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        fmt = form.cleaned_data['format']
        resource = self.get_resource()
        queryset = self.get_queryset()

        dataset = resource.export(queryset)
        data = dataset.export(fmt)

        response = HttpResponse(
            data,
            content_type=self.get_content_type(fmt)
        )
        response['Content-Disposition'] = (
            f'attachment; filename="{self.get_filename(fmt)}"'
        )

        return response

    def get_filename(self, fmt):
        date = datetime.now().strftime('%Y-%m-%d')
        return f'{self.filename}_{date}.{fmt}'

    def get_content_type(self, fmt):
        return {
            'csv': 'text/csv',
            'json': 'application/json',
            'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        }[fmt]
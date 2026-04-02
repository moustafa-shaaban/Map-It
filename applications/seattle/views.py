import folium
from folium.plugins import MarkerCluster, Fullscreen, LocateControl, Geocoder
from django.shortcuts import render
from django.utils.html import escape
from django.views import generic
from django.views.generic import TemplateView
# from django.utils.html import escape

from .models import Hospital, School, Library
from .resources import HospitalResource, SchoolResource, LibraryResource
from .utils import render_markers
from .filters import SchoolFilter, LibraryFilter, HospitalFilter
from .mixins import BaseDataImport, BaseDataExport



class HomePage(generic.TemplateView):
    """ Class used for displaying website's main page. """
    template_name = 'seattle/seattle_homepage.html'


LAYERS = [
    {
        'model': School,
        'filter': SchoolFilter,
        'fields': ('name', 'address'),     ''
        'icon': {'icon': 'graduation-cap', 'prefix': 'fa'},                 
        'label': 'Schools'
    },
    {
        'model': Library,
        'filter': LibraryFilter, 
        'fields': ('name', 'address'),     
        'icon': {'icon': 'book', 'prefix': 'fa'},                 
        'label': 'Libraries'
    },
    {
        'model': Hospital,
        'filter': HospitalFilter,
        'fields': ('facility', 'address'), 
        'icon': {'icon': 'h-square', 'prefix': 'fa', 'color': 'red'}, 
        'label': 'Hospitals'
    },
]

DEFAULT_LOCATION = [47.6062100, -122.3320700]
DEFAULT_ZOOM     = 11


class MapView(TemplateView):
    """Source: ChatGPT"""
    template_name = "seattle/map.html"

    layers = LAYERS
    default_location = DEFAULT_LOCATION
    default_zoom = DEFAULT_ZOOM
    map_tiles = "cartodbpositron"
    map_attr = "Seattle City"

    # ----------------------------
    # Query + Filtering
    # ----------------------------
    def get_query(self):
        return self.request.GET.get("q", "").strip()
    
    def get_filtered_layers(self):
        return [
            {
                **layer,
                "queryset": layer["filter"](
                    self.request.GET,
                    queryset=layer["model"].objects.only(
                        "latitude", "longitude", *layer["fields"]
                    ),
                ).qs,
            }
            for layer in self.layers
        ]

    # ----------------------------
    # Map Creation
    # ----------------------------
    def get_map(self):
        folium_map = folium.Map(
            location=self.default_location,
            tiles=self.map_tiles,
            zoom_start=self.default_zoom,
            attr=self.map_attr,
        )
        folium.TileLayer("cartodbdark_matter").add_to(folium_map)
        return folium_map

    # ----------------------------
    # Marker Rendering
    # ----------------------------
    def render_markers(self, folium_map, layer):
        queryset = layer["queryset"]
        tooltip_field, popup_field = layer["fields"]

        simple_markers = folium.FeatureGroup(
            name=f"{layer['label']} Simple Markers",
            show=True,
        ).add_to(folium_map)

        clustered_group = folium.FeatureGroup(
            name=f"{layer['label']} Marker Cluster",
            show=False,
        ).add_to(folium_map)

        cluster = MarkerCluster().add_to(clustered_group)

        for obj in queryset:
            coords = [obj.latitude, obj.longitude]

            tooltip = f"{layer['label']}: {escape(str(getattr(obj, tooltip_field)))}"
            popup = f"Address: {escape(str(getattr(obj, popup_field)))}"

            marker = folium.Marker(
                coords,
                icon=folium.Icon(**layer["icon"]),
                tooltip=tooltip,
                popup=popup,
            )

            marker.add_to(simple_markers)
            marker.add_to(cluster)

    # ----------------------------
    # Collect Coordinates
    # ----------------------------
    def get_all_coords(self, filtered_layers):
        return [
            [obj.latitude, obj.longitude]
            for layer in filtered_layers
            for obj in layer["queryset"]
        ]

    # ----------------------------
    # Fit Bounds / Empty State
    # ----------------------------
    def handle_bounds(self, folium_map, query, all_coords):
        if query and all_coords:
            folium_map.fit_bounds(all_coords)
        elif query and not all_coords:
            folium.Marker(
                self.default_location,
                icon=folium.Icon(color="red", icon="exclamation", prefix="fa"),
                tooltip="No results found for your search.",
            ).add_to(folium_map)

    # ----------------------------
    # Add Controls
    # ----------------------------
    def add_controls(self, folium_map):
        folium.LayerControl(position="topright").add_to(folium_map)
        Fullscreen().add_to(folium_map)
        LocateControl().add_to(folium_map)
        Geocoder().add_to(folium_map)
        folium.LatLngPopup().add_to(folium_map)

    # ----------------------------
    # Main Context Builder
    # ----------------------------
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        query = self.get_query()
        filtered_layers = self.get_filtered_layers()

        folium_map = self.get_map()

        for layer in filtered_layers:
            self.render_markers(folium_map, layer)

        all_coords = self.get_all_coords(filtered_layers)

        self.handle_bounds(folium_map, query, all_coords)
        self.add_controls(folium_map)

        context.update({
            "map": folium_map._repr_html_(),
            "query": query,
            "count": len(all_coords),
        })

        return context

"""
 The following code (LAYERS + map_view function) + the `render_markers` function in the utils.py file is generated by Claude code.
 the main function i used before in the `django_and_folium` project (https://github.com/moustafa-shaaban/django_and_folium) 
 you can find it statring from line 160 to 279 of this file, 
 it does not follow the DRY (Don't Repeat Yourself) principle but it got the job done at that time.
"""

def map_view(request):
    query = request.GET.get('q', '').strip()

    filtered_layers = [
        {**layer, 'queryset': layer['filter'](request.GET, queryset=layer['model'].objects.only(
            'latitude', 'longitude', *layer['fields']
        )).qs}
        for layer in LAYERS
    ]

    all_coords = [
        [obj.latitude, obj.longitude]
        for layer in filtered_layers
        for obj in layer['queryset']
    ]

    folium_map = folium.Map(
        location=DEFAULT_LOCATION,
        tiles='cartodbpositron',
        zoom_start=DEFAULT_ZOOM,
        attr='Seattle City'
    )
    folium.TileLayer('cartodbdark_matter').add_to(folium_map)

    for layer in filtered_layers:
        render_markers(folium_map, layer, layer['queryset'])

    if query and all_coords:
        folium_map.fit_bounds(all_coords)
    elif query and not all_coords:
        folium.Marker(
            DEFAULT_LOCATION,
            icon=folium.Icon(color='red', icon='exclamation', prefix='fa'),
            tooltip='No results found for your search.',
        ).add_to(folium_map)

    folium.LayerControl(position='topright').add_to(folium_map)
    Fullscreen().add_to(folium_map)
    LocateControl().add_to(folium_map)
    Geocoder().add_to(folium_map)
    folium.LatLngPopup().add_to(folium_map)

    context = {
        'map':   folium_map._repr_html_(),
        'query': query,
        'count': len(all_coords)
    }
    return render(request, 'seattle/map.html', context)



class ImportHospitalsView(BaseDataImport):
    model = Hospital
    template_name = "seattle/import_hospitals_data.html"
    resource_class = HospitalResource
    success_url = 'seattle:import-hospitals'



class ImportSchoolsView(BaseDataImport):
    model = School
    template_name = "seattle/import_schools_data.html"
    resource_class = SchoolResource
    success_url = 'seattle:import-schools'


class ImportLibrariesView(BaseDataImport):
    model = Library
    template_name = "seattle/import_libraries_data.html"
    resource_class = LibraryResource
    success_url = 'seattle:import-libraries'




class HospitalsExportView(BaseDataExport):
    resource_class = HospitalResource
    filename = 'hospitals'
    template_name = "seattle/export_hospitals_data.html"

    def get_queryset(self):
        return Hospital.objects.all()



class SchoolsExportView(BaseDataExport):
    resource_class = SchoolResource
    filename = 'schools'
    template_name = "seattle/export_schools_data.html"

    def get_queryset(self):
        return School.objects.all()



class LibrariesExportView(BaseDataExport):
    resource_class = LibraryResource
    filename = 'libraries'
    template_name = "seattle/export_libraries_data.html"

    def get_queryset(self):
        return Library.objects.all()
    


# def index(request):
#     # Create folium basemap
#     folium_map = folium.Map(
#         location=[47.6062100, -122.3320700],
#         tiles='cartodbpositron',
#         zoom_start=11,
#         attr= 'Private Schoolss in Seattle'
#     )

#     # Add a second TileLayer to the basemap
#     folium.TileLayer('cartodbdark_matter').add_to(folium_map)


#     # Add Schools Data
#     schools = School.objects.all()

#     schools_simple_markers = folium.FeatureGroup(name='Schools Simple Markers').add_to(folium_map)

#     for school in schools:
#         locations = [school.latitude, school.longitude]
#         folium.Marker(
#             locations,
#             icon=folium.Icon(icon = "graduation-cap", prefix='fa'),
#             tooltip="School Name: " + escape(school.name),
#             popup="School Address :" + escape(school.address),
#     ).add_to(schools_simple_markers)

#     schools_marker_cluster = folium.FeatureGroup(name='Schools Marker Cluster', show=False).add_to(folium_map)

#     marker_cluster = MarkerCluster()

#     for school in schools:
#         locations = [school.latitude, school.longitude]
#         marker_cluster.add_child(
#             folium.Marker(
#                 locations,
#                 icon=folium.Icon(icon = "graduation-cap", prefix='fa'),
#                 tooltip="School Name: " + escape(school.name),
#                 popup="School Address :" + escape(school.address),
#             )
#         ).add_to(schools_marker_cluster)

#     ##################################################################################################

#     # Add Libraries data:
#     libraries = Library.objects.all()

#     libraries_simple_markers = folium.FeatureGroup(name='Libraries Simple Markers', show=False).add_to(folium_map)

#     for library in libraries:
#         locations = [library.latitude, library.longitude]
#         folium.Marker(
#             locations,
#             icon=folium.Icon(icon = "book", prefix='fa'),
#             tooltip="Library Name: " + escape(library.name),
#             popup="Library Address :" + escape(library.address),
#         ).add_to(libraries_simple_markers)

#     libraries_marker_cluster = folium.FeatureGroup(name='Libraries Marker Cluster', show=False).add_to(folium_map)

#     marker_cluster = MarkerCluster()

#     for library in libraries:
#         locations = [library.latitude, library.longitude]
#         marker_cluster.add_child(
#             folium.Marker(
#                 locations,
#                 icon=folium.Icon(icon = "book", prefix='fa'),
#                 tooltip="Library Name: " + escape(library.name),
#                 popup="Library Address :" + escape(library.address),
#             )
#         ).add_to(libraries_marker_cluster)

#     ##################################################################################################

#     # Add Hospitals data
#     hospitals = Hospital.objects.all()

#     hospitals_simple_markers = folium.FeatureGroup(name='Hospitals Simple Markers', show=False).add_to(folium_map)

#     for hospital in hospitals:
#         locations = [hospital.latitude, hospital.longitude]
#         folium.Marker(
#             locations,
#             icon=folium.Icon(icon_color = "red", icon = "h-square", prefix='fa'),
#             tooltip="Hospital Name: " + escape(hospital.facility),
#             popup="Hospital Address :" + escape(hospital.address),
#         ).add_to(hospitals_simple_markers)

#     hospitals_marker_cluster = folium.FeatureGroup(name='Hospitals Marker Cluster', show=False).add_to(folium_map)

#     marker_cluster = MarkerCluster()

#     for hospital in hospitals:
#         locations = [hospital.latitude, hospital.longitude]
#         marker_cluster.add_child(
#             folium.Marker(
#                 locations,
#                 icon=folium.Icon(icon_color = "red", icon = "h-square", prefix='fa'),
#                 tooltip="Hospital Name: " + escape(hospital.facility),
#                 popup="Hospital Address :" + escape(hospital.address),
#             )
#         ).add_to(hospitals_marker_cluster)
#     ##################################################################################################

#     folium.LayerControl(position='topright').add_to(folium_map)
#     Fullscreen().add_to(folium_map)
#     LocateControl().add_to(folium_map)
#     Geocoder().add_to(folium_map)
#     folium.LatLngPopup().add_to(folium_map)

#     folium_map.get_root().height = "100%"

#     map_context = folium_map._repr_html_()

#     context = {
#         'map': map_context
#     }

#     return render(request, 'map.html', context)

########################################################################################################


# def import_hospitals_data(request):
#     if request.method == 'POST':
#         file_format = request.POST['file-format']
#         hospital_resource = HospitalResource()
#         dataset = Dataset()
#         # new_hospitals = request.FILES['importData']

#         if file_format == 'CSV':
#             # imported_data = dataset.load(new_hospitals.read().decode('utf-8'),format='csv')
#             result = hospital_resource.import_data(dataset, dry_run=True)

#         elif file_format == 'JSON':
#             # imported_data = dataset.load(new_hospitals.read().decode('utf-8'),format='json')
#             # Testing data import
#             result = hospital_resource.import_data(dataset, dry_run=True)

#         if not result.has_errors():
#             # Import now
#             hospital_resource.import_data(dataset, dry_run=False)
#             messages.success(request, 'Data Imported Successfully.')

#     return render(request, 'seattle/import_hospitals_data.html')

# def export_hospitals_data(request):
#     if request.method == 'POST':
#         # Get selected option from form
#         file_format = request.POST['file-format']
#         hospital_resource = HospitalResource()
#         dataset = hospital_resource.export()

#         if file_format == 'CSV':
#             response = HttpResponse(dataset.csv, content_type='text/csv')
#             response['Content-Disposition'] = 'attachment; filename="seattle/data/hospitals.csv"'
#             return response
#         elif file_format == 'JSON':
#             response = HttpResponse(dataset.json, content_type='application/json')
#             response['Content-Disposition'] = 'attachment; filename="seattle/data/hospitals.json"'
#             return response
#         elif file_format == 'XLS (Excel)':
#             response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
#             response['Content-Disposition'] = 'attachment; filename="seattle/data/hospitals.xls"'
#             return response

#     return render(request, 'seattle/export_hospitals_data.html')


# def import_schools_data(request):
#     if request.method == 'POST':
#         file_format = request.POST['file-format']
#         school_resource = SchoolResource()
#         dataset = Dataset()
#         new_schools = request.FILES['importData']

#         if file_format == 'CSV':
#             imported_data = dataset.load(new_schools.read().decode('utf-8'),format='csv')
#             result = school_resource.import_data(dataset, dry_run=True)

#         elif file_format == 'JSON':
#             imported_data = dataset.load(new_schools.read().decode('utf-8'),format='json')
#             # Testing data import
#             result = school_resource.import_data(dataset, dry_run=True)

#         if not result.has_errors():
#             # Import now
#             school_resource.import_data(dataset, dry_run=False)
#             messages.success(request, 'Data Imported Successfully.')

#     return render(request, 'seattle/import_schools_data.html')


# def export_schools_data(request):
#     if request.method == 'POST':
#         # Get selected option from form
#         file_format = request.POST['file-format']
#         school_resource = SchoolResource()
#         dataset = school_resource.export()

#         if file_format == 'CSV':
#             response = HttpResponse(dataset.csv, content_type='text/csv')
#             response['Content-Disposition'] = 'attachment; filename="seattle/data/schools.csv"'
#             return response
#         elif file_format == 'JSON':
#             response = HttpResponse(dataset.json, content_type='application/json')
#             response['Content-Disposition'] = 'attachment; filename="seattle/data/schools.json"'
#             return response
#         elif file_format == 'XLS (Excel)':
#             response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
#             response['Content-Disposition'] = 'attachment; filename="seattle/data/schools.xls"'
#             return response

#     return render(request, 'seattle/export_schools_data.html')


# def import_libraries_data(request):
#     if request.method == 'POST':
#         file_format = request.POST['file-format']
#         library_resource = LibraryResource()
#         dataset = Dataset()
#         new_libraries = request.FILES['importData']

#         if file_format == 'CSV':
#             imported_data = dataset.load(new_libraries.read().decode('utf-8'),format='csv')
#             result = library_resource.import_data(dataset, dry_run=True)

#         elif file_format == 'JSON':
#             imported_data = dataset.load(new_libraries.read().decode('utf-8'),format='json')
#             # Testing data import
#             result = library_resource.import_data(dataset, dry_run=True)


#         if not result.has_errors():
#             # Import now
#             library_resource.import_data(dataset, dry_run=False)
#             messages.success(request, 'Data Imported Successfully.')

#     return render(request, 'seattle/import_library_data.html')


# def export_libraries_data(request):
#     if request.method == 'POST':
#         # Get selected option from form
#         file_format = request.POST['file-format']
#         library_resource = LibraryResource()
#         dataset = library_resource.export()

#         if file_format == 'CSV':
#             response = HttpResponse(dataset.csv, content_type='text/csv')
#             response['Content-Disposition'] = 'attachment; filename="seattle/data/libraries.csv"'
#             return response
#         elif file_format == 'JSON':
#             response = HttpResponse(dataset.json, content_type='application/json')
#             response['Content-Disposition'] = 'attachment; filename="seattle/data/libraries.json"'
#             return response
#         elif file_format == 'XLS (Excel)':
#             response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
#             response['Content-Disposition'] = 'attachment; filename="seattle/data/libraries.xls"'
#             return response

#     return render(request, 'seattle/export_libraries_data.html')

from django.urls import path

from . import views

app_name = 'seattle'


urlpatterns = [
    path('', views.HomePage.as_view(), name='seattle-homepage'),
    path('map/', views.map_view, name='seattle-map'),
    path('map2/', views.MapView.as_view(), name='seattle-map-2'),

    # Importing Data
    path('import-hospitals/', views.ImportHospitalsView.as_view(), name='import-hospitals'),
    path('import-schools/', views.ImportSchoolsView.as_view(), name='import-schools'),
    path('import-libraries/', views.ImportLibrariesView.as_view(), name='import-libraries'),

    # Exporting Data
    path('export-hospitals/', views.HospitalsExportView.as_view(), name='export-hospitals'),
    path('export-schools/', views.SchoolsExportView.as_view(), name='export-schools'),
    path('export-libraries/', views.LibrariesExportView.as_view(), name='export-libraries'),

]

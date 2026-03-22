from django.urls import path

from . import views

app_name = 'seattle'


urlpatterns = [
    path('', views.HomePage.as_view(), name='seattle-homepage'),
    path('map/', views.index, name='seattle-map'),

    # Importing Data
    path('import-hospitals/', views.import_hospitals_data, name='import-hospitals'),
    path('import-schools/', views.import_schools_data, name='import-schools'),
    path('import-libraries/', views.import_libraries_data, name='import-libraries'),

    # Exporting Data
    path('export-hospitals/', views.export_hospitals_data, name='export-hospitals'),
    path('export-schools/', views.export_schools_data, name='export-schools'),
    path('export-libraries/', views.export_libraries_data, name='export-libraries'),

]

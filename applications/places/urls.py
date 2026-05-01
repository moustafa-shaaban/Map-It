from django.urls import path

from . import views

app_name = 'places'

urlpatterns = [
    path("", views.map_view, name='places-list'),
    path('api/places/', views.places_list, name='places-api'),
    path('api/places/<int:pk>', views.PlaceDetailView.as_view(), name='place-detail-view'),
]
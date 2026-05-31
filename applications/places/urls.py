from django.urls import path

from . import views

app_name = 'places'

urlpatterns = [
    path("", views.map_view, name='places-map'),
    path('api/places/', views.places_list, name='places-api'),
    path('places/', views.PlacesListView.as_view(), name='place-list-view'),
    path('<int:pk>/', views.PlaceDetailView.as_view(), name='place-detail-view'),
    path('create/', views.create_place, name='place-create-view'),
    path('<int:pk>/update/', views.update_place, name='place-update-view'),
    # path('api/places/create', views.PlaceCreateView.as_view(), name='place-create-view'),
    # path('api/places/<int:pk>/update', views.PlaceUpdateView.as_view(), name='place-update-view'),
]
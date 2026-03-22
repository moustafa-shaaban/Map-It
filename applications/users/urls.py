from django.urls import path

from . import views
urlpatterns = [
    path('<str:username>/', views.ProfileDetailView.as_view(), name='profile-details'),
    path('~redirect/', views.UserRedirectView.as_view(), name='redirect'),
    path('update', views.update_profile, name='update-profile')
]
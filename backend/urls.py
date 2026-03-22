from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static

from graphene_django.views import GraphQLView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('silk/', include('silk.urls', namespace='silk')),
    path(
        "",
        TemplateView.as_view(template_name="index.html"),
        name="home",
    ),
    path('accounts/', include('allauth.urls')),
    path('users/', include('applications.users.urls')),
    path('seattle/', include('applications.seattle.urls')),
    
    # path(
    #     "settings/",
    #     TemplateView.as_view(template_name="settings.html"),
    #     name="settings",
    # ),
    path(
        "about/",
        TemplateView.as_view(template_name="about.html"),
        name="about",
    ),

    path("graphql/", GraphQLView.as_view(graphiql=True)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # Redoc UI:
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path("__reload__/", include("django_browser_reload.urls")),


] + debug_toolbar_urls() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

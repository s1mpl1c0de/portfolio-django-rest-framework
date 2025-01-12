"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from apps.accounts.views import UserViewSet
from apps.jobs.views import ExperienceViewSet

router = routers.DefaultRouter()
router.register(r'experiences', ExperienceViewSet, 'experience')
router.register(r'users', UserViewSet, 'user')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/', include(router.urls)),
]

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += (
            static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) +
            debug_toolbar_urls()
    )

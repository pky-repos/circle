"""circle URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView
from rest_framework import permissions
from rest_framework.routers import DefaultRouter, SimpleRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from chat.views import ChatGroupViewSet, MessageViewSet
from users.views import UserViewSet, ProfileViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="Circle API",
        default_version='v1',
        description="Create chat groups and more",
        terms_of_service="coming soon",
        contact=openapi.Contact(email="panky.asg@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ],
)

router = DefaultRouter()

router.register(r'users', UserViewSet, "users")
router.register(r'users-read', UserViewSet, "users")
router.register(r'profiles', ProfileViewSet, "profiles")
router.register(r'chat-groups', ChatGroupViewSet, "chat-groups")
router.register(r'messages', MessageViewSet, "messages")

# import pprint
#
# pprint.pprint(router.get_urls())

urlpatterns = [
    path('', RedirectView.as_view(url="swagger/")),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
            name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('auth/', include('dj_rest_auth.urls')),
    re_path(r"^api/", include((router.urls, 'api'))),
]

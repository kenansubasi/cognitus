"""cognitus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import routers, permissions

from django.contrib import admin
from django.urls import include, path

from data.views import DataViewSetV1
from users.views import UserLoginViewV1, UserLogoutViewV1, UserViewSetV1


# Api
router_v1 = routers.DefaultRouter()
router_v1.register("data", DataViewSetV1, basename="data")
router_v1.register("users", UserViewSetV1, basename="users")

# Docs
api_info = openapi.Info(
    title="Cognitus API",
    default_version="v1"
)
schema_view = get_schema_view(
   api_info,
   public=True,
   permission_classes=(permissions.IsAdminUser,),
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(router_v1.urls)),
    path("api/v1/login/", UserLoginViewV1.as_view(), name="login"),
    path("api/v1/logout/", UserLogoutViewV1.as_view(), name="logout"),
    path("docs/", schema_view.with_ui("redoc", cache_timeout=0), name="docs"),
]

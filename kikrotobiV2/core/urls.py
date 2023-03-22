from django.contrib import admin
from django.urls import path, include
from .drf_yasg import urlpatterns as drf_pat


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('order.urls'))
]
urlpatterns += drf_pat

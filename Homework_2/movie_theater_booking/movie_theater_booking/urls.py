from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("bookings.urls")),
    path("api-auth/", include("rest_framework.urls")),  # login page for the browsable API
    path("", include("bookings.page_urls")),             # the Bootstrap web pages
]
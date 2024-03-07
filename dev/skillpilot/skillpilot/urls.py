from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')), # connect the urls.py in core to this django project
    path('dashboard/', include('dashboard.urls')),  # Include dashboard app URLs
]

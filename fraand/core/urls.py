"""fraand URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from social_network.views import (
    index,
    search,
    AddItemView,
    GetItemView,
    EditItemView,
    DeleteItemView,
)

# fmt: off
# (Skip Black formatting in this section)


urlpatterns = [
    # NOTE: change the URL for Admin, for added security.
    # See #2 here: https://opensource.com/article/18/1/10-tips-making-django-admin-more-secure
    path("admin/", admin.site.urls),
    path('', index, name='homepage'),
    path('search/', search, name='search'),
    path('add_item/', AddItemView.as_view(), name='add_item'),
    path('get_item/<str:pk>', GetItemView.as_view(), name='get_item'),
    path('edit_item/<str:pk>', EditItemView.as_view(), name='edit_item'),
    path('delete_item/<str:pk>', DeleteItemView.as_view(), name='delete_item'),
    path('accounts/', include('django.contrib.auth.urls')),
]
# fmt: on

if settings.DEBUG:
    # Serve media files in development server.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

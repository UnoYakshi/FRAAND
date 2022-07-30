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

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from social_network.views import (
    index, search, profile,
    AddItemView, DeleteItemView, EditItemView, GetItemView,
    rent, GetRentView, EditRentView, DeleteRentView, confirm_rent, give_away, change_due_item
)

# fmt: off
# (Skip Black formatting in this section)

# fmt: on
urlpatterns = [
    # NOTE: change the URL for Admin, for added security.
    # See #2 here: https://opensource.com/article/18/1/10-tips-making-django-admin-more-secure

    path('admin/', admin.site.urls),
    path('', index, name='homepage'),
    path('search/', search, name='search'),

    path('profile/', profile, name='profile'),
    # path('password_change/',
    #      PasswordChangeView.as_view(template_name="fraand/templates/registration/password_change.html"),
    #      name='password_change'),
    # path('password_change/done/',
    #      PasswordChangeDoneView.as_view(template_name="fraand/templates/registration/password_change_done.html"),
    #      name='password_change_done'),
    # path('pwd/', change_password, name='profile'),

    path('add_item/', AddItemView.as_view(), name='add_item'),
    path('get_item/<str:pk>', GetItemView.as_view(), name='get_item'),
    path('edit_item/<str:pk>', EditItemView.as_view(), name='edit_item'),
    path('delete_item/<str:pk>', DeleteItemView.as_view(), name='delete_item'),

    path('add_rent/<str:item_id>', rent, name='add_rent'),
    path('get_rent/<str:pk>', GetRentView.as_view(), name='get_rent'),
    path('edit_rent/<str:pk>', EditRentView.as_view(), name='edit_rent'),
    path('delete_rent/<str:pk>', DeleteRentView.as_view(), name='delete_rent'),
    path('confirm_rent/<str:pk>', confirm_rent, name='confirm_rent'),
    path('refuse_rent/<str:pk>', rent, name='refuse_rent'),
    path('give_away/<str:from_uid>/<str:to_uid>/<str:item_uid>', rent, name='give_away'),
    path('change_due_date/<str:pk>', rent, name='change_due_time'),

    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    # Serve media files in development server.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include
from userapp import views as user_views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    # language switch endpoint
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('', user_views.index, name='index'),
    path('instructor/', include('instructorapp.urls')),
    path('user/', include('userapp.urls')),
    path('adminpanel/', include('adminapp.urls')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
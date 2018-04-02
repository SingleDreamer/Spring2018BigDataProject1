
from django.contrib import admin
from django.conf.urls import url#include, url#, patterns#path

from adkbase import views
#urlpatterns = [
#    path('adkbase/', include('adkbase.urls')),
#    path('admin/', admin.site.urls),
#]

urlpatterns = [
    url(r'^adkbase/', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
]

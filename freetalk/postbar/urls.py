from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^log/', views.index, name = 'index'),
    url(r'^register/', views.register, name = 'register'),
    url(r'^findback/', views.findback, name = 'findback'),
    url(r'^$', views.account, name = 'account'),
]

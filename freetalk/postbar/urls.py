from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^log/', views.index, name = 'index'),
    url(r'^register/', views.register, name = 'register')
]
from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^register/', views.register, name = 'register'),
    url(r'^findback/', views.findback, name = 'findback'),
    url(r'^account/', views.account, name = 'account'),
    url(r'^admin/', views.admin, name = 'admin'),
    url(r'^homepage/', views.homepage, name = 'homepage'),
    url(r'^post/(\d+)/$', views.showpost, name='post'),
]

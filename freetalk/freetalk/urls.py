from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
	url(r'^postbar/', include('postbar.urls')),
    url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


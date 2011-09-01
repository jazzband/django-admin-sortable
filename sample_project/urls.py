from django.conf import settings
from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)

if settings.SERVE_STATIC_MEDIA:
    urlpatterns += patterns('',
        (r'^' + settings.MEDIA_URL.lstrip('/'), include('appmedia.urls')),
    ) + urlpatterns

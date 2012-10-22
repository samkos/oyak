from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'oyak.views.home', name='home'),
    # url(r'^oyak/', include('oyak.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:

    url(r'^admin/', include(admin.site.urls)),
#    url(r'^(?P<url>.*).(?P<ext>png|gif|jpg)$', 'oyak.views.image'),
#    url(r'^(?P<url>.*)$', 'oyak.views.index'),
        url(r'^(?P<url>.*)$', 'oyak.views.index'),
                       )

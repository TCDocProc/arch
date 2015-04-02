from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/add_pathway/'), name='index'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^add_pathway/$', 'core.views.add_pathway', name='add_pathway'),
    url(r'^integrate/$', 'core.views.integrate', name='integrate'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^processes(?:(\.(?P<extension>(json)))|(?:(/\d+)+/?|/?$))', 'processes.views.index', name='process_view'),
    url(r'^openemr/signup', 'openemr.views.sign_up' )
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

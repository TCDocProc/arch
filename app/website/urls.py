from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/add_pathway/'), name='index'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^add_pathway/$', 'members.views.add_pathway', name='add_pathway'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^processes/user/(?P<user_id>\d+)(?:(\.(?P<extension>(json)))|(?:(/\d+)+/?|/?$))', 'processes.views.index',name='process_view'),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

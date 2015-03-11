from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^$', 'members.views.index', name='index'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^auth/', 'members.views.authenticated_page', name='auth'),
    url(r'^add_pathway/$', 'members.views.add_pathway', name='add_pathway'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^processes/user/(?P<user_id>\d+)\.(?P<extension>(json)|(html))', 'processes.views.index', name='process_view'),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

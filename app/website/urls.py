from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'members.views.index', name='index'),

    url(r'^accounts/', include('allauth.urls')),

    url(r'^auth/', 'members.views.authenticated_page', name='auth'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^processes/user/(?P<user_id>\d+)\.(?P<extension>(json)|(html))', 'processes.views.index'),
)

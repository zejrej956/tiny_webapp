from django.conf.urls import include, url
from django.contrib import admin

from .views import (
	home,
	download
	)

urlpatterns = [
	url(r'^$', home, name="home"),
	url(r'^download/(?P<slug>[\w-]+)/$', download, name='download')
]
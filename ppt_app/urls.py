from django.conf.urls import include, url
from django.contrib import admin

from .views import (
	converttexttoppt_func,
	import_file,
	create_outline,
	download_func,
	slide_templates_func
	)

urlpatterns = [
	url(r"^$", converttexttoppt_func, name="converttexttoppt"),
	url(r'^download/(?P<slug>[\w-]+)/$', download_func, name='download'),
	url(r'^import-file/$', import_file, name='import_file'),
	url(r'^create-outline/$', create_outline, name='create_outline'),
	url(r'^slide-templates/$', slide_templates_func, name='slide_templates'),
]


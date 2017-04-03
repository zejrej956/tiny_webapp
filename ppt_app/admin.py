from django.contrib import admin

# Register your models here.

from .models import ReportOutlineFile, ReportOutlineByEditor, Slide_Template
class SlideTemplate_Admin(admin.ModelAdmin):
	list_display = ['id', 'template_name', 'template',  'slug']

	class Meta:
		model = Slide_Template
class ReportOutlineAdmin(admin.ModelAdmin):
	list_display = ['filename', 'report_outline', 'template', 'slug']

	class Meta:
		model = ReportOutlineFile

class ReportOutline_byEditor_Admin(admin.ModelAdmin):
	list_display = ['filename', 'outline', 'template']

	class Meta:
		model = ReportOutlineByEditor

admin.site.register(Slide_Template, SlideTemplate_Admin)
admin.site.register(ReportOutlineFile, ReportOutlineAdmin)
admin.site.register(ReportOutlineByEditor, ReportOutline_byEditor_Admin)

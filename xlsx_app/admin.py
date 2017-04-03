from django.contrib import admin

# Register your models here.
from .models import Workbook
class WorkbookAdmin(admin.ModelAdmin):
	list_display = ['workbook', 'slug']

	class Meta:
		model = Workbook


admin.site.register(Workbook, WorkbookAdmin)

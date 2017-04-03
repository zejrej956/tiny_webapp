from django import forms

from .models import Workbook

class WorkbookForm(forms.ModelForm):
	class Meta:
		model = Workbook
		fields = [	
			"workbook"
		]

from django import forms

from .models import ReportOutlineFile, ReportOutlineByEditor, Slide_Template

class ReportOutlineForm(forms.ModelForm):
	class Meta:
		model = ReportOutlineFile	

		fields = [	
			"filename", "report_outline",
		]
		
class ReportOutlineForm_byEditor(forms.ModelForm):
	class Meta:
		model = ReportOutlineByEditor	
		fields = [	
			"filename", "outline",
		]

	def __init__(self, *args, **kwargs):
		super(ReportOutlineForm_byEditor, self).__init__(*args, **kwargs)
		self.fields['outline'].widget.attrs={'id': 'outline', 'class':'form-control', 'class': 'animated'}

class TemplateOptionsForm(forms.Form):
	# radio button for template options
	template_choices = [("user_template", "Upload Template"), ("preloaded_template", "Use preloaded templates")]
	template_option = forms.ChoiceField(choices=template_choices, widget=forms.RadioSelect())
			
class PreloadedSlideTemplateForm(forms.Form):
	instance_preloaded_template = Slide_Template.objects.all()
	slide_templates_choices = Slide_Template.objects.values_list('id', 'slug', flat=False)
	Preloaded_Templates = forms.ChoiceField(choices=slide_templates_choices, widget=forms.RadioSelect())

class UserSlideTemplateForm(forms.ModelForm):
	class Meta:
		model = Slide_Template	
		fields = [	
			"template_name", "template",
		]



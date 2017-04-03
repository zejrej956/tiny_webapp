from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ReportOutlineForm, ReportOutlineForm_byEditor, UserSlideTemplateForm, TemplateOptionsForm, PreloadedSlideTemplateForm
from .models import ReportOutlineFile, ReportOutlineByEditor, Slide_Template
# from .models import ReportOutline
from django.http import HttpResponseRedirect, Http404
# import pandas as pd
# from .worksheet_csv import convert_worksheets
from .Categorize_content import Categorize_content
import os

# Create your views here.
def converttexttoppt_func(request):
	if not request.user.is_authenticated:
		messages.success(request, "I'm sorry, but you must login first.")
		return redirect("login")
	else:
		form_ImportFile = ReportOutlineForm(request.POST or None, request.FILES or None)
		form_TextEditor = ReportOutlineForm_byEditor(request.POST or None, request.FILES or None)

		if form_ImportFile.is_valid():
			instance = form_ImportFile.save(commit=False)
	
			instance.save()
			return HttpResponseRedirect(instance.get_absolute_url())

		context = {
			"form_ImportFile": form_ImportFile,
			"form_TextEditor": form_TextEditor,
		}
		return render(request, "texttoppt_importfile.html", context)

def import_file(request):
	if not request.user.is_authenticated:
		messages.success(request, "I'm sorry, but you must login first.")
		return redirect("login")
	else:
		form_ImportFile = ReportOutlineForm(request.POST or None, request.FILES or None)
		form_TemplateOptions = TemplateOptionsForm(request.POST or None, request.FILES or None, auto_id=True)
		
		# form use if user wants to upload own templates
		form_UserSlideTemplate = UserSlideTemplateForm(request.POST or None, request.FILES or None)

		# form use if user wants to use preloaded templates
		form_PreloadedSlideTemplate = PreloadedSlideTemplateForm(request.POST or None, request.FILES or None, auto_id=True)
		print "been here!"
		if form_TemplateOptions.is_valid():
			if form_TemplateOptions['template_option'].value() == "user_template":
				if form_UserSlideTemplate.is_valid():
					instance_slide_template = form_UserSlideTemplate.save(commit=False)
					instance_slide_template.save()
					
			if form_TemplateOptions['template_option'].value() == "preloaded_template":
				if form_PreloadedSlideTemplate.is_valid():
					template_id = int(form_PreloadedSlideTemplate['Preloaded_Templates'].value())
					instance_slide_template = Slide_Template.objects.get(id=template_id)

		if form_ImportFile.is_valid():
			instance_outline = form_ImportFile.save(commit=False)
			instance_outline.template = instance_slide_template
			instance_outline.save()

			return HttpResponseRedirect(instance_outline.get_absolute_url())

		context = {
			"form_ImportFile": form_ImportFile,
			"form_UserSlideTemplate": form_UserSlideTemplate,
			"form_TemplateOptions": form_TemplateOptions,
			"form_PreloadedSlideTemplate": form_PreloadedSlideTemplate
			
		}
		return render(request, "texttoppt_importfile.html", context)

def create_outline(request):
	if not request.user.is_authenticated:
		messages.success(request, "I'm sorry, but you must login first.")
		return redirect("login")
	else:
		
		form_TextEditor = ReportOutlineForm_byEditor(request.POST or None, request.FILES or None)
		form_TemplateOptions = TemplateOptionsForm(request.POST or None, request.FILES or None, auto_id=True)

		# form use if user wants to upload own templates
		form_UserSlideTemplate = UserSlideTemplateForm(request.POST or None, request.FILES or None)

		# form use if user wants to use preloaded templates
		form_PreloadedSlideTemplate = PreloadedSlideTemplateForm(request.POST or None, request.FILES or None, auto_id=True)
		
		if form_TemplateOptions.is_valid():
			if form_TemplateOptions['template_option'].value() == "user_template":
				if form_UserSlideTemplate.is_valid():
					instance_slide_template = form_UserSlideTemplate.save(commit=False)
					instance_slide_template.save()
			if form_TemplateOptions['template_option'].value() == "preloaded_template":
				if form_PreloadedSlideTemplate.is_valid():
					template_id = int(form_PreloadedSlideTemplate['Preloaded_Templates'].value())
					instance_slide_template = Slide_Template.objects.get(id=template_id)

		if form_TextEditor.is_valid():
			instance_outline = form_TextEditor.save(commit=False)
			instance_outline.template = instance_slide_template
			instance_outline.save()

			return HttpResponseRedirect(instance_outline.get_absolute_url())

		context = {
			"form_TextEditor": form_TextEditor,
			"form_UserSlideTemplate": form_UserSlideTemplate,
			"form_TemplateOptions": form_TemplateOptions,
			"form_PreloadedSlideTemplate": form_PreloadedSlideTemplate
		}
		return render(request, "texttoppt_texteditor.html", context)

def download_func(request, slug):
	if not request.user.is_authenticated:
		messages.success(request, "I'm sorry, but you must login first.")
		return redirect("login")
	else:
		try:
			instance = get_object_or_404(ReportOutlineFile, slug=slug)
			slide_template = instance.template.template
			content = instance.report_outline.read()
			instance_type = "file"
		except:
			instance = get_object_or_404(ReportOutlineByEditor, slug=slug)
			slide_template = instance.template.template
			content = instance.outline
			instance_type = "outline_by_editor"
		#convert the ReportOutlineFile to a presentation
		try:
			try:
				print "dawd"
				file_ = Categorize_content(content, instance.filename, slide_template)
				file_.convert_to_ppt()
				file_.save_ppt()
			except:
				if instance_type == "file":
					messages.warning(request, "File you imported might be invalid.")
					instance.delete()
					return redirect("txttoppt:import_file")
				if instance_type == "outline_by_editor":
					messages.warning(request, "An outline with a single line doesn't make sense.")
					instance.delete()
					return redirect("txttoppt:create_outline")

			file_name = str(instance.filename) + ".pptx"
			context = {
				"name": file_name
			}
			messages.success(request, 'FILE IS SUCCESSFULLY CONVERTED!')

			return render(request, "download_page_ppt.html", context)
			
		except:
			messages.error(request, 'INVALID FILE FORMAT!')
			instance.delete()
			if instance_type == "file":
					return redirect("txttoppt:import_file")
			if instance_type == "outline_by_editor":
				return redirect("txttoppt:create_outline")

def slide_templates_func(request):
	if not request.user.is_authenticated:
		messages.success(request, "I'm sorry, but you must login first.")
		return redirect("login")
	else:
		return render(request, "slide_templates.html", {})
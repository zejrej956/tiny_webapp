from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .forms import WorkbookForm
from .models import Workbook
from django.http import HttpResponseRedirect
import pandas as pd
from .worksheet_csv import convert_worksheets
import inspect, os, csv

# Create your views here.
def home(request):

	if not request.user.is_authenticated:
		messages.success(request, "I'm sorry, but you must login first.")
		return redirect("login")
	else:	
		form = WorkbookForm(request.POST or None, request.FILES or None)

		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
		
			return HttpResponseRedirect(instance.get_absolute_url())
		context = {
			"form": form
		}
		return render(request, "xlsxtocsv.html", context)


def download(request, slug):
	if not request.user.is_authenticated:
		messages.success(request, "I'm sorry, but you must login first.")
		return redirect("login")
	else:	
		instance = get_object_or_404(Workbook, slug=slug)
		# print instance.workbook
		# print instance.workbook.name
		if os.path.exists('static/media/merged.csv'):
			with open('static/media/merged.csv', 'w'):
				pass
		else:
			with open('static/media/merged.csv', 'w') as fp:
				a = csv.writer(fp)
				data = []
				a.writerows(data)

		try:#convert the workbook to a single csv file
			convert_worksheets(instance.workbook)
			# instance.delete()
			context = {
				"name": 'merged.csv'
			}
			messages.success(request, 'FILE IS SUCCESSFULLY CONVERTED!')
			return render(request, "download_page_xlsx.html", context)
		except:
			messages.error(request, 'INVALID FILE FORMAT!')
			# instance.delete()
			return redirect("main_home:home")

	
import pandas as pd
import numpy as np 
import csv
from django.conf import settings

"""
Problem 1:
This function converts each worksheet in a workbook into a csv file
"""

def convert_worksheets(file_name):
	xlsx = pd.ExcelFile(file_name)

	# retrieve the names of each worksheet and store into a list
	names = xlsx.sheet_names
	for worksheet in range(0, len(names)):
		content = xlsx.parse(worksheet)
		csv_name = str(names[worksheet]) + ".csv"

		# merge_all_csv(content_list)
		merge_all_csv(content)

"""Problem 2: Merge all the CSVs"""
def merge_all_csv(content):
	# save contents of excel to csv excluding the added first column
	# by setting index to False


	content.to_csv("static/media/merged.csv", mode='a', index=False)
	

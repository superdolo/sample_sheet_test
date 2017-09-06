# -*- coding: utf-8 -*-
"""
Open Sample_Sheet_Test.xlsx, using Pandas preferably

1. Write a class for the parsing of the sheet. Assume the sheet is written by hand, and could contain errors. Raise errors if the sheet does not look like the one you are given, or, in other words, force the general structure of the sheet as given. Please be flexible and handle if there are spaces around names or capitalizations anywhere.

2. Get the Experiment Name, save it to the class object. Make the assumption the formatting will stay the same, with a Date followed by "_"

3. Check that the date on the experiment matches the Date column, throw error if it does not. Can assume the Experiment Date is before the first "_"

4. Parse the table starting on line 21 into a DataFrame (Can assume it starts on line 21, or dynamically find the headers)

5. Most of the rows in Sample_ID follow a similar pattern. Save the rows that do not follow this pattern into a different DataFrame, called “calibration_df” - Don't worry about being too fancy on this. Feel free to simply look for a string in the column

6. Check that the remaining rows follow the correct pattern of (YY)(3 Alpha Characters)(Number)_(Number)(G or T). 

7. Save any that do not follow the pattern into an error DataFrame, “non_conforming” everything else can go into "self.data"

8. Everything before the first “_” character in Sample_ID is the ID. Build a database with these IDs as the key (So 17RES970_2T and 17RES970_3T are both stored under 17RES970).

9. Print out the calibration_df, non_conforming, data, and the dictionary from Step 8

10. Be able to run the script by typing in the terminal “python sample_sheet_test.py” , zip the Sample_Sheet_Test.xlsx and python script into a folder (Or can do a private Github repo and grant access to @schwallie)

"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xlrd
import sys

file_name = 'Sample_Sheet_Test.xlsx'

class Sample:
	
	section_names = ['[Header]','[Reads]','[Settings]','[Data]'] #just a little descriptive data we will use later to parse datasets to each section
	
	def parse_sample(self,file):
		return pd.read_excel(file, sheetname=0, header=None,index_col = None, na_values=['NA'])
	
	def __init__(self,file_name):
		xlsx = self.parse_sample(file_name) #Here we parse the entire xlsx 
		
		def generate_dataset(section_name): #write a method to find the starting positions of each section of data section_names = ['[Header]','[Reads]','[Settings]','[Data]']
			row_id = int(xlsx.loc[xlsx[0] == section_name].index[0])
			other_sections = [name for name in self.section_names if name != section_name]
			print(other_sections)
			def find_next_row_id():
				try:
					return max([xlsx.loc[xlsx[0] == idx].index[0] for idx in other_sections if xlsx.loc[xlsx[0] == idx].index[0] > row_id])
				except:
					return None
			next_row_id = find_next_row_id()
			print (next_row_id)
			if section_name == '[Header]':
				raw_data = pd.DataFrame()
				pass
			elif section_name == '[Reads]':
				pass
			elif section_name == '[Settings]':
				pass
			elif section_name == '[Data]':
				raw_data = xlsx[row_id+2:next_row_id].values
				headers = xlsx[row_id+1:row_id+2].values[0]
				return pd.DataFrame(raw_data,columns=headers) #Here is where we create the dataframe for the test data
			else:
				print('You entered a header incorrrectly!')
		
		
		
		self.data = generate_dataset('[Data]')
		#self.data = generate_dataset('[Reads]')
		#self.data = generate_dataset('[Settings]')
		#self.data = generate_dataset('[Data]')
		
test_sample = Sample(file_name)

#print (test_sample.data)
#print (test_sample.data.head())



print(test_sample.data)



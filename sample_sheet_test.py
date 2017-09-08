# -*- coding: utf-8 -*-
"""
# Test should take ~1.5 hours
# No need to write unit tests, but make sure to do logical checks anywhere it makes sense and raise errors if something doesn't conform. Assume these are written by hand and things like "Sample_ID" could be "Sample_Id" -- Handle those yourself, but error out if "Sample_ID" is "Smaple_ID" for example

Open Sample_Sheet_Test.xlsx, using Pandas preferably

x1. Write a class for the parsing of the sheet. Assume the sheet is written by hand, and could contain errors. Raise errors if the sheet does not look like the one you are given, or, in other words, force the general structure of the sheet as given. Please be flexible and handle if there are spaces around names or capitalizations anywhere.

x2. Get the Experiment Name, save it to the class object. Make the assumption the formatting will stay the same, with a Date followed by "_"

x3. Check that the date on the experiment matches the Date column, throw error if it does not. Can assume the Experiment Date is before the first "_"

x4. Parse the table starting on line 21 into a DataFrame (Can assume it starts on line 21, or dynamically find the headers)

x5. Most of the rows in Sample_ID follow a similar pattern. Save the rows that do not follow this pattern into a different DataFrame, called “calibration_df” - Don't worry about being too fancy on this. Feel free to simply look for a string in the column.

x6. Of the rest of the rows that follow a general pattern, there are still some small errors. Check that the remaining follow the correct pattern of (YY)(3 Alpha Characters)(Number)_(Number)(G or T).

x7. Save any that do not follow the pattern into an error DataFrame, “non_conforming” everything else can go into "self.data" -- This leaves you with a calibration_df, which has radically different "Sample_ID" entries, a non_conforming, which has the same general pattern but some small changes, and a "self.data" DataFrame that has (YY)(3 Alpha Characters)(Number)_(Number)(G or T) rows only.

x8. Everything before the first “_” character in Sample_ID is the ID. Build a dictionary with these IDs as the key (So 17RES970_2T and 17RES970_3T are both stored under 17RES970, saved_dictionary["17RES970"] = ["17RES970_2T", "17RES970_3T"]

x9. Print out the calibration_df, non_conforming, data, and the dictionary from Step 8

10. Be able to run the script by typing in the terminal “python sample_sheet_test.py” , zip the Sample_Sheet_Test.xlsx and python script into a folder (Or can do a private Github repo and grant access to @schwallie)

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xlrd
import sys
import datetime
import re

file_name = 'Sample_Sheet_Test.xlsx'

class Sample:

	section_names = ['[header]','[reads]','[settings]','[data]'] #just a little descriptive data we will use later to parse datasets to each section
	header_headers = ['iemfileversion','investigator name','experiment name','date','workflow','application','assay','description','chemistry','nan'] #expected headers categories for validation/structure enforcement
	data_headers  = ['lane','sample_id','sample_name','sample_plate','sample_well','i7_index_id','index','sample_project','description'] #expected headers categories for validation/structure enforcement
	settings_headers = ['adapter','adapterread2','nan']#expected headers categories for validation/structure enforcement
	valid_headers = {'header':header_headers,'data':data_headers,'settings': settings_headers} #dictionary of expected headers categories for validation/structure enforcement
	
	def parse_sample(self,file): #in retrospect i would parse as series for greater flexibility in creating dataframes later but this still works 
		dirty_df = pd.read_excel(file, sheetname=0, header=None,index_col = None, na_values=['NA']) #If header rows are assumed to be consistent, this process can be made much simpler with header=[0, 1, 2, 3, etc]
		clean_df = dirty_df.apply(lambda x: x.astype(str).str.strip().str.lower()) #1. strip whitespace and convert to lower to decrease the change of errors due to inconsistencies in data entry
		return clean_df
	
	def __init__(self,file_name):
		xlsx = self.parse_sample(file_name) #Here we parse the entire xlsx
		def generate_dataset(section_name): #generates a dataframe for each section in test xlsx
			try:
				row_id = int(xlsx.loc[xlsx[0] == section_name].index[0]) #find the starting positions of each section of data section_names = ['[Header]','[Reads]','[Settings]','[Data]']
			except: 
				raise ValueError(section_name + ' section was not found in sample!')
			other_sections = [name for name in self.section_names if name != section_name]
			def find_next_row_id(): #allows dataframes to adjust to data in different order by parsing dataframe to next section header instead of fixed by row# / df.index
				try:
					return min([xlsx.loc[xlsx[0] == idx].index[0] for idx in other_sections if xlsx.loc[xlsx[0] == idx].index[0] > row_id])
				except:
					return None
			next_row_id = find_next_row_id()
			if section_name == '[header]':
				raw_data = xlsx[row_id+1:next_row_id].values.T
				headers = raw_data[0].tolist()
				return pd.DataFrame(raw_data[1:2],columns=headers)
			elif section_name == '[reads]':
				raw_data = xlsx[row_id+1:next_row_id].values.T
				headers = xlsx[row_id+1:row_id+2].values[0]
				return xlsx[row_id+1:next_row_id][0]
			elif section_name == '[settings]':
				raw_data = xlsx[row_id+1:next_row_id].values.T
				headers = raw_data[0].tolist()
				return pd.DataFrame(raw_data[1:2],columns=headers)
			elif section_name == '[data]':
				raw_data = xlsx[row_id+2:next_row_id].values
				headers = xlsx[row_id+1:row_id+2].values[0]
				return pd.DataFrame(raw_data,columns=headers) #Here is where we create the dataframe for the test data
			else:
				pass

		self.header = generate_dataset('[header]')
		self.reads = generate_dataset('[reads]')
		self.settings = generate_dataset('[settings]')
		self.df = generate_dataset('[data]')
		
		def validate_structure(): #since my parsing is flexible to take the sections out of order and with extra lines I am validating by matching expected headers 
			dataframes = [[self.header,'header'],[self.settings,'settings'],[self.df,'data']]
			missing_headers = []
			invalid_headers = []
			for each in dataframes:
				for hdr in list(each[0].columns.values):
					if hdr not in self.valid_headers[each[1]]:
						invalid_headers.append(hdr)
				for hdr in self.valid_headers[each[1]]:
					if hdr not in list(each[0].columns.values):
						missing_headers.append(hdr)
			if missing_headers != [] and invalid_headers == []:
				raise ValueError('! Test is invalid ! The following headers were missing from the test: '+ ' '.join(missing_headers))
			elif missing_headers == [] and invalid_headers != []:
				raise ValueError('! Test is invalid ! The following invalid headers were found in the test: '+ ' '.join(invalid_headers))
			elif missing_headers != [] and invalid_headers != []:
				raise ValueError('! Test is invalid ! The following headers were missing from the test: '+ ' '.join(missing_headers) + ' and ' + 'The following invalid headers were found in the test: '+ ' '.join(invalid_headers))
			else:
				print('File Passed Validation Checks')
				pass
		
		validate_structure() #runs the structure validation to ensure there are no bad data 
		self.experiment_name = self.header['experiment name'].values[0]
		self.experiment_date = self.header['date'].values[0]

		#print self.header
		#print self.experiment_name
		#print self.experiment_date

		re = r'(?<=\A)\d{2}[a-z]{3}\d+_\d+[g|t]\b'



		self.calibration_df = self.df[self.df.sample_id.str.contains('res') == False]
		self.non_conforming = self.df[self.df.sample_id.str.contains('res') == True]
		self.non_conforming = self.non_conforming[self.non_conforming.sample_id.str.contains(re)==False]
		self.data = self.df[self.df.sample_id.str.contains(re)]
		
		self.sample_ids = {}
		for id in self.df['sample_id'].values:
			try:
				main_id = id[:str(id).index('_')]
			except:
				main_id = id
			try:
				self.sample_ids[main_id].append(id)
			except:
				self.sample_ids[main_id] = [id]
	
	def validate_dates(self): # method to check if the date matches the experiment_name
		if datetime.datetime.strptime(self.experiment_name[:8],'%Y%m%d') == datetime.datetime.strptime(self.experiment_date,'%Y-%m-%d %H:%M:%S'):
			print('Experiment Date: '+str(self.experiment_date)+' matches Experiment Name: '+ self.experiment_name)
			return True
		else:
			raise ValueError('! Experiment Date: '+str(self.experiment_date)+' DOES NOT MATCH Experiment Name: '+ self.experiment_name)

test_sample = Sample(file_name) # call class to create new Sample object

print('Experiment Name: ' + test_sample.experiment_name)
test_sample.validate_dates()


print(test_sample.calibration_df)
print(test_sample.non_conforming)
print(test_sample.data)
print(test_sample.sample_ids)

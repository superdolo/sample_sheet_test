# sample_sheet_test
Tempus Python Developer Applicant Test - Steve Dolatowski

Installation:
1. unpack sample_sheet_test.py and Sample_Sheet_Test.xlxs into folder

Required Packages: 
pandas numpy matplotlib xlrd

Run: 
from cmd line # python sample_sheet_test.py


Notes: 

The purpose of this projet was to demonstrate my ability with python and the pandas datascience package. 
Each of the requirements should be met without issue. 

I thoroughly enjoyed learning/using many of the features of the pandas package.
In retrospect I would do a couple things differently:
	1.	Execute the initial parse of the xlsx into series rather than directly into dataframe. 
		Parsing everything into a dataframe to start cauese the rest of sorting to be a little tricky. 
		I could have read the file multiple times and parsed different dataframes each time but I wanted to limit reading the file to once.
	2.	Revisit my method for stripping and formating the data in the initial dataframe. 
		The way it is currently done converts all fields to str type which works but could be a problem with a more diverse dataset
		
Thank You:

Thanks to everyone at Tempus for taking the time and giving me the opertunity to show you how I can be an excelent member of your team.
I had a great time with the challenge and am happy to add Pandas and Numpy to my toolbox for future projects.
		
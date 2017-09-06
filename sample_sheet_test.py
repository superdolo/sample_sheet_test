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
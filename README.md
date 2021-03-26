# Data-Frame
Implementation of data frames in python

This file was a challenge to see if I could implement dataframes from scratch in Python.
The script uses no outside libraries and contains a single class, data_frame. 

This class can read csv files to create dataframes, or they can be created manually from lists of rows of data. 
I have included some data from W3 schools SQL course, as well as the iris dataset. Both of these can be used to test the funcitonality of the class. 

In this class, I have implemented some basic dataframe functions such as:

-Reading a csv file into a dataframe 
-Getting and setting data
-Filtering dataframes based on a column condition
-Inner joins between 1 dataframes with 1 column in common
-A group by and aggregate function. Choose a column to group by, and choose another column to aggregate. Allows, count, min, max, average and sum functions

This class is certainly no replacement for Pandas, as it was created only as a personal challenge. It is not optimized for performance on larged datasets. 
Feel free to download and test it with your own data in csv format!

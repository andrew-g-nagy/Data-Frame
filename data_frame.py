# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 2021
@author: Andrew G. Nagy
"""
#Create a data frame and perform data frame operations. Import from a csv, or past a list of lists, with each list representing a data row. 
#Column names can also be specified, or will be created by default if none are passed. Supported operations are selecting and updating values,
#stacking/merging dataframes with like columns, or performing inner joins

class data_frame():
    
    def __init__(self,rows,col_names = []):
        
        self.rows = rows
        #The default for col_names is []. If user does not pass any column names (only data rows), then
        #below code will detect this. The data frame then be initialized with column names of 0,1,...n by default
        lengths =[]
        for i in self.rows:
            lengths.append(len(i))
        
        #check the length of each row passed. If 
        max_length = max(lengths)    
        for i,j in enumerate(lengths):
            if j < max_length:
                self.rows[i].append("NA")
                
        
        self.col_names = col_names if len(col_names) != 0 else list(map(str,list(range(max_length)))) 
    
    
    
    #Return the shape of the dataframe [rows, columns]
    def shape(self):
        return [len(self.rows), len(self.col_names)]
    
    
    
    #Return the specific value at x,y    
    def get(self, row, column):
        return self.rows[row][column]
    
    
    
    #Get the specified row, returns it as a list
    def get_row(self,row):
            
        return self.rows[row]
    
    
    
    #Select a column. Returns it as a list. Use the column name as string by default. 
    #If name == False, use a numeric value
    def get_col(self, col, name = True):
        if name == True:
            v = self.col_names.index(col)
        else:
            v = col
            
        return_col = []
        for i in self.rows:
            return_col.append(i[v])
        
        return return_col
    
    
    
    #Change a cell value in the dataframe
    def set_value(self, row, column, val):
        self.rows[row][column] = val
    
    #Obtain column names
    def get_names(self):
        return self.col_names
    
    
    
    #Show entire dataframe
    def show(self):
        print("   " + str(self.col_names))
        for i,j in enumerate(self.rows):
            print(str(i) + ": " + str(j))
    
    
    
    #Show the first 'n' rows of the data frame        
    def preview(self,n=5):
        print("   " + str(self.col_names))
        for i,j in enumerate(self.rows[:n]):
            print(str(i) + ": " + str(j))
    
    
    
    #Given a csv file location, load it as a dataframe
    def read_csv(location, header = True):
        
        list_of_rows = []
        file = open(location,"r")
        
        #Open the file, remove any line breaks, and split into a list of values. Add this to the final list
        for i in file:
            list_of_rows.append(i.rstrip('\n').split(","))
        #If header is true, use the fist column as the column names. 
        if header == True:
            loaded = data_frame(list_of_rows[1:],list_of_rows[0])
        #Otherwise, use the default values of 0,1,2...n
        else:
            
            loaded = data_frame(list_of_rows)
            
        return loaded



    #Filter the dataframe by the value of a column. Specify the column and the value. Default comparison is 'equal to'.
    #For numeric values, can also select less than or greater than.
    
    def filter(self, col, col_val, comparison = 'equals'):
        if comparison not in ["equals","not","greater","less","less_or_eq","greater_or_eq"]:
            print("Must be one of the following comparisons: " + str( ["equals","not","greater","less","less_or_eq","greater_or_eq"]))
            return None
        
        #get the index of the column you are filtering for
        col_index = self.col_names.index(col)
        col_val =  str(col_val
                       )
        #if the specified value is not in the column and equals is the comparison, return none 
        if col_val not in self.get_col(col) and comparison == 'equals':
            print("Value: " + col_val + " is not in column " + col)
            return None
        
        new_rows = []
        
        if comparison == 'equals':
            
            for row in self.rows:
                if row[col_index] == col_val:
                    new_rows.append(row)
                    
            filtered = data_frame(new_rows,self.col_names).show()  
            return filtered        
        
        if comparison == 'not':
        
            for row in self.rows:
                if row[col_index] != col_val:
                    new_rows.append(row)
            filtered = data_frame(new_rows,self.col_names).show()  
            return filtered        
        
        
        if (comparison == 'greater') and (col_val.isnumeric()):
        
            for row in self.rows:
                if row[col_index] > col_val:
                    new_rows.append(row)
                    
            filtered = data_frame(new_rows,self.col_names).show()  
            return filtered               
        
        if (comparison == 'less') and (col_val.isnumeric()):
       
            for row in self.rows:
                if row[col_index] < col_val:
                    new_rows.append(row)
            filtered = data_frame(new_rows,self.col_names).show()  
            return filtered            
        
        if (comparison == 'less_or_eq') and (col_val.isnumeric()):
       
            for row in self.rows:
                if row[col_index] <= col_val:
                    new_rows.append(row)  
            
            filtered = data_frame(new_rows,self.col_names).show()  
            return filtered        
       
        if (comparison == 'greater_or_eq') and (col_val.isnumeric()):
       
            for row in self.rows:
                if row[col_index] >= col_val:
                    new_rows.append(row)
            filterd = data_frame(new_rows,self.col_names).show()  
            return filtered           
                 
                 
        else:
            print('must use numeric value with ' + comparison)
            return None
    
    
        


    #Given 2 dataframes with the same columns, but different rows, 'stack' or merge them vertically. 
    def stack(self, df):
        
        names = self.col_names
            
        if self.col_names != df.col_names:
            print("Can only stack 2 dataframes with the same column names")
        else:
            
            new_rows = [] 
            
            for i in self.rows:
                new_rows.append(i)
                
            for i in df.rows:
                new_rows.append(i)
                
            df_stacked = data_frame(new_rows, names)
           
            return df_stacked
        


    #Group the values of 1 column (the agg column) by the values of one column (the category or 'cat_col') and appyly a function.
    #This function treats any aggregation column values as floats, unless using the count function. It will fail if there is non-numeric
    #data in any column passed for aggregation. Non numeric columns are accepted in the group by (category or cat_col)
    def group_by_and_agg(self,cat_col,agg_col, func = "Sum",print_result = True):
        
        #Get indices of the group by column (category - cat_index) and the column you will be aggregating (agg_index)
        cat_index = self.col_names.index(cat_col)
        agg_index = self.col_names.index(agg_col)
    
        #Get a list of unique elements you will be grouping by. Create a list of them
        grouped = list(set(self.get_col(cat_col)))
        agg_rows = [[l] for l in grouped]
        
        #If the function is count, loop through each row and obtain the values of your aggregation column, and
        #concatenate them to the group by column. Try each value to see if it is numeric (can be converted to float)
        #If not, throw an error, as we can only aggregate numeric values. The exception is the count function. If aggregating
        #by count, we do not need to have all numeric values in the aggregation column (note the else clause)
        
        if func != "Count":
            for i in agg_rows:
                for j in self.rows:
                    if j[cat_index] == i[0]:
                        try:
                            i.append(float(j[agg_index]))
                        except:
                            print("Cannot perform aggregation, all values in column must be numeric")
                            return None
        else:
            for i in agg_rows:
                for j in self.rows:
                    if j[cat_index] == i[0]:
                            i.append(j[agg_index])
                        
        #Now that the values of the group by and aggregation are found and associated to eachother, apply the function, based 
        #on the users selection
        if func == "Sum":
            for i in agg_rows:
                agg_rows[agg_rows.index(i)] = [i[0],sum(i[1:])]
                                 
        if func == "Avg":
            for i in agg_rows:
                agg_rows[agg_rows.index(i)] = [i[0], (sum(i[1:]) / len(i[1:])) ]
                
        if func == "Min":
            for i in agg_rows:
                agg_rows[agg_rows.index(i)] = [i[0], min(i[1:]) ]
            
        if func == "Max":
            for i in agg_rows:
                agg_rows[agg_rows.index(i)] = [i[0], max(i[1:]) ]
         
        if func == "Count":
            for i in agg_rows:
                agg_rows[agg_rows.index(i)] = [i[0], len(i[1:]) ]       
         
        #If user attempts to enter an unknown function, throw an error.         
        if func not in ['Sum', 'Avg', 'Min', 'Max', 'Count']:
            print("Must use one of the following functions: Sum, Avg, Min, Max, Count")
            return None
        
        #Create a dataframe with the new rows and the selected columns.
        agg_frame = data_frame(agg_rows,[cat_col, func + " " + agg_col + " by " + cat_col])
        
        #Print result if users specifies, then return the resulting data frame
        if print_result == True:
            agg_frame.show()
        
        return agg_frame
            
     
        
    #Perform an inner join on 2 dataframes with 1 matching column.  
    def join_inner(self,df,key_col,print_result=False):
        
        #Get the column names for both dataframes
        left_names = [n for n in self.col_names]
        right_names = [n for n in df.col_names if n != key_col]
        
        #If the key column is not in either dataframe, this operation will print an error
        if (key_col not in self.col_names) or (key_col not in df.col_names):
            print("Key column msut be in both dataframes")
            return None
        
        #Obtain the indices of the key column in both dataframes
        left_df_key_index = self.col_names.index(key_col)
        right_df_key_index = df.col_names.index(key_col)
        
        #Creat a new list of all rows in the left dataframe
        rows_primary = []
        for i in self.rows:
            rows_primary.append(i)
        #Create an empty list for the joined rows
        joined_rows = []
        
        #For each row in the left dataframe, loop through the right dataframes rows. 
        for row in rows_primary:
            
            for j in df.rows:
                #When a match is found between the rows of the left and right dataframes, based on the key column, 
                #combine both rows together and append to the new list of joined columns. 
                #The key column is not appended twice.
                if j[right_df_key_index] == row[left_df_key_index]:
                    joined_rows.append(row + j[:right_df_key_index] + j[right_df_key_index+1:])
        
        #The names for the columns are the names of the 2 dataframes combined (the key column only appears once, however)
        final_names = left_names + right_names
        #Create the joined dataframe using the new rows and new columns
        joined_frame = data_frame(joined_rows,final_names)
        
        #If user specifies, show the entire resulting dataframe. 
        if print_result == True:
            joined_frame.show()
            
        return joined_frame
    
        
            
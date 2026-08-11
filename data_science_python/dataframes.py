## What is Pandas?
## Pandas is a powerful and flexible open-source data analysis and manipulation library for Python. It provides data structures like Series (1-dimensional) and DataFrame (2-dimensional) that make it easy to work with structured data. Pandas is widely used in data science, machine learning, and statistical analysis due to its ability to handle large datasets, perform complex operations, and integrate seamlessly with other libraries like NumPy, Matplotlib, and Scikit-learn.

# Pandas deal with dataframes
# dataframes are 2-dimensional labeled data structures with columns of potentially different types. You can think of them like a spreadsheet or SQL table, or a dict of Series objects. DataFrames are generally the most commonly used pandas object.

import os
# OS is used to change the woking directory to the location of the data file. This is important because it allows you to read and write files without having to specify the full path every time.

import pandas as pd
import numpy as np

os.chdir("C:/Users/HP/Documents/DS_21/DS_21/DS_21/data_science_python")
# Above line changes the current working directory to the specified path. This is useful when you want to read or write files in that directory without providing the full path.

# importing the data from the csv file
data = pd.read_csv("data.csv")

# Crating a copy of original data
data_copy = data.copy()
# shallow copy of the original data is created to ensure that any modifications made to the data_copy do not affect the original data. This is a good practice when working with data, as it allows you to preserve the original dataset for reference or further analysis.
# deep copy is not necessary here because we are not modifying the data_copy in a way that would affect the original data. However, if you were to modify the data_copy in a way that could affect the original data (e.g., changing values in place), you would want to use a deep copy instead.

samp = data.sample(n=5, random_state=1)
# The sample() function is used to randomly select a specified number of rows from the DataFrame. In this case, 5 random rows are selected from the data DataFrame. The random_state parameter is set to 1 to ensure that the same random sample is generated each time the code is run, which is useful for reproducibility.
# .coloums is used to access the column names of the DataFrame. It returns an Index object containing the column labels.

# .rows is used to access the rows of the DataFrame. It returns a DataFrame containing the rows of the original DataFrame.

# .size is used to get the number of elements in the DataFrame. It returns an integer representing the total number of elements (rows * columns) in the DataFrame.

# .shape is used to get the dimensions of the DataFrame. It returns a tuple representing the number of rows and columns in the DataFrame.
# .memory_usage() is used to get the memory usage of the DataFrame. It returns a Series containing the memory usage of each column in bytes.

# .ndim gives the number of dimensions of the DataFrame. It returns an integer representing the number of dimensions (1 for Series, 2 for DataFrame).
# .head() is used to view the first few rows of the DataFrame. By default, it returns the first 5 rows, but you can specify a different number of rows to display by passing an integer as an argument (e.g., .head(10) to view the first 10 rows).

# .tail() is used to view the last few rows of the DataFrame. By default, it returns the last 5 rows, but you can specify a different number of rows to display by passing an integer as an argument (e.g., .tail(10) to view the last 10 rows).

# .at and iat are used to access a single value in the DataFrame. .at is label-based, while .iat is integer position-based. For example, data.at[0, 'column_name'] would return the value in the first row of the specified column, while data.iat[0, 0] would return the value in the first row and first column.

# .loc and iloc are used to access a group of rows and columns by labels or integer positions, respectively. .loc is label-based, while .iloc is integer position-based. For example, data.loc[0:5, 'column_name'] would return the first 6 rows of the specified column, while data.iloc[0:5, 0] would return the first 6 rows of the first column.

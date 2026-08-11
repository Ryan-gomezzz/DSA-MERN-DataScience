# Numpy is used for numerical computing in Python. It provides support for large, multi-dimensional arrays and matrices, along with a collection of mathematical functions to operate on these arrays.
import numpy as np

# In array all elemets should be of same data type. If we try to create an array with mixed data types, NumPy will upcast the elements to a common data type.

# Used for scientific computing, data analysis, and machine learning tasks. It is a fundamental library for numerical computations in Python.

my_list = [1, 2, 3, 4, 5,6]
my_array = np.array(my_list)

array = np.array(my_list, dtype=float)  # Specify data type as float
print(array)  # Output: [1. 2. 3. 4. 5.]

print(type(array))  # Output: <class 'numpy.ndarray'>
print(len(array))  # Output: 5
print(array.ndim) # Output: 1 (number of dimensions)
print(array.shape) # Output: (5,) (shape of the array)

array2 = array.reshape(3,2)
print(array2)  # Output: [[1. 2.]
              #          [3. 4.]
                #          [5. 0.]] (reshaped array)

array3 = array.reshape(3,-1)
print(array3)  # Output: [[1. 2.]
              #          [3. 4.]
                #          [5. 0.]] (reshaped array with inferred dimension)


# Initializing numpy arrays from nests python lists 

my_list1 = [[1, 2, 3,4, 5, 6]]
my_list2 = [[7, 8, 9,10, 11, 12]]

multi_array = np.array([my_list1, my_list2])
print(multi_array)  # Output: [[ 1  2  3  4  5  6]
              #          [ 7  8  9 10 11 12]]

r = range(24)
print(r)  # Output: range(0, 24)

a = np.arange(24)
print(a)  # Output: [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19
          #          20 21 22 23]   
b = np.arange(24).reshape(4, 6)
print(b)  # Output: [[ 0  1  2  3  4  5]
          #          [ 6  7  8  9 10 11]
          #          [12 13 14 15 16 17]    
        #          [18 19 20 21 22 23]] (reshaped array)
c = np.arange(2,24)
print(c)  # Output: [ 2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23] (array starting from 2 to 23)   

# Arithmatic operations on numpy arrays are performed element-wise. This means that the operation is applied to each corresponding element of the arrays.

print(np.sum(a))

print(np.sum(b, axis =0))  # Output: [36 40 44 48 52 56] (sum along columns)
print(np.sum(b, axis =1))  # Output: [15 51 87 123] (sum along rows)

print(np.mean(b, axis =0))  # Output: [ 9. 10. 11. 12. 13. 14.] (mean along columns)
print(np.mean(b, axis =1))  # Output: [ 2.5  8.5 14.5 20.5] (mean along rows)


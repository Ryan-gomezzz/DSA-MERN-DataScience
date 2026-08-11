# We will be doing operations on sequence data types in Python. The sequence data types include lists, tuples, and strings. These data types allow us to store multiple items in a single variable and provide various methods to manipulate the data.
# Strings
strsample = "Hello, World!"

print(strsample.index("W"))  # Output: 7
print(strsample.count("o"))  # Output: 2

print(strsample[-2])
print(strsample[7:12])  # Output: World

#Lists
list1 = [1, 2, 3, 4, 5]
print(list1[0])  # Output: 1

print(list1.index(3))  # Output: 2
print(list1.count(2))  # Output: 1

#Arrays
from array import array
arr = array('i', [1, 2, 3, 4, 5])
print(arr[0])  # Output: 1
for x in arr: print(x)

#tuples
tuple1 = (1, 2, 3, 4, 5)
print(tuple1[0])  # Output: 1
tuple1.index(3)  # Output: 2

dict1 = {'a': 1, 'b': 2, 'c': 3}
print(dict1['a'])  # Output: 1
# indexing cannot be performed on dictionaries, but we can access values using keys.
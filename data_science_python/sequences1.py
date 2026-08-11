# Slicing

from sequences import list1

print(list1[1:4])  # Output: [2, 3, 4]

print(list1[slice(1, 4, 2)])  # Output: [2, 4]

str1 = "Ryan"
str2 = "Gomez"

print(str1+str2)  # Output: RyanGomez
print(list1+['py'])  # Output: [1, 2, 3, 4, 5, 'py']

#concatenation of 2 array 
arr1 = array('i', [1, 2, 3])
arr2 = array('i', [4, 5, 6])
print(arr1 + arr2)  # Output: array('i', [1, 2, 3, 4, 5, 6])


print(list1*2)  # Output: [1, 2, 3, 4, 5, 1, 2, 3, 4, 5]
print(str1*3)  # Output: RyanRyanRyan

a = (1, 2)
b = (3, 4)
c = a + b  # (1, 2, 3, 4)

# t[0] = 10  ypeError: 'tuple' object does not support item assignment


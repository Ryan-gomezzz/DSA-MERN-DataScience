arr = [1,2,5,3,7,4,4,9]

a = sorted(arr)
print(a)

b = sorted(arr, reverse=True)
print(b)

#sorting in absolute values 
arr1 = [-1, -2, 5, -3, 7, 4, 4, -9]

c = sorted(arr1, key=lambda x: abs(x))

print(c)

# Sort by custom key
words = ["apple", "pie", "banana"]
d = sorted(words, key=len)  
print(d)  # Output: ['pie', 'apple', 'banana']

min([3, 1, 4, 1, 5])           # 1
max([3, 1, 4, 1, 5])           # 5

sum([1, 2, 3, 4])              # 10
sum([1, 2, 3], 10)             # 16 (starts from 10)

import math
math.prod([2, 3, 4])          # Product: 24 (Python 3.8+)

len([1, 2, 3])                 # 3
"hello".count('l')             # 2

any([False, True, False])       # True
all([True, True, True])        # True
any([])                        # False (empty is False)

for i, val in enumerate([10, 20, 30]):
    print(i, val)              # 0 10, 1 20, 2 30
list(enumerate(['a', 'b', 'c']))  # [(0, 'a'), (1, 'b'), (2, 'c')]
list(enumerate(['a', 'b'], 1))     # [(1, 'a'), (2, 'b')] (start=1)

list(zip([1, 2], [3, 4]))      # [(1, 3), (2, 4)]
list(zip([1, 2, 3], [4, 5]))   # [(1, 4), (2, 5)] (stops at shortest)
list(zip([1, 2], [3, 4], [5, 6]))  # [(1, 3, 5), (2, 4, 6)]

list(reversed([1, 2, 3]))     # [3, 2, 1]
"hello"[::-1]                  # "olleh" (string slicing)


list(range(5))                 # [0, 1, 2, 3, 4]
list(range(1, 5))              # [1, 2, 3, 4]
list(range(0, 10, 2))          # [0, 2, 4, 6, 8]

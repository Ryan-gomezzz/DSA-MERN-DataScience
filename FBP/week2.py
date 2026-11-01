a = 1
b = 2
c = a + b
print(c)

list1 = [1, 2, 3, 4, 5]
print(list1[-1])  # prints the last element of the list
# print(list1[:3])  # prints the first three elements of the list

dict1 = {"name": "Ryan", "standard": "10th", "age": 15}
print(dict1)

contact = {"name": "Ryan", "phone": 1234567890, "email": "ryangomez9965@gmail.com"}
print(contact)

def add(x, y):
    return x + y

print(add(5, 10))

def shlok(a, b):
    return a - b

print(shlok(10, 5))

def multiply(x, y, a, b):
    return x * y * a * b

print(multiply(2, 3, 4, 5))

list2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
total = 0
for i in list2:
    total += i

print(total)


class Total:
    def __init__(self, values=None):
        self.values = list(values) if values is not None else []

    def add(self, value):
        self.values.append(value)
        return self

    def calculate(self):
        return sum(self.values)

    def average(self):
        if not self.values:
            return 0
        return sum(self.values) / len(self.values)

    def __repr__(self):
        return f"Total(values={self.values}, total={self.calculate()})"


# Example usage of the Total class
numbers = Total([10, 20, 30, 40])
print(numbers.calculate())
print(numbers.average())
numbers.add(50)
print(numbers.calculate())
print(numbers.average())
print(numbers)



print("Enter a number")

a = int(input())

print("Enter another number")

b = int(input())

print("Enter the operation you want to perform (+, -, *, /)")

c = input()

def calculator(a, b, c):
    if c == "+":
        return a + b
    elif c == "-":
        return a - b
    elif c == "*":
        return a * b
    elif c == "/":
        return a / b
    else:
        return "Invalid operation"

print(calculator(a, b, c))
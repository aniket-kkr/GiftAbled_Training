a = int(input("Enter first integer: "))
b = int(input("Enter second integer: "))
while b != 0:
    a, b = b, a % b
print(abs(a))

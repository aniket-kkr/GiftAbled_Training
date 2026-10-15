n = int(input("How many Fibonacci numbers? "))
a, b = 0, 1
for _ in range(max(0, n)):
    print(a, end=" ")
    a, b = b, a + b
print()

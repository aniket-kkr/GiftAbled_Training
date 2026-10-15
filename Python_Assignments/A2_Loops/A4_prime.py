n = int(input("Enter an integer: "))
prime = n >= 2
for i in range(2, int(n ** 0.5) + 1):
    if n % i == 0:
        prime = False
        break
print("Prime" if prime else "Not prime")

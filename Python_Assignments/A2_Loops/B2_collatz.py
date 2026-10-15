n = int(input("Enter a positive integer: "))
if n <= 0:
    print("Please enter a positive integer")
else:
    while n != 1:
        print(n, end=" ")
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
    print(1)

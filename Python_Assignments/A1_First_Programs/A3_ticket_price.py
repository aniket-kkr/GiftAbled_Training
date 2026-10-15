age = int(input("Enter age: "))

if age < 0:
    print("Invalid age")
elif age < 5:
    price = 0
elif age < 18:
    price = 100
elif age < 60:
    price = 200
else:
    price = 120

if age >= 0:
    print("Ticket price:", price)

numbers = list(map(int, input("Enter numbers separated by spaces: ").split()))
unique = sorted(set(numbers), reverse=True)
if len(unique) < 2:
    print("No second-largest distinct number")
else:
    print("Largest:", unique[0])
    print("Second largest:", unique[1])

import csv
import json

names = ["Aniket", "Rahul", "Priya"]

with open("students.txt", "w", encoding="utf-8") as f:
    for name in names:
        f.write(name + "\\n")

with open("students.txt", "r", encoding="utf-8") as f:
    print("TXT:", [line.strip() for line in f])

students = [
    {"name": "Aniket", "marks": 85},
    {"name": "Rahul", "marks": 72},
    {"name": "Priya", "marks": 91},
]

with open("students.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "marks"])
    writer.writeheader()
    writer.writerows(students)

with open("students.csv", "r", newline="", encoding="utf-8") as f:
    print("CSV:", list(csv.DictReader(f)))

student_data = {"name": "Aniket", "marks": 85}
with open("students.json", "w", encoding="utf-8") as f:
    json.dump(student_data, f, indent=2)

with open("students.json", "r", encoding="utf-8") as f:
    print("JSON:", json.load(f))

import csv

with open(r'test.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)

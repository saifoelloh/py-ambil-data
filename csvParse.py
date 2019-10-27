import csv
input_file = csv.DictReader(open("myBigData.csv"))
for row in input_file:
    print row['nim']
    print row['ipk']
    print row['name']
    print row['status']

import csv

with open("api_yamdb/static/data/comments.csv", encoding='utf-8') as r_file:
     file_reader = csv.DictReader(r_file, delimiter = ",")
     count = 0
     for row in file_reader:
         print(row)
         count += 1
     print(f'Всего в файле {count + 1} строк.')

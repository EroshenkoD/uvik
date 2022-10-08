import csv
from pprint import pprint

with open('data.csv') as file:
    data = list(csv.reader(file))

del data[0]
res_dict = {}
for i in data:
    if i[0] in res_dict:
        res_dict[i[0]]['people'].append(i[1])
        res_dict[i[0]]['count'] += 1
    else:
        temp = {
            'count': 1,
            'people': [i[1]]
        }
        res_dict[i[0]] = temp

pprint(res_dict)

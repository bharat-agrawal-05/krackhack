import json 

with open('stock_data.json', 'r') as file:
    data = json.load(file)
    print(data)

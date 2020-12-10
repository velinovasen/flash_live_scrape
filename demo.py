import json
from datetime import date

with open('oddsportal_data.json', 'r') as f:
    data = json.load(f)

print(date.today())
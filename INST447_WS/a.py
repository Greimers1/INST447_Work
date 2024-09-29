import json
import requests

response = requests.get('https://date.nager.at/api/v3/publicholidays/2022/US')
public_holidays = json.loads(response.content)

for public_holiday in public_holidays:
  print(f"""{public_holiday['name']}: {public_holiday['date']}""")
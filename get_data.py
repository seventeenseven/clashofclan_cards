import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cards_game.settings')
django.setup()

import requests
from pprint import pprint
#import json
from trading.models import Cards




url = "https://api.clashofclans.com/v1/players/%23UU9RURJL"
headers = {
    'Accept': "application/json",
    'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImU4YmQ0ZjljLWQwMzUtNGZkNC1hYWY3LTJhNGQ4YjY3MTdmMiIsImlhdCI6MTU3Nzc3NDU1MSwic3ViIjoiZGV2ZWxvcGVyL2M4Nzk0MzY0LTRkNzktZDI0Yi03ZmZmLWQzMmY3NjFkY2JiZiIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjM3LjE0Mi41MS4xNzYiLCI4OS4yMzcuOTguMTEwIl0sInR5cGUiOiJjbGllbnQifV19.mB9KlKTpAOq-8PhPn-sqiuXDxiSnJFwa8j1gckEmSBjaPfjoC5yj4_ACuGgxMb3YWJfOiZ4dUkpCjp5otqZVXw"
    }
response = requests.request("GET", url, headers=headers)
data = response.json()
troop = data['troops']
heroes = data['heroes']
spells = data['spells']
pprint(spells[0]['village'])
pprint(spells)

# with open('coc_troop.txt', 'w') as outfile:
#     json.dump(troop, outfile)



# for i in range(len(spells)):
#     new_card = Cards(
#         name=spells[i]['name'],
#         village=spells[i]['village'],
#         level=spells[i]['level'],
#         maxLevel=spells[i]['maxLevel'],
#         heroes=False,
#         xp=(spells[i]['maxLevel'])*10
#         )
#     new_card.save()
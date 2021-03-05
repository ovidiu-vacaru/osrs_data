from data import GrandExchange
import json

ge = GrandExchange()


top100 = ge.display_top_twenty("2")
print(top100)

ge.populatedb_items(top100)
items = ge.extract_items()

objs = []
for item in items:
    objs.append(item[1])
ge.populatedb_values(objs)




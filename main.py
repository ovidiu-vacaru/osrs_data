from data import GrandExchange
import json

ge = GrandExchange()


object_id = ge.display_top_twenty("2")
ge.populatedb_items(object_id)


import json
import requests
from SocioSim.utils.database import send_data_to_database, get_data_from_database

data = {'name': 'Southern-Style Pulled Pork Sandwich', 'description': 'Slow-cooked, smoky pulled pork topped with our homemade tangy coleslaw and served on a toasted brioche bun.', 'price': 14, 'cost_price': 7}

def test(data):
    # data = json.dumps(data)
    response = requests.post("http://localhost:9001/menu/", json=data)
    print(response)
    # send_data_to_database(data, "menu", 9001)

test(data)
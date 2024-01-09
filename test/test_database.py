import json
import requests

data = {'name': 'Southern-Style Pulled Pork Sandwich', 'description': 'Slow-cooked, smoky pulled pork topped with our homemade tangy coleslaw and served on a toasted brioche bun.', 'price': 14, 'cost_price': 7}

def test(data):
    # data = json.dumps(data)
    response = requests.get("http://localhost:9000/menu/")
    print(response.text)
    print(response.json())
    # send_data_to_database(data, "menu", 9001)

test(data)
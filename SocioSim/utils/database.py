import json
import requests


def get_data_from_database(endpoint, port, base_url="http://localhost:"):
    response = requests.get(f"{base_url}{port}/{endpoint}/")
    if response.status_code == 200:
        data = response.json()  # e.g. [{'id': 1, 'name': 'Yangzhou Fried Rice', 'price': 9, 'cost_price': 3, 'description': 'Flavorful Yangzhou fried rice with chicken, shrimp, green peas, and eggs.'}]
        return data
    else:
        raise Exception(f"error: get data from database: {endpoint} {port} {response.status_code}")

def send_data_to_database(data, endpoint, port, base_url="http://localhost:"):
    # handle the case when different types of res
    if isinstance(data, dict):
            res_list = [data]
    elif isinstance(data, list):
        res_list = data
    else:
        try:
            res_list = json.loads(data)
            if not isinstance(res_list, list):
                res_list = [res_list]
        except:
            raise Exception("error: data should be a dict or a list of dict")
    
    url = f"{base_url}{port}/{endpoint}/"
    for res in res_list:
        data_type = res["type"]
        
        if data_type == "add":
            response = requests.post(url, json=res["data"])
            if response.status_code != 201:
                raise Exception(f"A error occur when adding data to {endpoint}: {response.status_code}")
        elif data_type == "delete":
            response = requests.delete(f"{url}{res['id']}/")
            if response.status_code != 204:
                raise Exception(f"A error occur when deleting data to {endpoint}: {response.status_code}")
        elif data_type == "update":
            response = requests.put(f"{url}{res['id']}/", json=res["data"])
            if response.status_code != 200:
                raise Exception(f"A error occur when updating data to {endpoint}: {response.status_code}")
        elif data_type == "partial_update":
            response = requests.patch(f"{url}{res['id']}/", json=res["data"])
            if response.status_code != 200:
                raise Exception(f"A error occur when updating data to {endpoint}: {response.status_code}")
        else: 
            raise Exception(f"error: No this type {data_type}")
 
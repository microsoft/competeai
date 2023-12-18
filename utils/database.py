import json
import logging
import requests


def get_data_from_database(endpoint, base_url="http://localhost:", port="8000"):
    response = requests.get(f"{base_url}{port}/{endpoint}/")
    if response.status_code == 200:
        data = response.json()  # e.g. [{'id': 1, 'name': 'Yangzhou Fried Rice', 'price': 9, 'cost_price': 3, 'description': 'Flavorful Yangzhou fried rice with chicken, shrimp, green peas, and eggs.'}]
        return data
    else:
        print(f"error: {response.status_code}")
        # print(response.text)
        return None

def send_data_to_database(res, endpoint, base_url="http://localhost:", port="8000"):
    # handle the case when different types of res
    if isinstance(res, dict):
            res_list = [res]
    elif isinstance(res, list):
        res_list = res
    else:
        try:
            res_list = json.loads(res)
            if not isinstance(res_list, list):
                res_list = [res_list]
        except:
            logging.warning("invalid json")
            return
    
    url = f"{base_url}{port}/{endpoint}/"
    for res in res_list:
        data_type = res["type"]
        
        if data_type == "add":
            response = requests.post(url, json=res["data"])
            if response.status_code == 201:
                logging.info("success")
            else:
                logging.warning(f"error: {response.status_code}")
                logging.warning(response.text)
        elif data_type == "delete":
            response = requests.delete(f"{url}{res['id']}/")
            if response.status_code == 204:
                logging.info("success")
            else:
                logging.warning(f"error: {response.status_code}")
                logging.warning(response.text)
        elif data_type == "update":
            response = requests.put(f"{url}{res['id']}/", json=res["data"])
            if response.status_code == 200:
                logging.info("success")
            else:
                logging.warning(f"error: {response.status_code}")
                logging.warning(response.text)
        elif data_type == "partial_update":
            response = requests.patch(f"{url}{res['id']}/", json=res["data"])
            if response.status_code == 200:
                logging.info("success")
            else:
                logging.warning(f"error: {response.status_code}")
                logging.warning(response.text)
        else: 
            logging.warning(f"error: No this type {data_type}")
 
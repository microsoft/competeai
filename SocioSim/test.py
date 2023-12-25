from utils.database import get_data_from_database

res = get_data_from_database("menu", port=9001)
print(res)
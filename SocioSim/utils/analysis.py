import os
import re
import csv
import json
import openai

from .draw import Draw
from .prompt_template import PromptTemplate


openai.api_key = os.getenv("OPENAI_KEY")

def get_gpt_response(prompt):
    """ OpenAI 0.27 version"""
    # FIXME: v 0.28.1
    messages = [{'role': 'user', 'content': prompt}]
    completion = openai.ChatCompletion.create(
                model="gpt-4-1106-preview",
                messages=messages,
                temperature=0.7,
                max_tokens=1000,
            )
        
    response = completion.choices[0]['message']['content']
    response = response.strip()
    return response

def read_csv(path, fields):
    res = {}
    
    if isinstance(fields, str):
        fields = [fields]
        
    with open(path, mode='r') as file:
        csv_reader = csv.reader(file)    
        for row in csv_reader:
            if row[0] in fields:
                res[row[0]] = row[1:]

    return res

def analysis_menu(menu1, menu2):
    if isinstance(menu1, str):
        menu1 = json.loads(menu1)
    if isinstance(menu2, str):
        menu2 = json.loads(menu2)
    
    print(menu1)
    print(type(menu1))
    
    # 计算两个餐馆各自菜的数量
    num_dish1 = len(menu1)
    num_dish2 = len(menu2)

    # 计算每个餐馆的菜的平均价格
    price1 = [dish['price'] for dish in menu1]
    avg_price1 = sum(price1) / len(price1)

    price2 = [dish['price'] for dish in menu2]
    avg_price2 = sum(price2) / len(price2)
    
    # 向gpt查询两个菜单中相同的菜，记录相似菜的数量
    prompt_template = PromptTemplate(["analysis_menu"])
    prompt = prompt_template.render(data=[menu1, menu2])
    print(prompt)
    response = get_gpt_response(prompt)
    print(response)
    
    # find first { and last }
    pattern = r"\{[\s\S]*\}"

    response = re.findall(pattern, response)[0]
    print(response)
    response = json.loads(response)

    similar_dish1 = response['restaurant1']
    similar_dish2 = response['restaurant2']

    num_similar_dish = len(similar_dish1)

    # 计算两个餐馆相似菜的平均价格, 遍历菜单查看每个菜的id是否在similar_dish中
    similar_price1 = []
    similar_price2 = []

    for dish in menu1:
        if dish['id'] in similar_dish1:
            similar_price1.append(dish['price'])

    for dish in menu2:
        if dish['id'] in similar_dish2:
            similar_price2.append(dish['price'])
        
    avg_similar_price1 = sum(similar_price1) / num_similar_dish
    avg_similar_price2 = sum(similar_price2) / num_similar_dish
    
    # put data into a dict
    data = {
        'num_dish1': num_dish1,
        'num_dish2': num_dish2,
        'num_similar_dish': num_similar_dish,
        'avg_price1': avg_price1,
        'avg_price2': avg_price2,
        'avg_similar_price1': avg_similar_price1,
        'avg_similar_price2': avg_similar_price2
    }
    
    return data

def analysis_menus(path1, path2):
    res = []
    
    # from two path read the menus in csv file
    menus1 = read_csv(path1, fields=['menu'])['menu']
    menus2 = read_csv(path2, fields=['menu'])['menu']
    
    # call anaysis_menu to analysis the menus
    for menu1, menu2 in zip(menus1, menus2):
        data = analysis_menu(menu1, menu2)
        res.append(data)
    
    print(res)
    
    # analysis the res and draw the graph
    avg_price1 = []
    avg_price2 = []
    avg_similar_price1 = []
    avg_similar_price2 = []
    similar_proportion = []
    for r in res:
        avg_price1.append(r['avg_price1'])
        avg_price2.append(r['avg_price2'])
        avg_similar_price1.append(r['avg_similar_price1'])
        avg_similar_price2.append(r['avg_similar_price2'])
        
        p = 2 * r['num_similar_dish'] / (r['num_dish1'] + r['num_dish2'])
        similar_proportion.append(p)
    
    return {
        'avg_price1': avg_price1,
        'avg_price2': avg_price2,
        'avg_similar_price1': avg_similar_price1,
        'avg_similar_price2': avg_similar_price2,
        'similar_proportion': similar_proportion
    }
    
def analysis_data(path1, path2):
    # from two path read the data in csv file
    data1 = read_csv(path1, fields=['num_of_customer', 'dish_score', 'customer_score'])
    data2 = read_csv(path2, fields=['num_of_customer', 'dish_score', 'customer_score'])
    
    num_of_customer1 = [int(d) for d in data1['num_of_customer']]
    num_of_customer2 = [int(d) for d in data2['num_of_customer']]
    
    dish_score1 = [float(d) for d in data1['dish_score']]
    dish_score2 = [float(d) for d in data2['dish_score']]
    
    customer_score1 = [float(d) for d in data1['customer_score']]
    customer_score2 = [float(d) for d in data2['customer_score']]
    
    return {
        'num_of_customer1': num_of_customer1,
        'num_of_customer2': num_of_customer2,
        'dish_score1': dish_score1,
        'dish_score2': dish_score2,
        'customer_score1': customer_score1,
        'customer_score2': customer_score2
    }

def analysis(path):
    draw = Draw(path)
    
    # Part1: analysis the menus
    menu_path1 = os.path.join(path, 'restaurant_design_9000', 'menu.csv')
    menu_path2 = os.path.join(path, 'restaurant_design_9001', 'menu.csv')
    
    data = analysis_menus(menu_path1, menu_path2)
    
    draw.similar_proportion(data['similar_proportion'])
    draw.avg_price(data['avg_price1'], data['avg_price2'])
    draw.similar_avg_price(data['avg_similar_price1'], data['avg_similar_price2'])
    
    # Part2: analysis the scores
    data_path1 = os.path.join(path, 'restaurant_design_9000', 'data.csv')
    data_path2 = os.path.join(path, 'restaurant_design_9001', 'data.csv')
    
    data = analysis_data(data_path1, data_path2)
    
    draw.customer_flow(data['num_of_customer1'], data['num_of_customer2'])
    draw.dish_score(data['dish_score1'], data['dish_score2'])
    draw.customer_score(data['customer_score1'], data['customer_score2'])
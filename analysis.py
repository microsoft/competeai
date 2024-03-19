# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import os
import re
import time
import yaml
import openai
import multiprocessing

openai.api_key = os.getenv("OPENAI_KEY")
print(openai.api_key)

prompt_template = """
You are outstanding data analysts. Now you need to analyze the reason of customer choices. Next is the thought process of customer:
{process}

This customer role description is 
{role_desc}

Please choose single or multi options:
1: Meet Core Needs (Align with diet restriction or taste)
2: Brand Loyalty (Customer previous experience)
3: Public Praise (High Score or Positive comments)
4: More Affordable or Reasonable
5: Unique or Signature Dish
6: Explore New Dining Experience or Flavor

Only output all answer (1 - 6)
"""

prompt_template_group = """
You are outstanding data analysts. Now you need to analyze the reason of customer choices. Next is the thought process of customer:
{process}

Please choose single or multi options:
1: Meet Core Needs (Align with diet restriction or taste)
2: Brand Loyalty (Customer previous experience)
3: Public Praise (High Score or Positive comments)
4: More Affordable or Reasonable
5: Unique or Signature Dish
6: Explore New Dining Experience or Flavor

Only output all answer (1 - 6)
"""


def get_gpt_response(prompt):
    messages = [{'role': 'user', 'content': prompt}]
    completion = openai.ChatCompletion.create(
                model="gpt-4-1106-preview",
                messages=messages,
                temperature=0.7,
                max_tokens=2000,
            )
        
    response = completion.choices[0]['message']['content']
    response = response.strip()
    
    time.sleep(5)
    return response

# 统计客户选择原因
def single_reason(path='./logs'):
    # 读取 group.yaml文件
    with open('competeai/examples/group.yaml', 'r') as f:
        config = yaml.safe_load(f)

    # read all players
    players = config['players']
    players = players[2:]
    players_name = [ 'Jack', 'Xena', 'Bob']
    
    # 构建name2index的dict
    player2idx = {}
    player2role = {}
    for i, player in enumerate(players):
        player2idx[player['name']] = i
        player2role[player['name']] = player['role_desc']
        
    group2idx = {}
    # 读取config中scenes中的第二个元素的players
    players = config['scenes'][1]['players']
    # this list contain group inforamtion, find all single element
    for i, player in enumerate(players):
        if isinstance(player, str):
            group2idx[player] = i
    
    # 除去 Oscar,Umar剩余8个顾客
    customers = players_name
    
    # 读取logs所有的文件
    exps_name = os.listdir(path)
    # get all exp named with 'single
    exps = [exp for exp in exps_name if 'single' in exp or 'group' in exp]
    
    # find the customer dine history message in each log folder
    # 使用文件记录全过程
    log = open('log_single.txt', 'a')
    # 用字典记录每个顾客选择的原因
    customers_reason = {}
    for customer in customers:
        log.write(f'Customer: {customer}\n')
        role_desc = player2role[customer]
        customer_reason = {}
        
        for exp in exps:
            log.write(f'Experiment: {exp}\n')
            
            exp_path = os.path.join(path, exp)
            index = player2idx[customer] if 'single' in exp else group2idx[customer]
            file_name = f'dine_{index}'
            # print(file_name)
            content = open(os.path.join(exp_path, file_name), 'r')
            content = content.read()
            
            # 根据结构找到每一次客户选择过程
            # 从下面的结构提取内容 " "reason" (xxx) }"
            # regular match
            def regular_match(content):
                pattern = r"\"reason\"(.*?)}"
                # 需要匹配换行符
                res = re.findall(pattern, content, re.S)
                # res = re.findall(pattern, content)
                format_tag = "Only compare"
                res = [r.strip() for r in res if format_tag not in r]
                return res

            def regular_match_2(content):
                pattern = r"\"summary\"(.*?)}"
                # 需要匹配换行符
                res = re.findall(pattern, content, re.S)
                # res = re.findall(pattern, content)
                format_tag = "including why this"
                res = [r.strip() for r in res if format_tag not in r]
                return res
            
            
            processes = regular_match(content)
            
            # 使用gpt询问每个过程中出现的原因
            cnt = {}
            for process in processes:
                
                prompt = prompt_template.format(process=process, role_desc=role_desc)
                ans = get_gpt_response(prompt)
                print(ans)
                # 提取答案（A-E)
                pattern = r"[1-6]"
                ans = re.findall(pattern, ans)
                print(ans)
                
                ans_str = ','.join(ans)
                log.write(f'Reason: {ans_str}\n')
                # 将选项插入计数字典中
                for r in ans:
                    if r not in customer_reason:
                        customer_reason[r] = 1
                    else:
                        customer_reason[r] += 1
  
                    if r not in cnt:
                        cnt[r] = 1
                    else:
                        cnt[r] += 1
            # 记录本次实验该顾客选择的原因总数
            log.write(f'one exp reason dict: {cnt}\n')
        log.write(f'{customer}: {customer_reason}\n')
        customers_reason[customer] = customer_reason
        print(customers_reason)
    print(customers_reason)
    
def group_reason(path='./logs'):
    # 读取 group.yaml文件
    with open('competeai/examples/group.yaml', 'r') as f:
        config = yaml.safe_load(f)
        
    # read all players
    players = config['players']
    players = players[2:]
    
    # 2 - 14 13个顾客组
    groups = list(range(9, 15))
    
    # 读取logs所有的文件
    exps_name = os.listdir(path)
    # get all exp named with 'single
    exps = [exp for exp in exps_name if 'group' in exp]
    
    # find the customer dine history message in each log folder
    # 使用文件记录全过程
    log = open('log_group.txt', 'a')
    # 用字典记录每个顾客选择的原因
    groups_reason = {}
    for group in groups:
        log.write(f'group id: {group}\n')

        group_reason = {}
        for exp in exps:
            log.write(f'Experiment: {exp}\n')
            
            exp_path = os.path.join(path, exp)
            index = 10 + int(group)
            file_name = f'group_dine_{index}'
            # print(file_name)
            content = open(os.path.join(exp_path, file_name), 'r')
            content = content.read()
            
            # 根据结构找到每一次客户选择过程
            # 从下面的结构提取内容 " "summary" (xxx) }"
            # regular match
            def regular_match(content):
                pattern = r"\"summary\"(.*?)}"
                # 需要匹配换行符
                res = re.findall(pattern, content, re.S)
                # res = re.findall(pattern, content)
                format_tag = "including why this"
                res = [r.strip() for r in res if format_tag not in r]
                return res
            
            processes = regular_match(content)
            
            # 使用gpt询问每个过程中出现的原因
            cnt = {}
            for process in processes:
                
                prompt = prompt_template_group.format(process=process)
                ans = get_gpt_response(prompt)
                print(ans)
                # 提取答案（1-6)
                pattern = r"[1-6]"
                ans = re.findall(pattern, ans)
                print(ans)
                
                ans_str = ','.join(ans)
                log.write(f'Reason: {ans_str}\n')
                # 将选项插入计数字典中
                for r in ans:
                    if r not in group_reason:
                        group_reason[r] = 1
                    else:
                        group_reason[r] += 1
  
                    if r not in cnt:
                        cnt[r] = 1
                    else:
                        cnt[r] += 1
            # 记录本次实验该顾客选择的原因总数
            log.write(f'one exp reason dict: {cnt}\n')
        log.write(f'group_{group}: {group_reason}\n')
        groups_reason[group] = group_reason
        print(groups_reason)
    print(groups_reason)           
       
if __name__ == "__main__":
    # get current path
    # print(os.getcwd())
    
    # 并行运行group 和 single
    
    # single_reason('./logs')
    group_reason('./logs')
    
    # 创建两个进程，分别运行func1和func2，并传递参数
    # process1 = multiprocessing.Process(target=single_reason)
    # process2 = multiprocessing.Process(target=group_reason)

    # # 启动进程
    # process1.start()
    # process2.start()

    # # 等待两个进程完成
    # process1.join()
    # process2.join()

    # print("Both functions have finished.")
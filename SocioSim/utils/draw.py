import os
import scienceplots

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

plt.style.use('science')
colors = sns.color_palette("coolwarm", 3)

class Draw:
    def __init__(self, path):
        self.path = path
        
    def customer_flow(self, data1, data2):
        plt.figure()

        days = list(range(1, len(data1) + 1))
        plt.xticks(days)
        
        plt.plot(days, data1, label='R1', marker='o', linestyle='-', color=colors[0])
        plt.plot(days, data2, label='R2', marker='x', linestyle='--', color=colors[2])

        plt.xticks([x for x in days if x % 2 == 0])
        
        plt.legend()
        plt.xlabel('Day')
        plt.ylabel('Customer flow')

        print(os.getcwd())
        path = os.path.join(self.path, 'fig', 'fig-customer-flow.pdf')
        plt.savefig(path)

    def dish_score(self, data1, data2):
        plt.figure()

        days = list(range(1, len(data1) + 1))
        plt.xticks(days)
        
        plt.plot(days, data1, label='R1', marker='o', linestyle='-', color=colors[0])
        plt.plot(days, data2, label='R2', marker='x', linestyle='--', color=colors[2])

        plt.xticks([x for x in days if x % 2 == 0])
        
        plt.grid(True, which='major', linewidth=0.8, color='#DDDDDD', axis='both')
        plt.grid(which='minor', color='#EEEEEE', linestyle=':', linewidth=0.5)
        
        # plt.title('score curve')
        plt.legend()
        plt.xlabel('Day')
        plt.ylabel('Avg score of dishes')

        path = os.path.join(self.path, 'fig', 'fig-dishes-score.pdf')
        plt.savefig(path)

    def customer_score(self, data1, data2):
        plt.figure()

        days = list(range(1, len(data1) + 1))
        plt.xticks(days)
        
        plt.plot(days, data1, label='R1', marker='o', linestyle='-', color=colors[0])
        plt.plot(days, data2, label='R2', marker='x', linestyle='--', color=colors[2])

        plt.xticks([x for x in days if x % 2 == 0])
        
        # plt.title('score curve')
        plt.legend()
        plt.xlabel('Day')
        plt.ylabel('Avg score of customers')

        path = os.path.join(self.path, 'fig', 'fig-customers-score.pdf')
        plt.savefig(path)

    def avg_price(self, data1, data2):
        plt.figure()

        days = list(range(1, len(data1) + 1))
        plt.xticks(days)
        
        plt.plot(days, data1, label='R1', marker='o', linestyle='-', color=colors[0])
        plt.plot(days, data2, label='R2', marker='x', linestyle='--', color=colors[2])

        plt.xticks([x for x in days if x % 2 == 0])
        
        plt.legend()
        plt.xlabel('Day')
        plt.ylabel('Avg price')

        path = os.path.join(self.path, 'fig', 'fig-whole-avg-price.pdf')
        plt.savefig(path)

    def similar_avg_price(self, data1, data2):
        plt.figure()

        days = list(range(1, len(data1) + 1))
        plt.xticks(days)
        
        plt.plot(days, data1, label='R1', marker='o', linestyle='-', color=colors[0])
        plt.plot(days, data2, label='R2', marker='x', linestyle='--', color=colors[2])

        plt.xticks([x for x in days if x % 2 == 0])
        
        plt.legend()
        plt.xlabel('Day')
        plt.ylabel('Avg price')

        path = os.path.join(self.path, 'fig', 'fig-part-avg-price.pdf')
        plt.savefig(path)
        
    def similar_proportion(self, data):
        days = list(range(1, len(data) + 1))
        
        similar = data * 100
        different = 100 - similar  # 'Different' is just 100 minus 'similar'

        # Plotting the stacked bar chart
        plt.figure()
        
        plt.bar(days, similar, color=colors[0], label='Similar')
        plt.bar(days, different, bottom=similar, color=colors[2], label='Different')

        # Adding the legend in the upper left corner
        plt.legend(loc='upper left')

        # Labels and title
        plt.xlabel('Day')
        plt.ylabel('Proportion')

        path = os.path.join(self.path, 'fig', 'fig-ratio.pdf')
        plt.savefig(path)

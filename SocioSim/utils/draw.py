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

        # print(os.getcwd())
        path = os.path.join(self.path, 'fig', 'fig-customer-flow.pdf')
        plt.savefig(path)

    def customer_flow_with_annotate(self, data1, data2):
        plt.figure()

        days = list(range(1, len(data1) + 1))
        plt.xticks(days)
        
        plt.plot(days, data1, label='R1', marker='o', linestyle='-', color=colors[0])
        plt.plot(days, data2, label='R2', marker='x', linestyle='--', color=colors[2])

        plt.xticks([x for x in days if x % 2 == 0])
        
        plt.annotate('Add two dishes using local ingredients', xy=(3, data1[2]), xytext=(4, data1[2]+10),
                     arrowprops=dict(facecolor='black', shrink=0.05),
                     fontsize=12, colors='black')
        
        plt.annotate('Update dishes featuring local ingredients', xy=(4, data2[3]), xytext=(4, data2[2]+10),
                     arrowprops=dict(facecolor='black', shrink=0.05),
                    fontsize=12, colors='black')
        
        plt.annotate('Add American Fusion Bowl', xy=(7, data1[6]), xytext=(4, data1[2]+10),
                     arrowprops=dict(facecolor='black', shrink=0.05),
                     fontsize=12, colors='black')
        
        plt.annotate('Add Stars & Stripes Fusion Bowl', xy=(6, data2[5]), xytext=(4, data2[2]+10),
                     arrowprops=dict(facecolor='black', shrink=0.05),
                    fontsize=12, colors='black')
        
        plt.legend()
        plt.xlabel('Day')
        plt.ylabel('Customer flow')

        # print(os.getcwd())
        path = os.path.join(self.path, 'fig', 'fig-customer-flow-annotate.pdf')
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
        
    def similar_proportion(self, data, stdev=None):
        days = list(range(1, len(data) + 1))
        
        if stdev:
            stdev = [x * 100 for x in stdev]
        similar = [x * 100 for x in data]
        different = [100 - x for x in similar] # 'Different' is just 100 minus 'similar'

        # Plotting the stacked bar chart
        plt.figure()
        
        bar_width = 0.6
        if stdev:
            plt.bar(days, similar, color=colors[0], yerr=stdev, width=bar_width, capsize=2, label='Similar')
        else:
            plt.bar(days, similar, color=colors[0], width=bar_width, label='Similar')
            
        plt.bar(days, different, bottom=similar, color=colors[2], width=bar_width, label='Different')

        # Adding the legend in the upper left corner
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=3)

        # Labels and title
        plt.xlabel('Day')
        plt.ylabel('Proportion')

        path = os.path.join(self.path, 'fig', 'fig-ratio.pdf')
        plt.savefig(path)

    def aggregate_two_line(self, data1, data2, field=None):
        data1 = np.array(data1, dtype=float)
        data2 = np.array(data2, dtype=float)
        
        # 计算每次实验的平均值
        means1 = np.mean(data1, axis=0)
        means2 = np.mean(data2, axis=0)

        # x轴的值，根据实验的参数替换这些值
        days = list(range(1, len(means1) + 1))

        plt.figure(figsize=(10, 5))
        
        # 绘制每次实验的结果
        for i in range(data1.shape[0]):
            plt.plot(days, data1[i, :], color=colors[0], alpha=0.3)  # alpha设置为透明度，以便看到重叠

        for i in range(data2.shape[0]):
            plt.plot(days, data2[i, :], color=colors[2], alpha=0.3)
        
        # 绘制平均曲线，加粗突出
        plt.plot(days, means1, color=colors[0], linewidth=2, label='R1')
        plt.plot(days, means2, color=colors[2], linewidth=2, label='R2')
        
        # 添加图例
        plt.legend()

        # 添加坐标轴标签和标题
        plt.xlabel('Day')
        plt.ylabel(field)
        # plt.title('Aggregate Performance Across Benchmarks')

        path = os.path.join(self.path, 'fig', f'fig-{field}.pdf')
        plt.savefig(path)

    def aggregate_two_line2(self, data1, data2, field=None):
        data1 = np.array(data1, dtype=float)
        data2 = np.array(data2, dtype=float)
        
        # 计算每次实验的平均值
        means1 = np.mean(data1, axis=0)
        means2 = np.mean(data2, axis=0)

        # x轴的值，根据实验的参数替换这些值
        days = list(range(1, len(means1) + 1))

        plt.figure(figsize=(10, 5))
        
        
        # calculate the standard deviation
        stdev1 = np.std(data1, axis=0)
        stdev2 = np.std(data2, axis=0)
        
        # subtract the standard deviation from the mean
        background_start1 = means1 - stdev1
        background_end1 = means1 + stdev1
        background_start2 = means2 - stdev2
        background_end2 = means2 + stdev2
        
        
        plt.fill_between(days, background_start1, background_end1, color=colors[0], alpha=0.3)
        plt.fill_between(days, background_start2, background_end2, color=colors[2], alpha=0.3)
        # 绘制平均曲线，加粗突出
        plt.plot(days, means1, color=colors[0], linewidth=2, label='R1')
        plt.plot(days, means2, color=colors[2], linewidth=2, label='R2')
        
        # 添加图例
        plt.legend()
        
        # 添加坐标轴标签和标题
        plt.xlabel('Day')
        plt.ylabel(field)
        
        path = os.path.join(self.path, 'fig', f'fig-{field}.pdf')
        plt.savefig(path)
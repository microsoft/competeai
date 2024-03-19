# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import os
import scienceplots

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

plt.style.use('science')
colors = sns.color_palette("coolwarm", 6)

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

    def customer_flow_with_annotation(self, data1, data2):
        plt.figure()

        days = list(range(1, len(data1) + 1))
        plt.xticks(days)
        
        plt.plot(days, data1, label='R1', marker='o', linestyle='-', color=colors[0])
        plt.plot(days, data2, label='R2', marker='x', linestyle='--', color=colors[2])

        plt.xticks([x for x in days if x % 2 == 0])
        
        size = 100
        color1 = 'green'
        color2 = '#E1638D'
        marker1 = '*'
        marker2 = '^'
        plt.scatter([2], [data1[1]], marker=marker1, color=color1, s=size, label='Differentiation1: Add two dishes using local ingredients', zorder=5)
        plt.scatter([4], [data2[3]], marker=marker2, color=color1, s=size-20, label='Imitation1: Update dishes featuring local ingredients', zorder=5)
        plt.scatter([5], [data2[4]], marker=marker1, color=color2, s=size, label='Differentiation2: Add \'Stars \& Stripes Fusion Bowl\'', zorder=5)
        plt.scatter([6], [data1[5]], marker=marker2, color=color2, s=size-20, label='Imitation2: Add \'American Fusion Bowl\'', zorder=5)
        
        # day 8 two differentiations
        # day10 r1 imitation
        # day14 r2 differentiation
        # day15 r2 imitation
        color3 = 'grey'
        plt.scatter([8], [data1[7]], marker=marker1, color=color3, s=size, label='Other Differentiations', zorder=5)
        plt.scatter([8], [data2[7]], marker=marker1, color=color3, s=size-20, zorder=5)
        plt.scatter([10], [data1[9]], marker=marker2, color=color3, s=size-20, label='Other Imitations', zorder=5)
        plt.scatter([14], [data2[13]], marker=marker1, color=color3, s=size, zorder=5)
        plt.scatter([15], [data1[14]], marker=marker2, color=color3, s=size-20, zorder=5)
        
        # 创建图例的handles和labels
        handles, labels = plt.gca().get_legend_handles_labels()

        # 首先放置R1和R2的图例
        legend1 = plt.legend(handles[:2], labels[:2], loc='upper center', bbox_to_anchor=(0.7, 0.6),
                            fancybox=True, shadow=True, ncol=1, frameon=False)

        # 将第一个图例添加到图表中（这一步很重要，因为它保证了第一个图例不会被后面的图例覆盖）
        plt.gca().add_artist(legend1)

        new_handles = []
        new_labels = []
        vertical_offset = 0

        for i in range(2, len(handles)):
            new_handles.append(handles[i])
            new_labels.append(labels[i])

        plt.legend(new_handles, new_labels, loc='lower center', bbox_to_anchor=(0.5, -0.85 - vertical_offset),
                fancybox=True, shadow=True, ncol=1, frameon=False)

        # new_handles = []
        # new_labels = []
        # vertical_offset = 0
        
        # for i in range(len(handles)-2, len(handles)):
        #     new_handles.append(handles[i])
        #     new_labels.append(labels[i])
        
        # legend3 = plt.legend(new_handles, new_labels, loc='lower center', bbox_to_anchor=(0.5, -0.8 - vertical_offset),
        #         fancybox=True, shadow=True, ncol=1, frameon=False)
        # plt.gca().add_artist(legend3)

        plt.xlabel('Day', fontsize=12)
        plt.ylabel('Customer flow', fontsize=12)

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
        
        # mean value of similar
        average_similar = np.mean(similar)
        print(average_similar)
        
        # Plotting the stacked bar chart
        plt.figure()
        
        bar_width = 0.6
        if stdev:
            plt.bar(days, similar, color=colors[0], yerr=stdev, width=bar_width, capsize=2, label='Similar')
        else:
            plt.bar(days, similar, color=colors[0], width=bar_width, label='Similar')
            
        plt.bar(days, different, bottom=similar, color=colors[2], width=bar_width, label='Different')

        plt.axhline(y=average_similar, color='green', linestyle='--')
        
        # Adding the legend in the upper left corner
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=3)

        # Labels and title
        plt.xlabel('Day')
        plt.ylabel('Proportion')

        path = os.path.join(self.path, 'fig', 'fig-ratio.pdf')
        plt.savefig(path)

    def choice_percentage(self, data_list, x_name):
        choices = ['Core Needs', 'Brand Loyalty', 'Reputation', 'Affordable', 'Signature Dish', 'Explore New Thing']
        choices_len = len(choices)
        customer_name = x_name
        
        # list 中每个元素也为list, 先将里面的list归一化
        norm_data_list = []
        print(data_list)
        for data in data_list:
            data = np.array(data, dtype=float)
            norm_data = data / sum(data)
            norm_data_list.append(norm_data)

        # 将norm_data_list转为二维向量
        norm_data_list = np.array(norm_data_list)
        print(norm_data_list)
        
        # 将其中每个元素都乘以100，转为百分比
        norm_data_list = norm_data_list * 100
        
        # 现在这个二维的array中有25个子array,现在分成两个二维array,前10个子array一组，后面一组
        array1 = norm_data_list[:10]
        array2 = norm_data_list[10:]
        
        # 对两个array每一列取平均
        mean_array1 = np.mean(array1, axis=0)
        mean_array2 = np.mean(array2, axis=0)
        
        print(mean_array1)
        print(mean_array2)
        
        
        # 每一个data为一柱，每一柱的高度都为1，其中通过data中的比例决定占这个柱子多少高度，将所有data都画图上，形成多个柱子
        # plt.figure(figsize=(6, 3))
        
        # bar_width = 0.6
        # plt.bar(customer_name, norm_data_list[:, 0], color=colors[0], width=bar_width, label='Core Needs')
        
        # for i in range(1, choices_len):
        #     plt.bar(customer_name, norm_data_list[:, i], bottom=np.sum(norm_data_list[:, :i], axis=1), color=colors[i], width=bar_width, label=choices[i])
        
        # plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.3), ncol=3)
        
        # plt.xticks(rotation=45)
        # plt.xlabel('Customer Name / Group Id', fontsize=12)
        # plt.ylabel('Percentage (\%)', fontsize=12)
        
        # path = os.path.join(self.path, 'fig', 'fig-choice-percentage.pdf')
        # plt.savefig(path)
        
    def aggregate_two_line(self, data1, data2, field=None):
        data1 = np.array(data1, dtype=float)
        data2 = np.array(data2, dtype=float)

        
        # 计算每次实验的平均值
        means1 = np.mean(data1, axis=0)
        means2 = np.mean(data2, axis=0)

        # x轴的值，根据实验的参数替换这些值
        days = list(range(1, len(means1) + 1))

        plt.figure()
        
        # 绘制每次实验的结果
        # for i in range(data1.shape[0]):
        #     plt.plot(days, norm_data1[i, :], color=colors[0], alpha=0.3)  # alpha设置为透明度，以便看到重叠

        # for i in range(data2.shape[0]):
        #     plt.plot(days, norm_data2[i, :], color=colors[2], alpha=0.3)
        
        # 绘制平均曲线，加粗突出
        plt.plot(days, means1, label='R1', marker='o', linestyle='-', color=colors[0])
        plt.plot(days, means2, label='R2', marker='x', linestyle='--', color=colors[2])
        
        plt.xticks([x for x in days if x % 2 == 0])
        
        # 添加图例
        plt.legend()

        # 添加坐标轴标签和标题
        plt.xlabel('Day')
        plt.ylabel('Avg score of dishes')
        # plt.title('Aggregate Performance Across Benchmarks')

        path = os.path.join(self.path, 'fig', f'fig-{field}.pdf')
        plt.savefig(path)

    def aggregate_two_line2(self, data1, data2, field=None):
        data1 = np.array(data1, dtype=float)
        data2 = np.array(data2, dtype=float)
        
        # 计算每次实验的平均值
        means1 = np.mean(data1, axis=0)
        means2 = np.mean(data2, axis=0)
        
    

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
        
    def customer_flow_and_score(self, data1, data2, data3, data4):
        plt.figure()

        days = list(range(1, len(data1) + 1))
        plt.xticks(days)

        # Plot the first set of data
        plt.plot(days, data1, label='R1', marker='o', linestyle='-', color=colors[0])
        plt.plot(days, data2, label='R2', marker='x', linestyle='--', color=colors[2])

        # Create a twin Axes sharing the xaxis
        ax2 = plt.gca().twinx()

        # Plot the second set of data on the twin Axes
        ax2.plot(days, data3, label='Score1', marker='s', linestyle='-', color=colors[0])
        ax2.plot(days, data4, label='Score2', marker='^', linestyle='--', color=colors[2])

        # Set ticks for the twin Axes
        ax2_ticks = [x for x in days if x % 2 == 0]
        ax2.set_xticks(ax2_ticks)
        ax2.set_xticklabels([])  # Hide tick labels on the top x-axis

        # Set labels for the twin Axes
        ax2.set_ylabel('Scores')
        ax2.set_ylim(1, 10)
        
        # Combine legends for both axes
        lines, labels = plt.gca().get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        plt.legend(lines + lines2, labels + labels2, loc='upper left')

        # Set labels for the main Axes
        plt.xlabel('Day')
        plt.ylabel('Customer flow')

        # Save the figure
        path = os.path.join(self.path, 'fig', 'fig-customer-flow.pdf')
        plt.savefig(path)
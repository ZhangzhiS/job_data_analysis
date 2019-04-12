#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-
# @Author   : zhi
# @Time     : 2019/4/11 下午6:51
# @Filename : data_analysis
# @Software : PyCharm

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from matplotlib import cm
import jieba
from wordcloud import WordCloud, ImageColorGenerator
import PIL.Image as Image

plt.style.use('ggplot')

"""
如果生成的统计图的中文无法正常显示,运行tools中的get_zh_fonts()函数，
获取可用的中文字体，替换下面的'Droid Sans Fallback'
"""
plt.rcParams['font.sans-serif'] = ['Droid Sans Fallback']  # 指定中文字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题


class DataCount(object):
    """数据统计, 进行绘图"""

    def __init__(self, path):
        self.data_frame = pd.read_csv(path)
        self.city_list = list(set(self.data_frame["job_city"]))

    def generate_max_and_min_wage(self):
        """生成薪资最大和最小的表"""
        # 根据”-“连接符分割薪资字段
        min_wage, max_wage = self.data_frame.loc[:, "wage_range"].str.split('-',1).str
        # 生成最大和最小的数据表
        df_min = self.generate_columns_data(min_wage, "min_wage")
        df_max = self.generate_columns_data(max_wage, "max_wage")
        # 合并多个数组
        df_clean_concat = pd.concat([self.data_frame, df_min, df_max], axis=1)
        df_clean_concat['min_wage'] = pd.to_numeric(df_clean_concat['min_wage'])
        df_clean_concat['max_wage'] = pd.to_numeric(df_clean_concat['max_wage'])
        df_clean_concat.sort_values('min_wage', inplace=True)
        # print(df_clean_concat)
        return df_clean_concat

    def generate_columns_data(self, initial_data, columns_name):
        """生成数据列"""
        data_frame = pd.DataFrame(initial_data)
        data_frame.columns = [columns_name]
        # 将薪资字段中存在的 “k”、“·13薪” 等字段替换
        data_frame[columns_name] = data_frame[columns_name].replace("k"+".*", "", regex=True)
        return data_frame

    def city_count(self):
        """统计各城市的职位情况， 生成对应的数据表"""
        # 根据工作所在的城市进行统计
        city_job_count = self.data_frame.groupby('job_city')['job_name','company_name'].count()
        # 计算职位所占百分比
        city_job_count['company_name'] = city_job_count['company_name'] / (city_job_count['company_name'].sum())
        city_job_count.columns = ['number', 'percentage']
        # 根据职位数目倒序
        city_job_count.sort_values(by='number', ascending=False, inplace=True)
        # 根据百分比增加标签页
        city_job_count["label"] = city_job_count.index+ ' '+  ((city_job_count['percentage']*100).round()).astype('int').astype('str')+'%'
        return city_job_count

    def draw_pie_graph(self, data_frame):
        """绘制饼图"""
        label = data_frame["label"]
        number = data_frame["number"]
        # 创建一个图像对象和子图
        fig, axes = plt.subplots(figsize=(10, 6), ncols=2)
        # 创建两个子图
        ax1, ax2 = axes.ravel()
        # 设置颜色
        colors = cm.RdBu(np.arange(len(number))/len(number))
        # 生成图片
        ax1.axis('equal')
        ax1.set_title('职位分布', loc='center')
        patches, texts = ax1.pie(number, labels=None, shadow=False, startangle=0, colors=colors)
        # 图例
        ax2.axis('off')
        ax2.legend(patches, label, loc='center left', fontsize=8)
        # 保存 支持eps, pdf, pgf, png, ps, raw, rgba, svg, svgz等格式
        plt.savefig('job_distribute.png')
        # 展示图片
        # plt.show()

    def wage_distribution(self, data_frame):
        x_pos = list(range(data_frame.shape[0]))
        # 底薪列
        y_axis = data_frame['min_wage']
        fig, (ax1, ax2) = plt.subplots(figsize=(10, 8), nrows=2)
        # 设置xy轴
        ax1.plot(x_pos, y_axis)
        # 设置标题
        ax1.set_title('最低月薪工资趋势', size=14)
        # 设置x轴刻度标签
        # ax1.set_xticklabels('')
        # 设置y轴的标签
        ax1.set_ylabel('最低月薪/k')
        # x轴薪分布刻度
        bins = range(1, 41)

        counts, bins, patches = ax2.hist(y_axis, bins,  density=1, histtype='bar', facecolor='g', rwidth=0.8)
        ax2.set_title('最低月薪柱图', size=14)
        ax2.set_xlabel('月薪/k')
        # 设置x轴要显示的刻度
        ax2.set_xticks(bins)  # 将bins设置为xticks
        # 设置x轴刻度标签
        ax2.set_xticklabels(bins)  # 设置为xticklabels的方向
        #
        # 标记原始计数和x轴以下的百分比
        bin_centers = 0.5 * np.diff(bins) + bins[:-1]
        # print(bin_centers)
        for count, x in zip(counts, bin_centers):
            # 计算百分比
            percent = '%0.0f%%' % (100 * float(count) / counts.sum())
            ax2.annotate(percent, xy=(x, 0), xycoords=('data', 'axes fraction'),
                         xytext=(0, -40), textcoords='offset points', va='top', ha='center', color='b',
                         size=10, rotation=-90)

        fig.savefig('salary_quanguo_min.png')

    def create_jd_str(self):
        jd_list = self.data_frame["jd"]
        jd_str = "".join(jd_list)
        # 写入文件中
        with open("jd.txt", "w", encoding="UTF-8") as fd:
            fd.write(jd_str)
        return jd_str


if __name__ == '__main__':
    df = DataCount("../data/data.csv")
    cdf = df.city_count()
    df.create_jd_str()
    # df.draw_pie_graph(cdf)
    # wd = df.get_max_and_min_wage()
    # df.wage_distribution(wd)

#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-
# @Author   : zhi
# @Time     : 2019/4/12 下午1:45
# @Filename : generate_word_cloud
# @Software : PyCharm
from wordcloud import WordCloud
import jieba
import numpy as np
import PIL.Image as img

class GenerateWordCloud(object):

    def read_file(self, path: str) -> str:
        """
        读取文件
        :param path: 文件路径
        :return:  内容
        """
        with open(path, "r") as rd:
            text_count = rd.read()
        return text_count

    def word_segmentation(self, txt_content: str) -> list:
        """
        文本分词，使用jieba库的词性分词，保留文本中的名词(n)，人名(nr)，地名(ns)

        :param txt_content: 文本内容
        :return: 分词之后的列表
        """
        word_list = jieba.cut(txt_content)
        return word_list


    def word_frequency_count(self, word_list: list) -> list:
        """
        生成词频的哈希表
        :param word_list: 文本分词之后的列表
        :return: 词频排序之后的列表
        """

        word_frequency = {}
        for word in word_list:
            if word in word_frequency:
                word_frequency[word] += 1
            else:
                word_frequency[word] = 1
        # 将结果按照出现的频率排序
        sorted_word_frequency = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)
        return sorted_word_frequency

    def create_world_cloud(self, name: str, text: str) -> None:
        """
        生成图云

        :param name: 文件名
        :param text: 要生成图云的文本
        """
        mask = np.array(img.open("../data/job.png"))
        word_cloud = WordCloud(
            mask=mask,
            font_path="../data/simhei.ttf",
            width=1920,
            height=1080,
            scale=4
            # background_color="white"
        ).generate(text)
        word_cloud.to_file("../data/%s.jpg" % name)

if __name__ == '__main__':
    jd_path = "jd.txt"
    gwc = GenerateWordCloud()
    jd_str = gwc.read_file(jd_path)
    word_list = gwc.word_segmentation(jd_str)
    sorted_word_frequency = gwc.word_frequency_count(word_list)
    word_content = " ".join([x[0] for x in sorted_word_frequency])
    gwc.create_world_cloud("jd", word_content)



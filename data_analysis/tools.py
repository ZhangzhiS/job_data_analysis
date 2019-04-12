#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-
# @Author   : zhi
# @Time     : 2019/4/11 下午11:36
# @Filename : tools
# @Software : PyCharm

from matplotlib.font_manager import FontManager
import subprocess


def get_zh_fonts():
    """获取可用的中文字体"""
    font_manger = FontManager()
    mat_fonts = set(f.name for f in font_manger.ttflist)
    # print(mat_fonts)
    output = subprocess.check_output('fc-list :lang=zh -f "%{family}\n"', shell=True)
    # print(output)
    zh_fonts = set(f.split(',', 1)[0] for f in output.decode('utf-8').split('\n'))
    available = mat_fonts & zh_fonts
    # print('*' * 10, '可用的字体', '*' * 10)
    for f in available:
        print(f)


if __name__ == '__main__':
    get_zh_fonts()
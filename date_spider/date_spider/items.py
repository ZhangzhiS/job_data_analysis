# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DateSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    job_name = scrapy.Field()  # 职位名称
    wage_range = scrapy.Field()  # 薪资范围
    job_city = scrapy.Field()  # 公司所在城市
    work_time = scrapy.Field()  # 工作经验
    educational = scrapy.Field()  # 学历要求
    jd = scrapy.Field()  # 职位描述
    company_name = scrapy.Field()  # 职位名称
    industry = scrapy.Field()  # 行业
    staged_financing = scrapy.Field()  # 融资阶段
    staff_num = scrapy.Field()  # 公司规模

# -*- coding: utf-8 -*-
import scrapy
import time

from date_spider.items import DateSpiderItem


class ExampleSpider(scrapy.Spider):
    name = 'boss_job'
    allowed_domains = ['zhipin.com']
    start_urls = ['https://www.zhipin.com/c101010100/?query=python&period=5&ka=sel-scale-5']

    def start_requests(self):
        """起始链接"""
        url = "https://www.zhipin.com/job_detail/?query=python&city=100010000&industry=&position="
        yield scrapy.Request(
            url=url,
            callback=self.select_city
        )

    def select_city(self, response):
        city_doc = response.css("dd.city-wrapper")
        """//*[@id="filter-box"]/div/div[2]/dl[1]/dd/a[4]"""
        city_list = city_doc.xpath("a")
        # print(city_list)
        for item in city_list:
            path = item.xpath("@href").extract()[0]
            if "javascr" in path:
                pass
            else:
                url_lisu = create_url(path)
                for url in url_lisu:
                    yield scrapy.Request(
                        url=url,
                        callback=self.parse,
                    )
                    time.sleep(2)

    def parse(self, response):
        job_items = response.css("div.job-primary")
        if job_items:
            for job_item in job_items:
                job_info = job_item.xpath('div[1]/h3/a')
                job_url = job_info.xpath("@href").extract()[0]
                ka = job_info.xpath("@ka").extract()[0]
                lid = job_info.xpath("@data-lid").extract()[0]
                url = create_job_url(job_url, ka, lid)
                yield scrapy.Request(
                    url=url,
                    callback=self.get_jd
                )

    def get_jd(self, response):
        """解析jd页面数据"""
        job_name = response.xpath('//*[@id="main"]/div[1]/div/div/div[2]/div[2]/h1/text()').extract()
        wage_range = response.xpath('//*[@id="main"]/div[1]/div/div/div[2]/div[2]/span/text()').extract()[0]
        wage_range = wage_range.replace(" ", '').replace("\n", '')
        job_claim = response.xpath('//*[@id="main"]/div[1]/div/div/div[2]/p/text()').extract()
        job_city = job_claim[0]  # 公司地址
        work_time = job_claim[1]  # 工作经验
        educational = job_claim[2]  # 学历要求
        job_detail_item = response.css("div.job-detail")
        jd = job_detail_item.xpath("div[2]/div[1]/div/text()").extract()
        jd = "".join(jd).replace(" ", '').replace("\n", '')

        company_info = response.css("div.sider-company")

        company_name = company_info.xpath("div/a[1]/@title").extract()[0]
        company_name = company_name.replace(" ", '').replace("\n", "")
        industry = company_info.xpath("p[4]/a/text()").extract()  # 行业
        staged_financing = company_info.xpath("p[2]/text()").extract()  # 融资阶段
        staff_num = company_info.xpath("p[3]/text()").extract()  # 公司规模

        item = DateSpiderItem()
        item["job_name"] = job_name[0]
        item["wage_range"] = wage_range
        item["job_city"] = job_city
        item["work_time"] = work_time
        item["educational"] = educational
        item["jd"] = jd
        item["company_name"] = company_name
        item["industry"] = industry[0]
        item["staged_financing"] = staged_financing[0]
        item["staff_num"] = staff_num[0]
        yield item



def create_job_url(job_url, ka, lid):
    """生成跳转到jd的链接"""
    url = "https://www.zhipin.com{job_url}?ka={ka}&lid={lid}"
    url = url.format(job_url=job_url, ka=ka, lid=lid)
    return url


def create_url(path):
    """生成各个城市的链接"""
    url_list = []
    for i in range(1,11):
        url = "https://www.zhipin.com{path}&page={page}&ka=page-{page}"
        url = url.format(path=path, page=i)
        url_list.append(url)
    return url_list


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute("scrapy crawl boss_job".split())

## 求职之路

最近在求一份Python开发的工作，但是简历投出去都是石沉大海，写个小爬虫抓取一下Boss上面的招聘信息，统计分析一下。

#### 描述
抓取了Boss直聘热门城市的Python岗位， 对职位进行了简单的统计制图， 分析每个职位的jd，根据词汇的频率生成了图云。

#### 相关依赖
> jieba==0.39\
numpy==1.16.2\
pandas==0.24.2\
pillow==6.0.0\
wordcloud==1.5.0\
matplotlib==3.0.3

- 职位分布情况
可以看出北京职位还是最多的，不过根据爬到的数据看，有职位350左右，因为Boss的页面最多十页，而且也只是在Boss上面的数据。
北上广深占了差不多75%。

![job_distribute.png](https://github.com/ZhangzhiS/job_data_analysis/blob/master/data/job_distribute.png?raw=true)

- 最低薪资
薪资分析的话，只分析了最低薪资，都寒冬了，还要啥自行车。

![salary_quanguo_min.png](https://github.com/ZhangzhiS/job_data_analysis/blob/master/data/salary_quanguo_min.png?raw=true)

- 职位描述
根据职位描述中出现的词语生成的图云，我所有的职位都是根据Python搜索的，但是出现最多的词汇是MYSQL？

![job.png](https://github.com/ZhangzhiS/job_data_analysis/blob/master/data/jd.jpg?raw=true)


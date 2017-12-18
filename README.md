# LagouDataAnalysis
拉勾数据分析前的数据预处理

@2017.12.18
###目前实现的功能如下：
1、获取到岗位关键字的对应页数(不局限于官网的30页)
2、多进程处理任务
3、将相应关键字的职位列表信息存入mysql数据库

###目前未实现的功能：
1、获取职位信息的详情
2、数据可视化

###遇到的问题
1、爬取详情页面时，使用host:www.lagou.com爬取5个后，下一个请求报404
2、爬取详情页面时，使用host:m.lagou.com爬取10个后，下一个请求报需要登录

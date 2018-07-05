# -*- coding: utf-8 -*-
import scrapy
from pypinyin import pinyin , lazy_pinyin
from scrapy.selector import Selector
from company_ifo_spider.items import BafangItem
import re


class BafangSpiderSpider(scrapy.Spider):
    '''
    本爬虫为八方资源网企业工商信息爬虫，使用方法是在项目目录（company_ifo_spider）下，
    打开命令提示符，输入一下命令：
    scrapy crawl bafang_spider -a keyword=k
    其中，k是用户设置的关键词，是用户爬取的行业关键词，例如：铜箔
    '''
    name = 'bafang_spider'

    start_urls = ['http://www.b2b168.com/']

    def __init__(self , keyword=None , *args , **kwargs):#keyword为用户通过命令行输入的中文关键词
            super(BafangSpiderSpider , self).__init__(*args , **kwargs)
            print('*********************启动爬虫**************************')
            self.keyword = ''.join(lazy_pinyin(keyword))
            self.start_urls = ['https://www.b2b168.com/k-' + self.keyword + '/']
            print(self.start_urls)
            self.allowed_domains = []
    def parse(self, response):
        '''
        本方法主要作用是获取下一页一级公司列表页面，以及当前页面中所包含的所有公司链接
        :param response:
        :return:
        '''

        try:
            data_link = Selector(response).re(r'<a class="list-item-title-text" title="[\s\S]*?</a>')
            for string in data_link:
                link = self.txt_wrap_by('href="', '">', string)
                company_url = link + '/home.aspx'
                print('当前链接：{}'.format(company_url))
                #进一步爬取企业信息详情页面
                #八方资源网的企业信息详情页有两种，两种页面的数据拜访不一样，所以要用不同的方法来提取
                if not 'b2b168.com/c168' in link:#如果网址中不存在这几个字符则是第一类网页
                    yield scrapy.Request(url=company_url, callback=self.parse_first_type_company_web)
                else:#网址中存在这几个字符就是第二类网页
                    yield scrapy.Request(url=company_url, callback=self.parse_second_type_company_web)

        except Exception as e:
            print('抓取搜索结果中企业链接列表时发生异常：{}-->{}'.format(e,response.url))

        next_page = response.xpath('//ul[@class="page"]/a[last()]/@href').extract()[0]
        next_page_url = 'https://www.b2b168.com' + next_page
        print('************下一页：************'+next_page_url)
        yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_first_type_company_web(self,response):
        '''
        对第一种类型的企业网站进行数据抓取
        :param response:
        :return:
        '''
        try:
            item = BafangItem()
            company_name = Selector(response).re(r'<li class="fl">.*?</li>')
            if company_name:#如果有企业名称，则对企业名称进行处理
                company_name = company_name[0].strip('<li class="fl">').strip('</li>')
                print('企业名称---->{}'.format(company_name))
            else:#如果没有企业名称，退出函数，直接返回
                print('没有企业名称-------->{}'.format(response.url))
                return None
            company_description = Selector(response).re(r'<pre>[\s\S]*</pre>')
            if company_description:#如果有详细信息描述，则对信息进行处理
                company_description = company_description[0].strip('<pre>').strip('</pre>').replace('\r\n','')
            else:#没有详细信息描述，令详细信息为空
                company_description = ''
            data_attr = Selector(response).re(r'class="table b">.*?</td>')
            data_value = Selector(response).re(r'class="table1">[\s\S]*?</td>')
            if not (data_attr and data_value):#如果没有抓取到企业信息，直接退出函数，返回-1
                print('没有企业详细信息****************')
                return None
            item['company_web_url'] = response.url#企业网址
            item['company_description']=company_description#企业描述
            item['company_name'] = company_name#企业名称
            item['economic_nature'] = data_value[0][15:-5]#企业经济性质
            item['legal_representative'] = data_value[1][15:-5]#法人代表或负责人
            item['company_type'] = data_value[2][15:-5]#企业类型
            item['registered_site'] = data_value[3][15:-5]#公司注册地
            item['registered_capital'] = data_value[4][15:-5]#注册资金
            item['establish_time'] = data_value[5][15:-5]#成立时间
            item['employees_number'] = data_value[6][15:-5]# 员工数量
            item['monthly_production'] = data_value[7][15:-5]#月产量
            item['annual_turnover'] = data_value[8][15:-5]#年营业额
            item['annual_export_volume'] = data_value[9][15:-5]#年出口额
            item['certification'] = data_value[10][15:-5]#管理体系认证
            item['main_operating_place'] = data_value[11][15:-5]#主要营业地点
            item['main_customer'] = data_value[12][15:-5]#主要客户
            item['workshop_area'] = data_value[13][15:-5]# 厂房面积
            item['provide_OEM'] = data_value[14][15:-5]#provide OEM
            item['bank'] = data_value[15][15:-5]#开户银行
            item['bank_account'] = data_value[16][15:-5]#银行帐号
            item['main_market'] = data_value[17][15:-5]#主要市场
            item['main_products'] = data_value[18][15:-5]#主营产品或服务
            yield item
        except Exception as e :
            print(e.__context__)
            print('抓取信息时发生异常：{}-->url：{}'.format(e,response.url))
            return None

    def parse_second_type_company_web(self,response):
        '''
        对第一种类型的企业网站进行数据抓取
        :param response:
        :return:
        '''
        try:
            item = BafangItem()
            company_name = Selector(response).re(r'<ul class="company">[\s\S]*?</ul>')
            if company_name:#如果有企业名称，则对企业名称进行处理
                company_name = company_name[0].strip('<ul class="company">').strip('</ul>')

            else:#如果没有企业名称，退出函数，直接返回--1
                return None
                '''
                !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                以下两行代码是到目前为止还没有搞清楚的bug问题，下面两行代码提取出来的内容只有
            <ul class="Cgsjj">\r\n</ul>，而其他真正的中文文本全被没有，但是print（response.text）
            出来的结果证明，爬取出来的网页源代码中是包含中文文本的。所以后续只能改成用re.findall()
            方法来提取数据。
                '''
            # company_description = Selector(response).re(r'<ul class="Cgsjj">[\w\W]*?</ul>')
            # company_description = response.xpath('//ul[@class="Cgsjj"]').extract()
            company_description = re.findall(r'<ul class="Cgsjj">[\w\W]*?</ul>', response.text)
            print('************************')
            if company_description:#如果有详细信息描述，则对信息进行处理
                company_description = company_description[0]
                delete_str = re.findall(r'<[\s\S]*?>', company_description)
                for string in delete_str:
                    company_description = company_description.replace(string , '')
                company_description = company_description.replace('\n' , '')
            else:#没有详细信息描述，令详细信息为空
                company_description = ''
            print(company_name)
            print(company_description)
            item['company_description']=company_description
            item['company_name'] = company_name
            data_attr = re.findall('<th[\S\s]*?</th>', response.text)
            data_value = re.findall('<td[\S\s]*?</td>', response.text)
            print('**************************{}'.format(len(data_attr)))
            if not (data_attr and data_value):#如果没有抓取到企业信息，直接退出函数，返回-1
                return None
            item['company_web_url'] = response.url#企业网址
            item['company_name'] = company_name#企业名称
            item['company_description']=company_description#企业描述
            item['economic_nature'] = self.txt_wrap_by('>', '<', data_value[0])#企业经济性质
            item['legal_representative'] = self.txt_wrap_by('>', '<', data_value[1])#法人代表或负责人
            item['company_type'] = self.txt_wrap_by('>', '<', data_value[2])#企业类型
            item['registered_site'] = self.txt_wrap_by('>', '<', data_value[3])#公司注册地
            item['registered_capital'] = self.txt_wrap_by('>', '<', data_value[4])#注册资金
            item['establish_time'] = self.txt_wrap_by('>', '<', data_value[5])#成立时间
            item['employees_number'] = self.txt_wrap_by('>', '<', data_value[6])# 员工数量
            item['monthly_production'] = self.txt_wrap_by('>', '<', data_value[7])
            item['annual_turnover'] = self.txt_wrap_by('>', '<', data_value[8])#年营业额
            item['annual_export_volume'] = self.txt_wrap_by('>', '<', data_value[9])#年出口额
            item['certification'] = self.txt_wrap_by('>', '<', data_value[10])#管理体系认证
            item['main_operating_place'] = self.txt_wrap_by('>', '<', data_value[11])#主要营业地点
            item['main_customer'] = self.txt_wrap_by('>', '<', data_value[12])#主要客户
            item['workshop_area'] = self.txt_wrap_by('>', '<', data_value[13])# 厂房面积
            item['provide_OEM'] = self.txt_wrap_by('>', '<', data_value[14])#provide OEM
            item['bank'] = self.txt_wrap_by('>', '<', data_value[15])#开户银行
            item['bank_account'] = self.txt_wrap_by('>', '<', data_value[16])#银行帐号
            item['main_market'] = self.txt_wrap_by('>', '<', data_value[17])#主要市场
            item['main_products'] = self.txt_wrap_by('>', '<', data_value[18])#主营产品或服务
            #事实上，在八方资源网有的企业信息详情页有更多的数据，就是说data_attr和data_value长度不止19（不包含企业名称和描述）,
            # 但是有的却只有19所以在这里只取前面19个数据，因为19以后的数据有些包含在了前面19中
            yield item
        except Exception as e :
            print('抓取信息时发生异常：{}-->url：{}'.format(e,response.url))
            return None

    def txt_wrap_by(self , start_str, end_str, html):
        '''
        获取html里面在start_str与end_str之间的字符
        :param start_str:
        :param end_str:
        :param html:
        :return:
        '''
        start = html.find(start_str)
        if start >= 0:
            start += len(start_str)
            end = html.find(end_str, start)
            if end >= 0:
                return html[start:end].strip()

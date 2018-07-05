# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import csv

class CompanyIfoSpiderPipeline(object):
    def __init__(self):
        self.file_path = 'data.csv'
        self.dict_key = ['企业名称' , '企业描述' , '企业经济性质' , '法人代表或负责人' , '企业类型' , '公司注册地' , '注册资金' , '成立时间' , ' 员工数量' , '月产量' , '年营业额' , '年出口额' , '管理体系认证' , '主要营业地点' , '主要客户' , ' 厂房面积' , '是否提供OEM' , '开户银行' , '银行帐号' , '主要市场' , '主营产品或服务' , '企业网站链接' ]
        if not os.path.exists(self.file_path):#若是存放数据的文件不存在，那么就要写入第一行的表头
            self.file = open(self.file_path,'a',encoding='utf-8' , newline='')
            self.w=csv.writer(self.file)
            self.w.writerow(self.dict_key)#写入表头
        else:
            self.file = open(self.file_path,'a',encoding='utf-8' , newline='')
            self.w=csv.writer(self.file)
    def process_item(self, item, spider):
        print('****************管道文件运行******************')
        dict_values = [
            item['company_name'] ,
            item['company_description'] ,
            item['economic_nature'] ,
            item['legal_representative'] ,
            item['company_type'] ,
            item['registered_site'] ,
            item['registered_capital'] ,
            item['establish_time'] ,
            item['employees_number'] ,
            item['monthly_production'] ,
            item['annual_turnover'] ,
            item['annual_export_volume'] ,
            item['certification'] ,
            item['main_operating_place'] ,
            item['main_customer'] ,
            item['workshop_area'] ,
            item['provide_OEM'] ,
            item['bank'] ,
            item['bank_account'] ,
            item['main_market'] ,
            item['main_products'] ,
            item['company_web_url']]

        self.w.writerow(dict_values)#写入数据
        return item

    def close_spider(self , spider):
        print('**********************关闭爬虫**********************')
        self.file.flush()
        self.file.close()
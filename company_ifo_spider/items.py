# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BafangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    company_name = scrapy.Field()#企业名称
    company_description = scrapy.Field()#企业描述
    economic_nature = scrapy.Field()#企业经济性质
    legal_representative = scrapy.Field()#法人代表或负责人
    company_type = scrapy.Field()#企业类型
    registered_site = scrapy.Field()#公司注册地
    registered_capital = scrapy.Field()#注册资金
    establish_time = scrapy.Field()#成立时间
    employees_number = scrapy.Field()# 员工数量
    monthly_production = scrapy.Field()#月产量
    annual_turnover = scrapy.Field()#年营业额
    annual_export_volume = scrapy.Field()#年出口额
    certification = scrapy.Field()#管理体系认证
    main_operating_place = scrapy.Field()#主要营业地点
    main_customer = scrapy.Field()#主要客户
    workshop_area = scrapy.Field()# 厂房面积
    provide_OEM = scrapy.Field()#provide OEM
    bank = scrapy.Field()#开户银行
    bank_account = scrapy.Field()#银行帐号
    main_market = scrapy.Field()#主要市场
    main_products = scrapy.Field()#主营产品或服务

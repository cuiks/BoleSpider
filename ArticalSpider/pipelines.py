# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from ArticalSpider.models.es_model import ArticleType
from w3lib.html import remove_tags


class ArticalspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class EsPipline(object):
    # 用于保存数据到ElasticSearch
    def process_item(self, item, spider):
        # 首先装换item数据为es储存格式
        item.save_es()
        return item

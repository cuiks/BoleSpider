# -*- coding: utf-8 -*-
import time

import scrapy
from scrapy.http import Request
from urllib import parse
from scrapy.loader import ItemLoader

from ArticalSpider.items import JobboleArticlrItem, JobboleItemLoader
from ArticalSpider.utils.commend import get_md5


class JobjoleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        print(response.url)
        urls = response.css("#archive .floated-thumb .post-thumb a")
        for url in urls:
            image_url = url.css("img::attr(src)").extract_first("")
            post_url = url.css("::attr(href)").extract_first("")
            post_url = parse.urljoin(response.url, post_url)
            yield Request(url=post_url, callback=self.articleParse,
                          meta={'image_url': image_url})
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(url=next_url, callback=self.parse)

    def articleParse(self, response):
        image_url = response.meta.get("image_url", "")  # 文章封面图
        item_loader = JobboleItemLoader(item=JobboleArticlrItem(), response=response)
        item_loader.add_css("title", ".entry-header h1::text")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("create_time", "p.entry-meta-hide-on-mobile::text")
        item_loader.add_value("image_url", [image_url])
        item_loader.add_css("praise_nums", ".vote-post-up h10::text")
        item_loader.add_css("comment_nums", "a[href='#article-comment'] span::text")
        item_loader.add_css("fav_nums", ".bookmark-btn::text")
        item_loader.add_css("tags", "p.entry-meta-hide-on-mobile a::text")
        item_loader.add_css("content", "div.entry")
        article_item = item_loader.load_item()
        yield article_item

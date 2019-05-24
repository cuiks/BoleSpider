# -*- coding: utf-8 -*-
import time

import scrapy
from scrapy.http import Request
from urllib import parse
from scrapy.loader import ItemLoader

from ArticalSpider.items import JobboleArticlrItem
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
                          meta={'image_url': image_url, 'post_url': post_url})
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(url=next_url, callback=self.parse)

    def articleParse(self, response):
        article_item = JobboleArticlrItem()
        image_url = response.meta.get('image_url', '')
        post_url = response.meta.get('post_url', '')
        title = response.css('#wrapper > div.grid-8 > div.post > div.entry-header > h1::text').extract_first()
        create_time = response.css('#wrapper > div.grid-8 > div.post > div.entry-meta '
                                   '> p::text').extract_first("2019-01-01").strip().rstrip(' ·')
        # 点赞数
        praise_nums = response.css('#wrapper > div.grid-8 > div.post > div.entry > div.post-adds '
                                   '> span.vote-post-up > h10::text').extract_first('0')
        # 收藏数
        fav_nums = response.css('#wrapper > div.grid-8 > div.post > div.entry > div.post-adds '
                                '> span.bookmark-btn::text').extract_first()
        fav_nums = fav_nums.replace(' ', '').replace('收藏', '')
        fav_nums = fav_nums if fav_nums else '0'
        # 评论数
        comment_nums = response.css('#wrapper > div.grid-8 > div.post > div.entry > div.post-adds '
                                    '> a >span::text').extract_first()
        comment_nums = comment_nums.replace(' ', '').replace('评论', '')
        comment_nums = comment_nums if comment_nums else '0'
        content = response.css('#wrapper > div.grid-8 > div.post > div.entry').extract_first('')
        element = response.css('#wrapper > div.grid-8 > div.post > div.entry-meta '
                               '> p.entry-meta-hide-on-mobile > a::text').extract()
        tags = [element_item for element_item in element if not '评论' in element_item]
        # ItemLoader解析
        # item_loader = ItemLoader(item=JobboleArticlrItem(),response=response)
        article_item['title'] = title
        article_item['create_time'] = create_time
        article_item['url'] = post_url
        article_item['url_object_id'] = get_md5(post_url)
        article_item['front_image_url'] = image_url
        article_item['praise_nums'] = praise_nums
        article_item['comment_nums'] = comment_nums
        article_item['content'] = content
        article_item['tags'] = tags
        article_item['fav_nums'] = fav_nums

        yield article_item

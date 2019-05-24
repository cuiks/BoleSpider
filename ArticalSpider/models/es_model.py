# -*- coding: utf-8 -*-

from elasticsearch_dsl import DocType, Text, Date, Keyword, Integer, Completion
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer

connections.create_connection(hosts=["192.168.62.140"])


class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}


ik_analyzer = CustomAnalyzer("ik_max_word", filter=["lowercase"])


class ArticleType(DocType):
    # item字段映射
    title = Text(analyzer="ik_max_word")
    create_time = Date()
    url = Keyword()
    url_object_id = Keyword()
    front_image_url = Keyword()
    front_image_path = Keyword()
    praise_nums = Integer()
    fav_nums = Integer()
    comment_nums = Integer()
    content = Text(analyzer="ik_max_word")
    tags = Text(analyzer="ik_max_word")
    suggest = Completion(analyzer=ik_analyzer)

    class Meta:
        index = "jobbole"
        doc_type = "article"


if __name__ == '__main__':
    ArticleType.init()

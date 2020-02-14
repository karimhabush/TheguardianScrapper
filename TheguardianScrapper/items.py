import scrapy

class ArticleItem(scrapy.Item):
    author = scrapy.Field()
    headline = scrapy.Field()
    content = scrapy.Field()
    standfirst = scrapy.Field()
    label = scrapy.Field()
    url = scrapy.Field()
    published_at = scrapy.Field()


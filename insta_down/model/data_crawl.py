from djongo import models


class ItemCrawl(models.Model):
    id = models.IntegerField(primary_key=True)
    # url of pic
    url = models.TextField()
    # thumbnail of pic (if list choose size minimum)
    thumbnail_url = models.TextField()
    # count comment of pic
    count_comment = models.IntegerField()
    # count like of pic
    count_like = models.IntegerField()
    # short-code of pic
    shortcode = models.TextField()


class Owner(models.Model):
    # id user
    id = models.IntegerField(primary_key=True)
    # avatar user
    avatar = models.TextField()
    # username user
    name = models.TextField()


class DataCrawl(models.Model):
    # id userId or post short-code
    id = models.IntegerField(primary_key=True)
    # info of owner
    owner = models.EmbeddedField(Owner)
    # list data crawl
    data = models.ArrayField(ItemCrawl)

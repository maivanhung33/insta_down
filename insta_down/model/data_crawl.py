from djongo import models


class ItemCrawl(models.Model):
    id = models.TextField(primary_key=True)
    # url of pic
    url = models.TextField()
    height = models.IntegerField()
    width = models.IntegerField()
    # thumbnail of pic (if list choose size minimum)
    thumbnail = models.TextField()
    # count comment of pic
    countComment = models.IntegerField()
    # count like of pic
    countLike = models.IntegerField()
    # short-code of pic
    shortcode = models.TextField()


class Owner(models.Model):
    # id user
    id = models.TextField(primary_key=True)
    # avatar user
    avatar = models.TextField()
    # username user
    name = models.TextField()


class DataCrawl(models.Model):
    # id userId or post id
    id = models.TextField(primary_key=True, unique=True)
    # info of owner
    owner = models.EmbeddedField(Owner)
    # list data crawl
    data = models.ArrayField(ItemCrawl)
    # Count images
    count = models.IntegerField()
    # ExpireAt
    _expireAt = models.DateTimeField()

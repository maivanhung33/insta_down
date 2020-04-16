from djongo import models


class ItemCrawl(models.Model):
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

    def to_dict(self):
        return dict(url=self.url,
                    thumbnailUrl=self.url,
                    countComment=self.count_comment,
                    countLike=self.count_like,
                    shortcode=self.shortcode)


class Owner(models.Model):
    # id user
    id = models.IntegerField(primary_key=True)
    # avatar user
    avatar = models.TextField()
    # username user
    name = models.TextField()

    def to_dict(self):
        return dict(id=self.id,
                    avatar=self.avatar,
                    name=self.name)


class DataCrawl(models.Model):
    # id user or post
    id = models.IntegerField(primary_key=True)
    # info of owner
    owner = models.EmbeddedField(Owner)
    # list data crawl
    data = models.ArrayField(ItemCrawl)

    def to_dict(self):
        owner = self.owner.__dict__
        del owner['_state']
        data = [item.__dict__ for item in self.data]
        for item in data:
            del item['_state']
            del item['id']
        return dict(id=self.id,
                    owner=owner,
                    data=data)

import datetime

class Episode:
    date = None
    title = None
    url = None
    thumbnail = None

    def __init__(self,date,title,url,thumbnail):
        self.date = date
        self.title = title
        self.url = url
        self.thumbnail = thumbnail

    def __str__(self):
        return "Title: " + self.title + "\nDate: " + str(self.date) + \
               "\nURL: " + self.url + "\nThumbnail: " + self.thumbnail

    def __eq__(self, other):
        return self.url == other.url

    def __hash__(self):
        # the hash of our string is our unique hash
        return hash(str(self.url))
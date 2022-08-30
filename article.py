from db import database

class article:
    def __init__(self, title, content, url, date):
        self.title = title
        self.content = content
        self.url = url
        self.date = date
        self.db = database()

    def set_title(self, title):
        self.title = title
    
    def set_content(self, content):
        self.content = content

    def set_url(self, url):
        self.url = url

    def set_date(self, date):
        self.date = date
    
    def push_to_db(self):
        self.db.article_push_to_db(self)
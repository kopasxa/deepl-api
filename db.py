import pymysql
import config

# class for connect to mysql database
class database:
    def __init__(self):
        self.db = pymysql.connect(host=config.DB_HOST, user=config.DB_USER, passwd=config.DB_PASSWORD, db=config.DB_NAME, port=config.DB_PORT)
        self.cursor = self.db.cursor()

    def query(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall() 

    def article_push_to_db(self, article):
        sql = "INSERT INTO articles (title, content, url, date) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(sql, (article.title, article.content, article.url, article.date))
        self.db.commit()

    def get_sources_articles(self):
        sql = "SELECT * FROM sources"
        return self.query(sql)

    def close(self):
        self.db.close()

    def __delete__ (self, instance):
        self.close()
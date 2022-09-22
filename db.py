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
        sql = "INSERT INTO articles (id_source, title, text, url, date, thumb) VALUES (%s, %s, %s, %s, %s, %s);"
        self.cursor.execute(sql, (article["id_source"], article["title"], article["text"], article["url"], article["date"], article["thumb"]))
        self.db.commit()
        self.cursor.execute("SELECT LAST_INSERT_ID();")
        return self.cursor.fetchone()[0]

    def set_images_by_article(self, article_id, images):
        sql = "INSERT INTO images (id_article, url) VALUES (%s, %s)"
        self.cursor.executemany(sql, [(article_id, image) for image in images])
        self.db.commit()

    def get_id_of_source(self, country):
        sql = "SELECT * FROM sources WHERE country = %s"
        self.cursor.execute(sql, (country))
        return self.cursor.fetchone()

    def get_all_articles(self, title, source_id):
        sql = "SELECT * FROM articles JOIN sources ON articles.id_source = sources.id WHERE articles.title = %s AND sources.id = %s"
        self.cursor.execute(sql, (title, source_id))
        return self.cursor.fetchone()

    def get_sources_articles(self):
        sql = "SELECT * FROM sources"
        return self.query(sql)

    def close(self):
        self.db.close()

    def __delete__ (self, instance):
        self.close()
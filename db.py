import sqlite3

from datetime import datetime
class DbHelper:
    def __init__(self):
        self.connection = sqlite3.connect('bolg.db',check_same_thread=False)
        self.cursor = self.connection.cursor()

    def get_blogs(self):
        self.cursor.execute("SELECT * FROM blogs")
        blogs_raw = self.cursor.fetchall()
        blogs=[]
        for blog in blogs_raw:
            blogs.append({'creator':blog[0],'title':blog[1],'body':blog[2],'maybe_images_url':blog[3],'date':blog[4]})

        del blogs_raw
        blogs.reverse()
        return blogs
    def add_blog(self,title, body, images_url=None):
        self.cursor.execute("INSERT INTO blogs VALUES (?,?,?,?,?)",("Vienna",title, body, images_url,datetime.today().strftime('%Y-%m-%d %H:%M:%S')))
        self.connection.commit()


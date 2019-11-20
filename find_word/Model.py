from pymysql import *
import hashlib


class UI:
    def __init__(self, host='localhost', port=3306, user='', passwd='', database='', charset='utf8'):
        self.__db = connect(
            host=host,
            port=port,
            user=user,
            passwd=passwd,
            database=database,
            charset=charset)
        self.cur = None

    def create_cur(self):
        self.cur = self.__db.cursor()

    def close(self):
        if self.cur:
            self.__db.cursor().close()
        self.__db.close()

    def register(self, name, password):
        sql = 'select name from user where name="%s"' % name
        self.cur.execute(sql)
        if self.cur.fetchone():
            return False
        # password = self.change_passwd(password)
        try:
            sql = 'insert into user(name,passwd) values("%s",%s)' % (name, password)
            self.cur.execute(sql)
        except Exception as e:
            print(e)
            self.__db.rollback()
            return False
        else:
            self.__db.commit()
            return True

    def login_in(self, name, password):
        # password = self.change_passwd(password)
        sql = 'select name,passwd from user where name="%s" and passwd = %s' % (name, password)
        self.cur.execute(sql)
        data = self.cur.fetchone()
        if data:
            return True
        return False

    def find_word(self, name, word):
        self.insert_into(name, word)
        sql = 'select mean from word where word = "%s"' % word
        self.cur.execute(sql)
        data = self.cur.fetchone()
        if data:
            return data[0]

    def insert_into(self, name, word):
        sql = 'insert into hist(name,word) values("%s","%s")' % (name, word)
        try:
            self.cur.execute(sql)
        except Exception as e:
            print(e)
            self.__db.rollback()
        else:
            self.__db.commit()

    def find_hist(self):
        sql = 'select name,word,curtime1 from hist order by curtime1 desc limit 10'
        self.cur.execute(sql)
        data = self.cur.fetchall()
        if data:
            return data

    # def change_passwd(self, passwd):
    #     salt = '!@#$%'
    #     new_passwd = hashlib.md5()
    #     new_passwd = new_passwd.update((salt + passwd).encode())
    #     passwd = new_passwd.hexdigest()
    #     return passwd

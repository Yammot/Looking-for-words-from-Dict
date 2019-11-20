from pymysql import *
import re

db = connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='123456',
    database='stu',
    charset='utf8')

cur = db.cursor()

f = open('dict.txt', 'r')

exc = []
for line in f:
    # word = line.split(' ',1)[0]
    # mean = ''.join(line.split(' ',1)[1].strip())
    # exc.append((word,mean))
    data = re.findall(r'(\S+)\s+(.*)', line)[0]
    exc.append(data)
f.close()

sql = 'insert into word(word,mean) values(%s,%s)'

try:
    cur.executemany(sql, exc)
except Exception as e:
    print(e)
    db.rollback()
else:
    db.commit()
finally:
    cur.close()
    db.close()

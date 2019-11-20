from socket import *
from multiprocessing import Process
import os, signal
from Model import UI

ADDR = ('localhost', 10086)
ui = UI(user='root', passwd='123456', database='stu')


def register(c, name, passwd):
    if ui.register(name, passwd):
        c.send(b'ok')
    else:
        c.send('失败'.encode())


def login_in(c, name, passwd):
    if ui.login_in(name, passwd):
        c.send(b'ok')
    else:
        c.send('失败'.encode())


def find_word(c, name, word):
    mean = ui.find_word(name, word)
    if not mean:
        c.send('没有找到单词'.encode())
    else:
        msg = '%s:%s' % (word, mean)
        c.send(msg.encode())


def find_hist(c):
    data = ui.find_hist()
    for item in data:
        msg = '%s:%s:%s' % (item[0], item[1], str(item[2]))
        c.send((msg + '\n').encode())


def run(c):
    ui.create_cur()
    while True:
        data = c.recv(1024).decode()
        print(c.getpeername(), data)
        msg = data.split(' ')
        if not data or msg[0] == 'E':
            return
        elif msg[0] == 'R':
            register(c, msg[1], msg[2])
        elif msg[0] == 'L':
            login_in(c, msg[1], msg[2])
        elif msg[0] == 'F':
            find_word(c, msg[1], msg[2])
        elif msg[0] == 'H':
            find_hist(c)


def main():
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(3)
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    while True:
        try:
            connfd, addr = s.accept()
            print('连接自:', addr)
        except KeyboardInterrupt:
            s.close()
            ui.close()
            os._exit(0)
        except Exception as e:
            print(e)
            continue
        p = Process(target=run, args=(connfd,))
        p.daemon = True
        p.start()


if __name__ == '__main__':
    main()

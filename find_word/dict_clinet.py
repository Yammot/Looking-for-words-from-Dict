from socket import *
import getpass,time
from Model import UI

ui = UI(user='root', passwd='123456', database='stu')


class Net:
    def __init__(self, ip):
        self.s = socket()
        self.ip = ip
        self.s.connect(self.ip)
        self.cur = ui.create_cur()

    def main(self):
        while True:
            print('1键注册,2键登录,3键注销')
            cmd = input('>>')
            if cmd == '1':
                self.register()
            elif cmd == '2':
                self.login_in()
            elif cmd == '3':
                self.s.close()
                return
            else:
                print('请输入正确的选项')

    def register(self):
        while True:
            name = input('名字:')
            passwd = getpass.getpass('密码:')
            passwd_ = getpass.getpass('密码:')

            if passwd != passwd_:
                print('密码不一致,请重新输入')
                continue

            if (' ' in name) or (' ' in passwd):
                print('不允许输入空格')
                continue

            msg = 'R %s %s' % (name, passwd)
            self.s.send(msg.encode())
            data = self.s.recv(128).decode()
            if data == 'ok':
                print('注册成功')
            else:
                print('注册失败')
            return

    def login_in(self):
        while True:
            name = input('名字:')
            passwd = getpass.getpass('密码:')
            passwd_ = getpass.getpass('密码:')

            if passwd != passwd_:
                print('密码不一致,请重新输入')
                continue

            msg = 'L %s %s' % (name, passwd)
            self.s.send(msg.encode())
            data = self.s.recv(128).decode()
            if data == 'ok':
                print('登录成功')
                self.display(name)
            else:
                print('登录失败')
            return

    def display(self, name):
        while True:
            print('1键查单词,2键查历史记录,3键注销')
            cmd = input('>>')
            if cmd == '1':
                self.find_word(name)
            elif cmd == '2':
                self.find_hist(name)
            elif cmd == '3':
                return
            else:
                print('输入有误,请重新输入')
                continue

    def find_word(self, name):
        while True:
            word = input('>>')
            if word == '##':
                break
            msg = 'F %s %s' % (name, word)
            self.s.send(msg.encode())
            data = self.s.recv(2048).decode()
            print(data)

    def find_hist(self, name):
        msg = 'H %s' % name
        self.s.send(msg.encode())
        data = self.s.recv(4096).decode()
        if not data:
            return
        time.sleep(0.1)
        print(data)


if __name__ == '__main__':
    s = Net(('localhost', 10086))
    s.main()

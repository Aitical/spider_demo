import base64
import requests
import time


class Online(object):
    """
    检测网络是否连接并,断网重连
    """
    def __init__(self, username, passwd, sleep=120):

        password = base64.b64encode(passwd.encode()).decode('utf8')

        self.data = {
                'username': username,
                'domain': '',
                'password': password,
                'enablemacauth': '0'
        }
        headers = {
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'a.suda.edu.cn',
            'Referer': 'http://a.suda.edu.cn/index.php?url=aHR0cDovL3dnLnN1ZGEuZWR1LmNuLw==',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        self.session = requests.Session()
        self.session.headers = headers
        self.sleep = sleep

    def connected(self):
        """
        判断当前网络是否连接
        :return: bool
        """
        try:
            requests.get('https://www.baidu.com', timeout=3)
            return True
        except requests.exceptions.ConnectTimeout:
            return False

    def login(self):
        """
        登录网关
        :return: bool
        """
        url = 'http://a.suda.edu.cn/index.php/index/login'
        resp = self.session.post(url, data=self.data)
        self.session.cookies = resp.cookies
        return resp.status_code == 200

    def run(self):
        """
        启动网络检测断网重连
        :return: None
        """
        self.login()
        time.sleep(10*60)
        while True:
            c = self.connected()
            if not c:
                self.login()
            time.sleep(self.sleep)



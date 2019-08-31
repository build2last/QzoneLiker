'''HttpClient unit test

author: build2last
20190831 v1
'''

import unittest
from core.HttpClient import HttpClient

class HttpClientTest(unittest.TestCase):
    '''HttpClient 测试类'''

    def setUp(self):
        self.client = HttpClient()
        self.url = "http://www.baidu.com"

    def test_get(self):
        '''测试 get 方法'''
        result = self.client.Get(self.url)
        print(result)
        self.assertIsNotNone(result)

    def test_post(self):
        '''测试 post 方法'''
        data = {"name": "test"}
        self.assertIsNotNone(self.client.Post(self.url, data))

    def test_download(self):
        ''' test Download method of HttpClient '''
        try:
            self.client.Download(self.url, "baidu.html")
        except Exception as e:
            self.assertFalse
    
    def test_getCookie(self):
        '''test getCookie method of HttpClient'''
        self.assertIsNotNone(self.client.getCookie("test"))

if __name__ == "__main__":
    unittest.main()

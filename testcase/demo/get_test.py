# encoding utf-8
import requests
import unittest
from common import HTTP

class GetNothing(unittest.TestCase):
    def setUp(self):
        host = "https://httpbin.org/"
        endpoint = "get"
        self.url = ''.join([host,endpoint])

    def test_get_nothing(self):
        ###给服务器发送请求
        r = requests.get(self.url)
        #print(r.url) #获取URL
        #print(r.status_code,r.reason) #获取状态码
        # print(r.headers) #获取响应头
        # print(r.text) #文本信息str字符串形式
        # print(r.content) #byte图片，文件更常用
        # print(r.request.headers) #请求头
        # print(r.request.url)
        # print(r.request.method)
        response = r.json()
        resp = HTTP.myHTTP().get(self.url)
        # User_Agent = resp['headers']['User-Agent']
        # self.assertEquals(User_Agent,'python-requests/2.22.0')
        code = resp.status_code
        self.assertEqual(code,200)

    '''
    # @unittest.skip('无条件跳过')
    def test_get_nothing2(self):
        #判断状态码是否为200，不需要转换格式可以直接取status_code字段
        r = requests.get(self.url)
        status_code = r.status_code
        DataAll = {}
        Method = 'get' #参数2
        resp = base.get_response(self.url,Method,**DataAll)
        # print(status_code)
        self.assertEquals(status_code,201)
    '''

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
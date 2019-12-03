# encoding utf-8

import unittest
from common import base

class PostData(unittest.TestCase):
    def setUp(self):
        host = "https://httpbin.org/"
        endpoint = "post"
        self.url = ''.join([host,endpoint])

    def test_post_data(self):
        params = {'show_env':1}
        data = {'a':111,'b':222}
        DataAll={'params':params,'data':data}
        #对象调用的必须是post方法，不能是get方法
        # resp = HttpService.MyHTTP().post(self.url,**DataAll)
        # response = r.json()
        Method = 'post' #参数2
        resp = base.get_response(self.url,Method,**DataAll)
        form = resp.get('form').get('a') #将响应体格式化，并取出form-a中的值赋值给form
        # print(r.status_code,r.reason)
        # print(r.text)
        print(resp)
        # print(r.headers)
        # print(response['form']) #从response返回的字典中取出自己要的字段
        # print(response['json'])
        # print(response['url'])
        self.assertEquals(form,'111') #比较form的预期的值是否一致
        self.assertIsInstance(form,str) #判断form是字符串格式

    # @unittest.skip('无条件跳过')
    # def test_post_data2(self):
    #     params = {'show_env':1}
    #     data = {'a':'skip','b':'装饰器跳过测试'}
    #     # r = requests.post(self.url,data=data)
    #     # resp = r.json()
    #     DataAll = {'params': params, 'data': data}
    #     resp = HttpService.MyHTTP().get(self.url, **DataAll)
    #     form = resp.get('form').get('a')
    #     self.assertEquals(form,'skip')
    #     self.assertIsInstance(form,str)

    def tearDwon(self):
        pass


if __name__ == '__main__':
    unittest.main()
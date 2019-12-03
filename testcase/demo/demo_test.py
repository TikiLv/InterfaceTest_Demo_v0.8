import unittest
import paramunittest
import readConfig as readConf
from common.Log import myLog as Log
from common import base,HTTP

demo_cls = base.get_xls("demo.xlsx","demo_test")
localreadconf = readConf.ReadConfig()
http = HTTP.myHTTP()
log = Log.get_log()
logger = log.get_logger()

#将列表里的数据参数化
@paramunittest.parametrized(*demo_cls)
class Demo(unittest.TestCase):
    def setParameters(self, case_name, method, token, code, msg):

        self.case_name = str(case_name)
        self.method = str(method)
        self.token = str(token)
        self.code = int(code)
        self.msg = str(msg)

    def description(self):
        return  self.case_name

    def setUp(self):
        self.log = Log.get_log()
        self.logger = self.log.get_logger()
        # self.cookie = base.login()

    def test_demo(self):
        '''
        set url
        :return:
        '''
        self.path = demo_cls[1][1]
        print(self.path)
        URL = http.set_url(self.path) #拼接完整的接口地址
        print(URL)
        #set headers
        #set data

        try:
            #test interface 确认类型，选择合适的方法
            self.return_json = http.get() #响应类型
            info_dic = self.return_json.json() #字典格式,需要将response结果做序列化处理
            info_str = self.return_json.text #字符串格式
            print(info_dic)
            result = info_dic.get('url')
            print(self.case_name)
            #check result
            #或者直接使用断言判断结果
            self.assertEqual(result,"https://httpbin.org/get")
            logger.info(self.case_name + '已执行完')
        except Exception as e:
            logger.error(e)

    def tearDown(self):
        self.info = self.return_json.json()
        try:
            log.build_case_line(self.case_name, self.info.get('url'),self.info.get('origin'))
            # print(self.name+ "测试结束，输出log完结\n\n")
            logger.info(self.case_name + '已执行完\n')
        except Exception as e:
            logger.error(e) #成功打印，但是日志显示错误，报告是正常的！
            print("错误：",e)

if __name__ == '__main__':
    Demo(unittest.TestCase)
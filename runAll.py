import os
import unittest
from common.Log import myLog as Log
import readConfig as readConf
from common import HTMLTestRunner
# from common import HTMLTestRunner
from common.Email import myEmail
import BeautifulReport

localReadConf = readConf.ReadConfig()

class ALLTest():
    def __init__(self):
        global log,logger,resultPath,on_off
        log = Log.get_log()
        logger = log.get_logger()
        resultPath = log.get_report_path() #返回报告的完整路径
        on_off = localReadConf.get_email('on_off')
        self.caseListFile = os.path.join(readConf.proDir, "caselist.txt")
        self.testcase = os.path.join(readConf.proDir, "testcase")
        print(self.testcase)
        self.caseList = []
        #从caselist里读取哪些需要执行
        self.email = myEmail.get_email()


    #查看case list里的不带#的case list执行
    def set_case_list(self):
        fb = open(self.caseListFile)
        for value in fb.readlines():
            data = str(value)
            if data != '' and not data.startswith('#'):
                self.caseList.append(data.replace("\n", ""))
            fb.close()

    #将要执行的所有用例添加到casesuite里
    def set_case_suite(self):
        self.set_case_list()
        test_suite = unittest.TestSuite()
        suite_module = []
        for case in self.caseList:
            case_name = case.split("/")[-1]+'.py'
            discover = unittest.defaultTestLoader.discover(self.testcase, pattern=case_name)
            suite_module.append(discover)
        #如果
        if len(suite_module) > 0:
            for suite in suite_module:
                for test_name in suite:
                    test_suite.addTest(test_name)
        else:
            return None
        return test_suite

    def run(self):
        try:
            discover = self.set_case_suite()
            # print('set_case_suite:',discover)
            if discover is not None:
                logger.info('************测试开始***********')
                fp = open(resultPath,'wb')
                runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title='测试报告',description='测试描述')
                runner.run(discover)
                fp.close()
            else:
                logger.info('没有要运行的测试用例')
        except Exception as ex:
            logger.error(ex)
        finally:
            logger.info('************测试结束*************')
            # fp.close()

            if on_off == 'on':
                self.email.send_email()
            elif on_off == 'off':
                logger.info('不发送测试报告给开发者')
            else:
                logger.info('未知状态')

    #不带case list，邮件发送功能
    def run_1(self):
        # testcase_dir = '/Users/tiki/interface_Demo/testcase/demo/' #获取testcase的路径
        # testcase_dir = self.testcase+'/demo/'  #凭借方法，join函数不能用
        testcase_dir = './testcase'
        try:
            discover = unittest.defaultTestLoader.discover(testcase_dir, pattern='*_test.py')
            if discover is not None:
                logger.info('**********测试开始*********')
                fp = open(resultPath,'wb') #打开创建的report.html写文件？
                runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title='测试报告',description='测试描述')
                runner.run(discover)
                fp.close()
            else:
                logger.info('没有可执行的测试用例!')
        except Exception as ex:
            logger.error(str(ex),'11111111xxxxxxyyyyy')
        finally:
            logger.info('**********测试结束*********')
            # fp.close()


if __name__ == '__main__':
    obj = ALLTest()
    # print(obj.set_case_suite()) #case list里需要执行的用例
    obj.run()
import requests
import readConfig as readConf
from common.Log import myLog
from common import base

localReadConfig = readConf.ReadConfig()

class myHTTP:
    def __init__(self):
        global scheme,host,port,timeout,sessionid,urlpath
        scheme = localReadConfig.get_http('scheme')
        host = localReadConfig.get_http('baseurl')
        port = localReadConfig.get_http('port')
        timeout = localReadConfig.get_http('timeout')
        sessionid = localReadConfig.get_headers('cookie')
        # urlpath = '' #自己加的
        self.url = None
        self.headers = {}
        self.params ={}
        self.data = {}
        self.files = {}
        self.state = 0
        self.log = myLog.get_log()
        self.logger = self.log.get_logger()

    #urlpath可能存在与excel里
    def set_url(self,urlpath):
        self.url = scheme +'://' +host +':'+port + '/' + urlpath
        return self.url

    def set_headers(self,headers):
        self.headers = headers

    def set_params(self,params):
        self.params = params

    def set_data(self,data):
        self.data = data

    #设置上传files，params=filename
    def set_files(self,filename):
        if filename != '':
            file_path='路径'+filename
            self.files = {'file':open(file_path,'rb')}
        if filename == '' or filename is None:
            self.state = 1

    def get(self):
        """
        defined get method
        :return:
        """
        try:
            response = requests.get(self.url, headers=self.headers, params=self.params, timeout=float(timeout))
            # response.raise_for_status()
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    def post(self):
        try:
            response = requests.post(self.url, headers=self.headers, params=self.params, data=self.data, timeout=float(timeout))
            # response.raise_for_status()
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    def postWithFile(self):
        """
        defined post method
        :return:
        """
        try:
            response = requests.post(self.url, headers=self.headers, data=self.data, files=self.files, timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    # defined http post method
    # for json
    def postWithJson(self):
        """
        defined post method
        :return:
        """
        try:
            response = requests.post(self.url, headers=self.headers, json=self.data, timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    #未验证
    def put(self):
        try:
            response = requests.put(self.url, headers=self.headers, params=self.params, data=self.data, timeout=float(timeout))
            # response.raise_for_status()
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None
    #未验证
    def delete(self):
        try:
            response = requests.delete(self.url, headers=self.headers, timeout=float(timeout))
            # response.raise_for_status()
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

if __name__ == '__main__':
    my=myHTTP()

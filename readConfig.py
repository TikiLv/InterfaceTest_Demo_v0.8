import os
import codecs
import configparser as cfp

proDir = os.path.split(os.path.realpath(__file__))[0] #获取当前文件的路径
configPath = os.path.join(proDir,'config.ini')

class ReadConfig():
    def __init__(self):
        fp = open(configPath)
        data = fp.read()
        if data[3:] == codecs.BOM_UTF8:
            data = data[3:]
            file = codecs.open(configPath,'w')
            file.write(data)
            file.close()
        fp.close()

        self.cf = cfp.ConfigParser()
        self.cf.read(configPath)

    def get_email(self,name):
        value = self.cf.get('EMAIL',name)
        return value

    def get_http(self,name):
        value = self.cf.get('HTTP',name)
        return value

    def get_headers(self,name):
        value = self.cf.get('HEADERS',name)
        return value

    def set_headers(self,name,value):
        self.cf.set('HEADERS',name,value)
        with open(configPath,'w+') as f:  #w+读写，若文件已存在，内容将先被清空
            self.cf.write(f)

    def get_url(self,name):
        value = self.cf.get('URL',name)
        return value

    def get_db(self,name):
        value = self.cf.get('DATABASE',name)
        return value

if __name__ == '__main__':
    rc = ReadConfig()
    name = rc.get_db('host')
    print(name)

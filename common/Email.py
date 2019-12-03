import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime
import time
import threading
import readConfig as readConf
from common.Log import myLog as Log
# import zipfile
import glob

localReadConf = readConf.ReadConfig()

class Email:
    # init少写一个字母__int__
    def __init__(self):
        global host,user,password,port,sender,title
        host = localReadConf.get_email('mail_host')
        user = localReadConf.get_email('mail_user')
        password = localReadConf.get_email('mail_pwd') #smtp的授权码
        port =  localReadConf.get_email('mail_port')
        sender = localReadConf.get_email('sender')
        title = localReadConf.get_email('subject')
        self.value = localReadConf.get_email('receiver')
        self.receiver = []
        for n in str(self.value).split(";"):
            self.receiver.append(n)
        # print(self.receiver)

        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.subject = '接口测试报告' + '/'+ date
        self.log = Log.get_log()
        self.logger = self.log.get_logger()
        self.msg = MIMEMultipart('related')

    def config_header(self):
        self.msg['Subject'] = self.subject
        self.msg['From'] = sender
        self.msg['To'] = ";".join(self.receiver)

    def config_content(self):
        #打开指定路径下email格式文件
        f = open(os.path.join(readConf.proDir,'testdata','emailStyle.txt'))
        content = f.read()
        f.close()
        content_plain = MIMEText(content,'html','utf-8')
        self.msg.attach(content_plain)
        self.config_image()

    def config_image(self):
        pass

    '''
    #构造附件内容，并压缩内容成zip文件，zip打不开！！！
    def config_file1(self):
        if self.check_file():
            reportpath = self.log.get_result_path()
            zippath = os.path.join(readConf.proDir,'result','test.zip')

            files = glob.glob(reportpath+'\*')
            f = zipfile.ZipFile(zippath,'w',zipfile.ZIP_DEFLATED)
            for file in files:
                #修改压缩文件的目录结构
                f.write(file,'/report/'+os.path.basename(file))
            f.close()
            reportfile = open(zippath,'rb').read()
            filehtml = MIMEText(reportfile,'base64','utf-8')
            filehtml['Content-Type'] = 'application/octet-stream'
            filehtml['Content-Disposition'] = 'attachment;filename="test.zip"'
            # filehtml['Content-Disposition'] = 'attachment;filename = %s' % lists[-1] #尝试构造单附件的邮件
            self.msg.attach(filehtml)
            '''
    #构造configfile的类似函数
    def config_file(self):
        reportpath = self.log.get_result_path()
        lists = os.listdir(reportpath)
        lists.sort(key=lambda fn:os.path.getatime(reportpath+'/'+fn))
        for i in range(2):
            file = os.path.join(reportpath,lists[i]) #顺序上传路径下的文件
            send_file = open(file,'rb').read()
            att = MIMEText(send_file,'base64','utf-8')
            att['Content-Type'] = 'application/octet-stream'
            att['Content-Disposition'] = 'attachment;filename = %s'%lists[i]
            self.msg.attach(att)

    def check_file(self):
        reportpath = self.log.get_report_path()
        if os.path.isfile(reportpath) and not os.stat(reportpath)==0:
            return True
        else:
            return False

    def send_email(self):
        self.config_header()
        self.config_content()
        self.config_file()
        try:
            smtp = smtplib.SMTP()
            smtp.connect(host)
            smtp.login(user,password)
            smtp.sendmail(sender,self.receiver,self.msg.as_string())
            smtp.quit()
            self.logger.info('测试报告已经通过邮件发送给开发者！')
        except Exception as ex:
            self.logger.error(ex)

class myEmail:
    email = None
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def get_email():
        if myEmail.email is None:
            myEmail.mutex.acquire()
            myEmail.email = Email() #创建Email的对象
            myEmail.mutex.release()
        return myEmail.email

if __name__ == '__main__':
    # e = Email()
    # e.config_file()
    email = myEmail.get_email()
    myEmail.email.send_email()

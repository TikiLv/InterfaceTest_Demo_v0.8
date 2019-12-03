import os
import logging
import readConfig as readConf
from datetime import datetime
import threading

#------------------------------------------------
# Logger 记录器，暴露了应用程序代码能直接使用的接口。

# Handler 处理器，将（记录器产生的）日志记录发送至合适的目的地。

# Filter 过滤器，提供了更好的粒度控制，它可以决定输出哪些日志记录。

# Formatter 格式化器，指明了最终输出中日志记录的布局
#------------------------------------------------

class Log:
    def __init__(self):
        global logPath,resultPath,proDir
        proDir = readConf.proDir
        resultPath = os.path.join(proDir,'result')
        if not os.path.exists(resultPath):
            os.mkdir(resultPath) #不存在则创建
        logPath = os.path.join(resultPath,str(datetime.now().strftime('%Y%m%d %H%M%S')))

        if not os.path.exists(logPath):
            os.mkdir(logPath)
        self.logger = logging.getLogger()  #对象
        self.logger.setLevel(logging.INFO) #logger等级开关

        #将logger添加到handler里面，为Logger实例增加一个处理器
        handler = logging.FileHandler(os.path.join(logPath,'output.log'),encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s -%(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
#------------------------------------------------------------------------------
        # logging.debug("详细信息，典型地调试问题时会感兴趣。");

        # http://logging.info("打证明事情按预期工作");

        # logging.warning("表明发生了一些意外，或者不久的将来会发生问题（如‘磁盘满了’）。软件还是在正常工作。")

        # logging.error("由于更严重的问题，软件已不能执行一些功能了")

        # logging.critical("严重错误，表明软件已不能继续运行了。");
#  ------------------------------------------------------------------------------

    def get_logger(self):
        return self.logger

    def build_start_line(self,case_no):
        self.logger.info('----------'+ case_no +'START----------')

    def build_end_line(self,case_no):
        self.build_end_line('----------'+ case_no +'END----------')

    def build_case_line(self,case_name,code,msg):
        strCode = str(code)
        self.logger.info(case_name+'- Code:'+strCode +'- msg:'+msg)

    def get_report_path(self):
        report_logPath= os.path.join(logPath,'report.html')
        # print(report_logPath)
        return report_logPath

    def get_result_path(self):
        return logPath

    def write_result(self,result):
        result_path = os.path.join(logPath,'report.txt')
        fp = open(result_path,'wb')
        try:
            fp.write(result)
        except FileNotFoundError as ex:
            logging.error(str(ex))

class myLog:
    log = None
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def get_log():
        if myLog.log is None:
            myLog.mutex.acquire()
            myLog.log = Log() #Log对象,调用初始化函数
            myLog.mutex.release()
        return myLog.log

if __name__ == '__main__':
    log = myLog.get_log()
    logger = log.get_logger()
    logger.debug('test debug')
    logger.info('test info')
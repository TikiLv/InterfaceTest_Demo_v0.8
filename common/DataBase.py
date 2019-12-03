import pymysql
import readConfig as readConf
from common.Log import myLog as Log

localReadConf = readConf.ReadConfig()

class myDB:
    global host,user,password,port,database,config
    host = localReadConf.get_db('host')
    user = localReadConf.get_db('user')
    password = localReadConf.get_db('password')
    port = localReadConf.get_db('port')
    database = localReadConf.get_db('database')
    config = {
        'host':str(host),
        'user':user,
        'password':password,
        'port':int(port),
        'db':database
    }

    def __int__(self):
        self.log = Log.get_log()
        self.logger = self.log.get_logger()
        self.db = None
        self.cursor = None
        print(self.logger.error())

    def connectDB(self):
        try:
            self.db = pymysql.connect(**config)
            self.cursor = self.db.cursor()
            print('数据库连接成功！')
        except Exception as e:
            print(e)
        # except ConnectionError as ex:
        #     self.logger.error(str(ex)) #logger对象没有

    def executeSQL(self,sql,params):
        self.connectDB()
        self.cursor.execute(sql,params)
        self.db.commit()
        return self.cursor

    def get_all(self,cursor):
        value = cursor.fetchall()
        return value

    def get_one(self,cursor):
        value = cursor.fetchone()
        return value

    def closeDB(self):
        self.db.close()
        print('关闭数据库！')

if __name__ == '__main__':
    db = myDB()
    db.connectDB()
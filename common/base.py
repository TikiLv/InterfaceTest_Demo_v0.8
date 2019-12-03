import os
import requests
import readConfig
from xlrd import open_workbook
from common import HTTP,Log
import json

localReadConfig = readConfig.ReadConfig()
# localmyHTTP = HTTP.myHTTP()
proDir = readConfig.proDir
# localxls = base.get_xls('testcase.xls','login') #先声明后调用
log = Log.myLog.get_log()
url1 = 'https://hhtpbim.org'

'''
#获取cookie
def login():
    url = localmyHTTP.set_url('/login')
    data = {'account':'root',
            'passwd':'root'}
    localmyHTTP.set_data(data)
    session = requests.Session()
    response = session.post(url,data)
    sessionId = session.cookie.get_dict()['JSESSIONID']
    cookie = 'JSESSIONID=' + sessionId
    localReadConfig.set_headers('cookie',cookie)
    return cookie

    # response = localmyHTTP.post().json()
    # token = base.get_value_form_return_json(response,'member','token')
    # return token

def logout():
    url = localmyHTTP.set_url('/join')
    localmyHTTP.set_url(url)
    localmyHTTP.get()
'''

#********读excel里的内容
def get_xls(xls_name,sheet_name):
    cls = []
    xlspath = os.path.join(proDir,'testdata','case',xls_name)
    file = open_workbook(xlspath)
    sheet =file.sheet_by_name(sheet_name)
    nrows = sheet.nrows
    for i in range(nrows):
        if sheet.row_values(i)[0] != 'case_name':
            cls.append(sheet.row_values(i))
    return cls

def get_value_from_return_json(json,name1,name2):
    info = json['info']
    group = info[name1]
    value = info[name2]
    return group,value

def show_return_msg(response):
    url = response.url
    msg = response.text
    print('\n请求地址：'+url)
    print('\n请求返回值：'+'\n'+json.dumps(json.loads(msg),ensure_ascii=False,sort_keys=True,indent=4))

#*****************读取sql xml
database = {}

def set_xml():
    pass

def get_xml_dict():
    pass

def get_sql():
    pass

#读取接口url xml
def get_url_form_xml(name):
    pass
#******************************
#单独封装增加的，方便获取response内容
'''
def get_response(url, Method, **DataAll):
    if Method == 'get':
        resp = HTTP.myHTTP.get(url,**DataAll)
        # text = resp.json()
    elif Method == 'post':
        resp = HTTP.myHTTP.post(url,**DataAll)
    elif Method == 'put':
        resp = HTTP.myHTTP.put(url, **DataAll)
        # text = resp.json()
    elif Method == 'delete':
        resp = HTTP.myHTTP.delete(url, **DataAll)
        # text = resp.json()
    ##需要其他方法再加其他方法，首先在httpservice里定义方法，参照get和post
    return resp
'''

def url():
    url = 'https://httpbin.org/'
    return url

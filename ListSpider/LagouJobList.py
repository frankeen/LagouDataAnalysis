#-*- coding:utf-8 -*-
import urllib
import requests
import json
import time,re
import random,os
import xlrd
from lxml import etree
from bs4 import BeautifulSoup
import time
import mysql.connector
from mysql.connector import errorcode
from threading import Thread
from multiprocessing import Process
from xlutils.copy import copy
from urllib.parse import quote
from configparser import ConfigParser
import psutil
import multiprocessing
import xml.dom.minidom
from multiprocessing.dummy import Pool as ThreadPool


basedir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
insert_joblist_sql="INSERT INTO temp_lagulist (id,position_name,company_name,salary,workyear,companyShortName, city, jobNature,education, position_id, createTime,companyId,keywords,positionLables,companySize,firstType,secondType,district) values ( %s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)"
insert_pagecount_sql="INSERT INTO temp_lagupagecount(id,tagName,totalcount,pagecount,tagId,fatherTagName) values(%s,%s,%s,%s,%s,%s)"
select_list_sql="SELECT DISTINCT position_id,position_name,company_name,companyShortName FROM temp_lagulist WHERE keywords=%s"
keyword_debug={"技术经理"}
keywords_jishu_simple={"Ruby"}



def read_db_Config(filename='config.ini',section='mysql'):
  #创建个parser和读取配置文件
  parser=ConfigParser()
  parser.read(filename)

  dbConfig = {}
  if parser.has_section(section):
    items=parser.items(section)
    for item in items:
      dbConfig[item[0]]=item[1]
  else:
    raise Exception('{0} not found in the {1} file'.format(section,filename))
  print(dbConfig)
  return dbConfig    

  config.read('')
def getCpuAndMem():
  # 系统的内存利用率
  print("the memory percent is ")
  print(psutil.virtual_memory().percent)
  cpuUsed=psutil.cpu_percent(interval=None,percpu=False)
  print("the cpu percent is "+str(cpuUsed))


def SaveCpuAndMemToFile():
  # 系统的内存利用率
  memPercent=psutil.virtual_memory().percent
  cpu=  psutil.cpu_percent(interval=None,percpu=False)
  with open('CpuAndMem.txt', 'a+') as f:
    f.write("the cpu percent is : "+str(cpu)+";the mem percent is : "+str(memPercent))
    f.write("\n")
  
def keywords_item(keywords):
  keywordsList=[]
  for item in keywords:
    keyword_item=item
    keywordsList.append(keyword_item)  
  #print(keywordsList)
  return  keywordsList   

def selectModel(keyword):
  """
  查询单条数据时，生成查询条件的元组
  """
  selectmodel=(keyword,)
  return selectmodel
def saveTomysql(result,sql):
  """
  根据sql语句的不同执行不同的方法
  """
  config=read_db_Config()
  cnx=mysql.connector.connect(**config)  
  cursor=cnx.cursor()
  data=[item for item in result]
  print(tuple(data))
  print("没有报错")
  cursor.executemany(sql,tuple(data))
  cnx.commit()
  cursor.close()
  cnx.close()
def saveTomysql2(sql,params,dbconfig):
  """
  根据sql语句的不同执行不同的方法
  """
  config=read_db_Config()
  cnx=mysql.connector.connect(**config)  
  cursor=cnx.cursor()
  data=[item for item in result]
  print(tuple(data))
  print("没有报错")
  cursor.executemany(sql,tuple(data))
  cnx.commit()
  cursor.close()
  cnx.close()

def SelectOneByKeyword(sql,keyword):
  """
  根据关键字查询第一条数据
  """
  Group=[]
  key=selectModel(keyword)
  print(key)
  config=read_db_Config()

  cnx=mysql.connector.connect(**config)  
  cursor=cnx.cursor(buffered=True)
  cursor.execute(sql,tuple(key))
  cnx.commit

  Group=cursor.fetchone()
  print("sqlnum"+str(Group))
  cursor.close()
  cnx.close()
  return Group
def SelectAllByKeyword(sql,keyword):
  """
  根据关键字所有的数据
  """
  config=read_db_Config()
  Group=[]
  key=selectModel(keyword)
  print("key="+"   "+str(key))
  cnx=mysql.connector.connect(**config)  
  cursor=cnx.cursor(buffered=True)
  cursor.execute(sql,tuple(key))
  cnx.commit

  Group=cursor.fetchall()
  #print("sqlnum"+str(Group))
  cursor.close()
  cnx.close()
  return Group
def get_ip_ports():
  """
  从包含代理服务器IP的文件中获取代理IP
  """ 
  count=0
  data=[]
  with open(basedir+'proxy_list.txt') as f:
    for line in f:
      str=line.strip()
      data.append(str)
  return data  


def getPageCount(keyword):
  """
  入参:keywords
  出参:(totalpagecount，totalcount)
  totalpagecount 总页数
  totalcount
  """
  url='https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
  referstr="https://www.lagou.com/jobs/list_"+str(quote(keyword))+"?labelWords=&fromSearch=true&suginput="
  #print(referstr)

  headers = {
          'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64) AppleWebKit/537.36(KHTML, like Gecko)Chrome/61.0.3163.79 Safari/537.36',
          'host': 'www.lagou.com',
          'Referer':referstr,
          'Cookie': 'user_trace_token = 20170825172024 - bacd1a4b - 2255 - 4654 - b457 - 515c631734ea;LGUID = 20170825172033 - a5538dab - 8976 - 11e7 - 8ed1 - 5254005c3644;X_HTTP_TOKEN = b1de8b4a133489968a90c6eace00b223;showExpriedIndex = 1;showExpriedCompanyHome = 1;showExpriedMyPublish = 1;hasDeliver = 43;TG - TRACK - CODE = search_code;index_location_city = % E5 % 85 % A8 % E5 % 9B % BD;login = false;unick = "";_putrc = "";JSESSIONID = ABAAABAAADEAAFI69018E2C5FCF41EFD7EB90825DF1DA5B;_gid = GA1.2.306486117.1506009766; _gat = 1;_ga = GA1.2.728564437.1503652829;Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6 = 1503652829, 1503927880, 1504702487, 1506009766;Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6 = 1506012702;LGSID = 20170922000246 - 4f1481fa - 9ee6 - 11e7 - 9219 - 5254005c3644;LGRID = 20170922005142 - 255c58f4 - 9eed - 11e7 - a097 - 525400f775ce;SEARCH_ID = 88c191cf0a45466aa247475560583f64',
          'X - Anit - Forge - Code': '0',
          'X - Anit - Forge - Token': None,
          'X - Requested - With': 'XMLHttpRequest'
  } 
  form_data = {
          'first': 'true',
          'pn': '1',
          'kd': str(keyword)
  }
  currentproxies={'http':random.choice(get_ip_ports())}
  result = requests.post(url,proxies=currentproxies, headers=headers, data=form_data)           
  try:
    if result.status_code==200:  
      jsonResult = result.json()
      page_positions = jsonResult['content']['positionResult']
      totalcount=page_positions['totalCount']

      totalpagecount=int(totalcount/15+1)

      return_content=(totalpagecount,totalcount,url,headers)

    else:
      return_content=()
    return return_content
  except Exception as e:
    raise e

"""
  数据模型用于temp_lagulist
"""
def savedb_parseJobList(url,headers,form_data,keyword):
  """
  解决result为404
  """
  pattern = re.compile(r'\d+')
  outstr=''

  positions = []
  currentproxies={'http':random.choice(get_ip_ports())}
  result = requests.post(url,proxies=currentproxies, headers=headers, data=form_data)           
  soup=BeautifulSoup(result.content,'lxml')  
  print(result.content)

  try:

    jsonResult = result.json()

    try:
      
      page_positions = jsonResult['content']['positionResult']['result']

      if len(page_positions)==0:
        #print(len(page_positions))    

        return len(page_positions)
      else: 
        for position in page_positions:
          try:  
            for label in position['positionLables']:
              labelstr=''
              labelstr+=str(label)+','
            position_dict=(
              '',
             position['positionName'],
             position['companyFullName'],       
             position['salary'],
             position['workYear'],
             position['companyShortName'],
             position['city'],
             position['jobNature'],
             position['education'],
             position['positionId'],
             position['createTime'],
             position['companyId'],
             str(keyword),
             labelstr,
             position['companySize'],
             position['firstType'],
             position['secondType'],
             position['district'],

            )
          except:
            pass
          positions.append(position_dict)
        print("IS OK")
        saveTomysql(positions,insert_joblist_sql) 
        SaveCpuAndMemToFile()
        return positions 

         
      
    except Exception as e:
      getCpuAndMem()
      print(str(url)+str(result.status_code)+str(form_data))
      with open('ErrorJobListcontent.txt', 'a+') as f:
        f.write(str(url)+str(result.status_code)+str(form_data))
        f.write("\n")

        f.write("-----------------------") 

        f.write(str(result.text))
        f.write("-----------------------") 
        f.write("\n")
      raise e    
  except:
    print("god love your")
    with open('errorJobList.txt', 'a+') as f:
      f.write(str(result.content))
      f.write("\n")    

      f.write("-------------")
      f.write("\n")    
    #print(result.content)
    errorDetail=soup.find(class_='i_error').findAll('img')
    #print(errorDetail)
    for i in errorDetail:
      t=i.get('alt')
      outstr=outstr+t
    errorout_status=pattern.match(outstr).group()
    #print(errorout)
    error_status_jobId=(str(keyword),errorout_status,str(form_data))
    with open('errorJobList.txt', 'a+') as f:
      f.write(str(error_status_jobId))
      f.write("\n")  
          
  
def position_dict(startpage,endpage,url,headers,thread,keyword):   
  """
  解决第N页没有数据后，还继续请求，否则还执行几千次

  """  
  print("currentThread is: "+str(thread)+"---"+"position_dict2 excute successful")  
  for x in range(startpage,endpage):
    form_data = {
            'first': 'true',
              'pn':x ,
              'kd': str(keyword)
    }
    time.sleep(3)
    print("currentThread is: "+str(thread)+"---"+"currentPage"+str(x)+"position_dict2 excute successful")        
    if savedb_parseJobList(url,headers,form_data,keyword)==0:

      print("IS NOT OK") 
      break  

def position_dict_debug(startpage,endpage,url,headers,thread,keyword): 
  """
  用于报错调试用的方法
  """  
  for x in range(1,8):
    form_data = {
                'first': 'true',
                  'pn':x ,
                  'kd': str(keyword)
    }
    time.sleep(2)
    print("currentThread is: "+str(thread)+"---"+"currentPage"+str(x)+"position_dict excute successful")        
    if savedb_parseJobList5(url,headers,form_data,keyword)==0:
      print("IS NOT OK") 
      break

def Threadfunc_multi(thread,keyword):
  """
  多线程处理
  """
  pageModel=getPageCount(keyword)
  perpageNo=pageModel[0]
  url=pageModel[2]
  headers=pageModel[3]

  pagestart=1
  pageend=perpageNo

  print("thread:"+str(thread)+"  " +"keywords"+str(keyword)+"   "+"pagestart:"+str(pagestart)+"   "+"pageend"+str(pageend))
  position_dict(pagestart,pageend,url,headers,thread,keyword)  
 
def multiprocess(keywords):
  keyList=keywords_item(keywords)

  with multiprocessing.Pool(processes=1) as pool:
    results = pool.starmap(Threadfunc_multi, zip(range(len(keyList)),keywords_item(keywords)))
    #print(results)


if __name__ == '__main__':

  multiprocess(keywords_jishu_simple)

  #SelectAllByKeyword(select_list_sql,"深度学习")
 

  
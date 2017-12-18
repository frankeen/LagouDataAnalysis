#-*- coding:utf-8 -*-
import mysql.connector
from mysql.connector import errorcode

class HandlerDB:
    """docstring for HandlerDB"""
    def __init__(self, sql):
        self.sql=sql
    def saveTomysql2(sql,result,config):
    """
    根据sql语句的不同执行不同的方法
    """
        config=read_db_Config()
        cnx=mysql.connector.connect(**self.config)  
        cursor=cnx.cursor()
        data=[item for item in result]
        print(tuple(data))
        print("没有报错")
        cursor.executemany(self.sql,tuple(data))
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
        cursor.execute(self.sql,tuple(key))
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
        cursor.execute(self.sql,tuple(key))
        cnx.commit

        Group=cursor.fetchall()
        #print("sqlnum"+str(Group))
        cursor.close()
        cnx.close()
        return Group
     
     
        
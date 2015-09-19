# -*- coding: utf-8 -*-
from mysql_base import Base,A
from sqlalchemy import create_engine
mysqlTssBR = "mysql://root:123456@localhost/nome-da-base"

def respQuery(mes,ano,pais,report):
paisMySql = {
"xxx-xx" : "mysql://usuario:senha@127.0.0.1/nome-da-base",
}

engine = create_engine(paisMySql[pais])
#engine = create_engine(mysqlTssBR)
connection = engine.connect()

queryTFX = """
# query
""" % (ano,mes,ano,mes)


if pais[0:1+2]=="xxx":
result = connection.execute(queryTSS)
elif pais[0:1+2]=="xxx":
result = connection.execute(queryTFX)
elif pais[0:1+2]=="xxx":
result = connection.execute(queryTMB)
elif pais[0:1+2]=="xxx":
result = connection.execute(queryTNT)
elif pais[0:1+2]=="xxx":
result = connection.execute(queryNetAssist)
elif pais[0:1+2]=="xxx" and report==1:
result = connection.execute(queryTISAtivos)
elif pais[0:1+2]=="xxx" and report==2:
result = connection.execute(queryTISCancelados)
return result.fetchall();



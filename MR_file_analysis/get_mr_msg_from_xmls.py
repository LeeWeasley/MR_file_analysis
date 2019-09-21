# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 14:55:16 2018
@author: lishuixing
Function of the program:get mr msg from xml files
"""
from xml.dom import minidom
import pandas as pd
from datetime import datetime
import os,re,time

def files_name(file_dir):   
    '''
    功能：读取所有xml_files文件夹下的xml文件
    '''
    list_for_storagexmlfile=[]
    for root, dirs, files in os.walk(file_dir):  
#        print(root) #当前目录路径  
#        print(dirs) #当前路径下所有子目录
#        print (files) #当前路径下所有非目录子文件 
        for xml in files:
            if re.compile(r'\w+.xml').findall(xml):
                list_for_storagexmlfile.append(xml)
    return list_for_storagexmlfile
a=datetime.now()
def get_attrvalue(node, attrname):
     return node.getAttribute(attrname) if node else ''

def get_nodevalue(node, index = 0):
    return node.childNodes[index].nodeValue if node else ''

def get_xmlnode(node, name):
    return node.getElementsByTagName(name) if node else []

def get_xml_data(filename):
    '''
    功能：获取单个xml文件的内容
    '''
    #    doc = minidom.parse("D:\\condas\\Cfiles\\tw项目update0906\\20190916\\xml_files\\"+filename)
    doc = minidom.parse(".\\xml_files\\"+filename)    
    root = doc.documentElement
    enbt = doc.documentElement
    user_nodes = get_xmlnode(root, 'object')    
#for the enbid  script below,enbid属于外层tag，不能与子tag混合
    user_enb   = get_xmlnode(enbt, 'eNB')
    for nod in user_enb:
        enbid  = get_attrvalue(nod, 'id')
#for the enbid  script  above 
    user_list=[]
    for node in user_nodes: 
        #获得tag object下的各个属性值
        user_id = get_attrvalue(node, 'id')
        MmeUeS1apId=get_attrvalue(node, 'MmeUeS1apId')
        MmeGroupId=get_attrvalue(node, 'MmeGroupId')
        MmeCode=get_attrvalue(node, 'MmeCode')
        TimeStamp=get_attrvalue(node, 'TimeStamp')
 #获得对应的tag v的value       
        node_name = get_xmlnode(node, 'v') 
        user_name =get_nodevalue(node_name[0])
 #将获得值存储到一个list中，同时剔除MR.LteScRIP以及MR.LteScPlrULQci两类干扰数据   
        user = [enbid]
        #下列的判断作用1是剔除tag v为空或者NIL的行，2.是为了直接剔除0或者NIL填充经纬度的行
        if  len(user_name)>80:         
            user.append(user_id)
            user.append(MmeUeS1apId)
            user.append(MmeGroupId)
            user.append(MmeCode)
            #user.append(type(TimeStamp))          
            #titan=str(time.mktime(time.strptime(TimeStamp.replace('T',' '), "%Y-%m-%d %H:%M:%S.%f"))).strip()
            #原始的时间戳不准确，python默认只能得到秒级别的戳，但我们需要毫秒级别的，也就是将2018-07-17T23:59:36.932最后小数点作为毫秒级别的最后，小数点前的作为秒级别*1000就得到毫秒了
            titan=int(float(str(time.mktime(time.strptime(TimeStamp.replace('T',' ')[:19], "%Y-%m-%d %H:%M:%S"))).strip())*1000)+int(TimeStamp.replace('T',' ')[-3:])
            user.append(titan)
            a=user_name.split(' ')
            if (a[-2]=='NIL' or float(a[-2])==0):
                pass
            else:
                for x in range(len(a)-1):
                    user.append(a[x])
                user_list.append(user)
    return user_list

filenames=files_name('xml_files')
data_purge=[]
for fis in filenames:
    user_list = get_xml_data(fis)
    for user in user_list :
                    if user:                   
                       data_purge.append(user)
                       
cols=['enbid','CELLID','MME_UE_S1AP_ID','MME_GROUP_ID','MME_CODE','TIMESTAMP','LTESCRSRP','LTESCRSRQ','LTESCTADV','LTESCENBRXTXTIMEDIFF','LTESCPHR','LTESCAOA','LTESCSINRUL','LTESCEARFCN','LTESCPCI','LTENCRSRP','LTENCRSRQ','LTENCEARFCN','LTENCPCI','TDSPCCPCHRSCP','TDSNCELLUARFCN','TDSCELLPARAMETERID','GSMNCELLBCCH','GSMNCELLCARRIERRSSI','GSMNCELLNCC','GSMNCELLBCC','LTESCPUSCHPRBNUM','LTESCPDSCHPRBNUM','LTESCBSR','LTESCRI1','LTESCRI2','LTESCRI4','LTESCRI8','LONGITUDE','LATITUDE']    

datas=pd.DataFrame(data_purge,columns=cols)
#将NIL替换为空白值，dataframe的属性操作是传递的，并不是副本,7月27日发现程序突然卡在datas[datas=='NIL']=' '，暂时只能使用如下替换NIL，效果一样，代码增加，运行时间效率不变。
#datas[datas=='NIL']=' '
datas.loc[datas['LTENCRSRP']=='NIL','LTENCRSRP']=' '
datas.loc[datas['LTENCRSRQ']=='NIL','LTENCRSRQ']=' '
datas.loc[datas['LTENCEARFCN']=='NIL','LTENCEARFCN']=' '
datas.loc[datas['LTENCPCI']=='NIL','LTENCPCI']=' '
datas.loc[datas['TDSPCCPCHRSCP']=='NIL','TDSPCCPCHRSCP']=' '
datas.loc[datas['TDSNCELLUARFCN']=='NIL','TDSNCELLUARFCN']=' '
datas.loc[datas['TDSCELLPARAMETERID']=='NIL','TDSCELLPARAMETERID']=' '
datas.loc[datas['GSMNCELLBCCH']=='NIL','GSMNCELLBCCH']=' '
datas.loc[datas['GSMNCELLCARRIERRSSI']=='NIL','GSMNCELLCARRIERRSSI']=' '
datas.loc[datas['GSMNCELLNCC']=='NIL','GSMNCELLNCC']=' '
datas.loc[datas['GSMNCELLBCC']=='NIL','GSMNCELLBCC']=' '
#datas.to_csv(r'E:\pgtool\Files\results.csv') 不需要index列，更新如下
#datas.to_csv(r'E:\pgtool\Files\MROresult.csv',index=False)
datas.to_csv('MRO_result.csv',index=False)
print('start time---------------',a)
print('end time-----------------',datetime.now())
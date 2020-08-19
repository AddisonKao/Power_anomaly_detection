# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 19:19:32 2020

@author: steve

#####################################################################################
#   Data Structure:                                                                 #
#   data:                                                                           #
#   L-1:                                                                            #
#       [0]:Consumption-O timestamp                                                 #
#       [1]:Consumption-O data                                                      #
#       [2]:Current1-timestamp                                                      #
#       [3]:Current1 data                                                           #
#       [4]:Current2-timestamp                                                      #
#       [5]:Current2 data                                                           #
#       [6]:Power1-timestamp                                                        #
#       [7]:Power1 data                                                             #
#       [8]:Power2-timestamp                                                        #
#       [9]:Power2 data                                                             #
#       [10]:Volt1-timestamp                                                        #
#       [11]:Volt1 data                                                             #
#       [12]:Volt2-timestamp                                                        #
#       [13]:Volt2 data                                                             #
#   L-2:                                                                            #
#       [][0:]:data for 20xx-xx-xx(one day)                                         #
#   L-3:                                                                            #
#       [(if odd) ][][0]:filename                                                   #
#       [(if even)][][0]:0                                                          #
#       [(if odd) ][][1:]:timestamp                                                 #
#       [(if even)][][1:]:Value                                                     #
#####################################################################################
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

def start_day(data):
    long=len(data[0])-1
    s_year=int(data[0][0][0][:4])
    s_month=int(data[0][0][0][5:7])
    s_day=int(data[0][0][0][8:10])
    start=[s_year,s_month,s_day]
    f_year=int(data[0][long][0][:4])
    f_month=int(data[0][long][0][5:7])
    f_day=int(data[0][long][0][8:10])
    finish=[f_year,f_month,f_day]
    return start,finish

def read_and_save(my_path='D:/document/NCTU_sec1/Powermeter/'):
    if(os.path.isfile('output.npy')):
        print("file output.npy existed.\nLoading...\n")
        out=np.load('./output.npy',allow_pickle=True)
        return out
    try:
        Path_o=my_path
        Path_dictionary=['Consumption-O','Current1','Current2','Power1','Power2','Volt1','Volt2',]
        num=0
        total=[]
        total_d=[]
        total_total=[]
        for p_d in Path_dictionary:
            Path_tmp = Path_o+p_d
            My_List = os.listdir(Path_tmp)
            total=[]
            total_d=[]
            for file in My_List:
                df=pd.read_csv(os.path.join(Path_tmp,file))
                tmp=[0]                 #用來對齊
                tmp.extend(df['value'])
                total.append(tmp)
                tmp_d=[file]            #與這個對齊
                tmp_d.extend(df['datetime'])
                total_d.append(tmp_d)
                num+=1
                print(num)
            total_total.append(total_d)
            total_total.append(total)
        out=np.array(total_total)
        print(out[0][100][2])
        np.save('output.npy',out)
        return out
    except:
        raise ValueError("There is an error in read_and_save function\nPlease check your path.")

def draw(my_path='D:/document/NCTU_sec1/Powermeter/',filename='Current1/2018-09-27.csv'):
    try:
        Path_o=my_path
        df=pd.read_csv(os.path.join(Path_o,filename))
        df.plot(title=filename)
        print("File loaded.\nClose picture to start.")
        plt.show()
    except:
        raise ValueError("There is an error in draw function\nPlease check your filename or path.")
def custom_max(data,start_day,end_day,type_key):
    type_key_d=type_key-1
    ans=0
    num=0
    tmp=0
    sum_ans=0
    s_day=0
    e_day=0
    index=[0,0]
    stdev_arr=[]
    for i in range(len(data[type_key_d])):
        if(start_day[0]==int(data[type_key_d][i][0][:4]) and start_day[1]==int(data[type_key_d][i][0][5:7]) and start_day[2]==int(data[type_key_d][i][0][8:10])):
            s_day=i
        if(end_day[0]==int(data[type_key_d][i][0][:4]) and end_day[1]==int(data[type_key_d][i][0][5:7]) and end_day[2]==int(data[type_key_d][i][0][8:10])):
            e_day=i+1
            break
    for i in range(s_day,e_day):
        if(len(data[type_key][i])!=1):
            num+=len(data[type_key][i])-1
            stdev_arr.extend(data[type_key][i][1:])
            sum_ans+=sum(data[type_key][i])
            tmp=max(data[type_key][i])
            if(ans<tmp):
                for x in range(len(data[type_key][i])):
                    if(tmp==data[type_key][i][x]):
                        tmp_index=x
                        break
                ans=tmp
                index=[i,tmp_index]
    print("Var:    \t"+str(np.var(stdev_arr)))
    print("Stdev:  \t"+str(np.std(stdev_arr)))
    print("Average:\t"+str(sum_ans/num))
    print("Count:  \t"+str(num))
    print("Max day: "+str(data[type_key_d][index[0]][index[1]]))
    print("The max from "+str(start_day[0])+"y "+str(start_day[1])+"m "+str(start_day[2])+"d to "+str(end_day[0])+"y "+str(end_day[1])+"m "+str(end_day[2])+"d "+" is "+str(ans))
def my_max(data,year=2018,month=1,key=0,type_key=3):
    if(key==0):
        ans=0
        num=0
        sum_ans=0
        flag=0
        s_day=0
        e_day=0
        type_key_d=type_key-1
        for i in range(len(data[type_key_d])) :
            if(year>int(data[type_key_d][i][0][:4])):
                continue
            elif(year<int(data[type_key_d][i][0][:4])):
                e_day=i
                break
            if(flag==0):
                s_day=i
                flag=1
            num+=len(data[type_key][i])-1
            if(data[type_key][i]!=[]):
                sum_ans+=sum(data[type_key][i])
                tmp=max(data[type_key][i])
                ans=max(tmp,ans)
            else:
                continue
        stdev_arr=[]
        for x in  range(s_day,e_day):
            if(len(data[type_key][x])!=1):
                stdev_arr.extend(data[type_key][x][1:])
        print("Var:    \t"+str(np.var(stdev_arr)))
        print("Stdev:  \t"+str(np.std(stdev_arr)))
        print("Average:\t"+str(sum_ans/num))
        print("Count:  \t"+str(num))
        print("The max in "+str(year)+" is "+str(ans))
    elif(key==1):
        ans=0
        num=0
        sum_ans=0
        s_day=0
        e_day=0
        type_key_d=type_key-1
        index=[0,0]
        flag=0
        for i in range(len(data[type_key_d])) :
            if(year>int(data[type_key_d][i][0][:4])):
                continue
            for j in range(i,len(data[type_key_d])):
                if(month!=int(data[type_key_d][j][0][5:7]) and flag==1):
                    e_day=j
                    break
                if(month>int(data[type_key_d][j][0][5:7])):
                    continue
                if(flag==0):
                    s_day=j
                    flag=1
                if(data[type_key][j]!=[]):
                    num+=len(data[type_key][j])-1
                    sum_ans+=sum(data[type_key][j])
                    tmp=max(data[type_key][j])
                    if(ans<tmp):
                        for x in range(len(data[type_key][j])):
                            if(tmp==data[type_key][j][x]):
                                tmp_index=x
                                break
                        ans=tmp
                        index=[j,tmp_index]#找到最大的index在哪
                else:
                    continue
            break
        stdev_arr=[]
        for x in  range(s_day,e_day):
            if(len(data[type_key][x])!=1):
                stdev_arr.extend(data[type_key][x][1:])
        print("Var     \t"+str(np.var(stdev_arr)))
        print("Stdev:  \t"+str(np.std(stdev_arr)))
        print("Average:\t"+str(sum_ans/num))
        print("Count:  \t"+str(num))
        print("Max day: "+str(data[type_key_d][index[0]][index[1]]))
        print("The max in "+str(year)+"y "+str(month)+"m is "+str(ans))
    #print("max")

def input_day(start_day,finish_day,key):
    def check_day(year,month,day):
        m_d={1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
        if(month>12):
            return False
        elif(month==2):
            if(year%4==0 and day==29):
                return True
        else:
            if(day>m_d[month] or day<1):
                return False
        return True
    
    def error_msg(error_key=0):
        if(error_key):
            print("Something is wrong for input month and day.")
        else:
            print("Error!!The data is out of range!\nRange is from")
            print(str(start_day[0])+"y "+str(start_day[1])+"m "+str(start_day[2])+"d")
            print("to\n"+str(finish_day[0])+"y "+str(finish_day[1])+"m "+str(finish_day[2])+"d")
    while(1):
        if(key==0):
            print("input your start day:")
        elif(key==1):
            print("input your finish day:")
        year=int(input("year:"))
        if(year==0):
            return [0,0,0]
        month=int(input("month:"))
        day=int(input("day:"))
        if(year<start_day[0] or (year==start_day[0] and month<start_day[1]) or (year==start_day[0] and month==start_day[1] and day<start_day[2])):
            error_msg()
        elif(year>finish_day[0] or (year==finish_day[0] and month>finish_day[1]) or (year==finish_day[0] and month==finish_day[1] and day>finish_day[2])):
            error_msg()
        else:
            if(check_day(year,month,day)):
                return [year,month,day]
            else:
                error_msg(error_key=1)

if __name__ == '__main__':
    my_path='D:/document/NCTU_sec1/Powermeter/' #input the path you put the data where named Powermeter in default.
    filename='Current1/2018-09-26.csv'
    data=read_and_save(my_path)
    start_day,finish_day=start_day(data)
    my_start_day=[0,0,0]
    my_finish_day=[0,0,0]
    draw(my_path,filename)
    key=1
    while(key):
        key=input("input 0 to exit\ninput 1 to show data status\ninput 2 to set range\nEnter:")
        if(key==""):
            key=1
            continue
        key=int(key)
        if(key==0):
            print("bye~")
            break
        elif(key==1):
            type_key=2*int(input("Current1 information input 1\nCurrent2 information input 2\nPower1 information input 3\nPower2 information input 4\nVolt1 information input 5\nVolt2 information input 6\nChoose data:"))+1
            year=int(input("year:"))
            month=int(input("(if you want to see year data,input 0)\nmonth:"))
            if(month==0):
                my_max(data,year,month,0,type_key)
            else:
                my_max(data,year,month,1,type_key)
        elif(key==2):
            type_key=2*int(input("Current1 information input 1\nCurrent2 information input 2\nPower1 information input 3\nPower2 information input 4\nVolt1 information input 5\nVolt2 information input 6\nChoose data:"))+1
            my_start_day=input_day(start_day,finish_day,0)
            if(my_start_day[0]==0):
                continue
            my_finish_day=input_day(start_day,finish_day,1)
            if(my_finish_day[0]==0):
                continue
            custom_max(data,my_start_day,my_finish_day,type_key)
        input("Press Enter...")
        

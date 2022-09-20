import pandas as pd
import numpy as np
import streamlit as st
from ast import operator
import asyncio
from cProfile import label
import aiohttp
#############

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
st.title("New Contact !!")

try :
    df=st.file_uploader("فایل نیو کانتکت را وارد کنید")
    df=pd.read_excel(df)
    #st.dataframe(df)
except ValueError:
    pass
df1=pd.read_excel(r"Ameliat.xlsx")

####Calculating New Contact:
try:
    mer=df.merge(df1,on="عاملیت")
except AttributeError:
    pass 
#Date:
i=0
try:
    df["date"]=0
    while (i<(len(df["تاریخ"]))):
        df["date"][i]=df["تاریخ"][i].split("/")[2].split(" ")[0]
        i=i+1
    count=df.groupby(["عاملیت","date"]).count()["شماره موبایل"]
    money=df.groupby(["عاملیت"]).sum()["مبلغ"]
    data=pd.DataFrame(count).reset_index().merge(pd.DataFrame(money),on="عاملیت")
    data=data.merge(df1,on="عاملیت")
    data=data.groupby(["اجرا کننده","date"]).sum()
    st.dataframe(data)
#st.dataframe(data)

except:
    pass


#data.to_excel(r"C:\Users\pcaqw\Desktop\NewContact.xlsx")

#st.write("file is in Your Desktop ... ")

####Calculating Sms:
try :
    df=st.file_uploader("فایل اس مس  را وارد کنید")
    df=pd.read_excel(df)
    #st.dataframe(df)
except ValueError:
    pass

key=pd.read_excel(r"sms key.xlsx")
key["number"]=np.int64(key["number"])
key["sms"]=np.int64(key["sms"])
try:
    sms=pd.DataFrame(df[["شماره دریافت کننده","متن پیامک","مبلغ کل","روز"]])
except TypeError:
    pass
#Date:
try:
    i=0
    sms["day"]=0
    while (i<len(sms["روز"])):
        sms["day"][i]=sms["روز"][i].split('/')[2]
        i=i+1
    sms["شماره دریافت کننده"]=pd.to_numeric(sms["شماره دریافت کننده"],errors='coerce')
    sms["شماره دریافت کننده"]=np.int64(sms["شماره دریافت کننده"])
    sms["متن پیامک"]=pd.to_numeric(sms["متن پیامک"],errors='coerce')
    sms["متن پیامک"]=np.int64(sms["متن پیامک"])
    sms.dropna(subset=["متن پیامک"],inplace=True)
    sms["مبلغ کل"]=sms["مبلغ کل"].fillna(0)
    all=sms.merge(key,left_on=["شماره دریافت کننده","متن پیامک"],right_on=["number","sms"])
    p=pd.DataFrame()
    p["تعداد شماره"]=all.groupby(["person","day"]).count()["شماره دریافت کننده"]
    p["مبلغ کل"]=all.groupby(["person","day"]).sum()["مبلغ کل"]
    st.dataframe(p)
except:
    pass



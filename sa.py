import streamlit as st
import numpy as np
import pandas as pd
import sidetable
import json
base="dark"


def load_data_json():
    return pd.read_json('路外停車資訊.json')
def load_data_excel():
    return pd.read_excel('table.xlsx')
info_column = ['areaId','areaName','parkName','totalSpace','surplusSpace','payGuide','introduction','address','wgsX','wgsY','parkId']
#df.columns=['areaId','areaName','parkName','totalSpace','surplusSpace''payGuide','introduction','address','wgsX','wgsY','parkId','charge']
areaId,areaName,parkName,totalSpace,surplusSpace,payGuide,introduction,address,wgsX,wgsY,parkId = [],[],[],[],[],[],[],[],[],[],[]
df = load_data_json()
charge_df =load_data_excel()

for info in df['parkingLots']:
    areaId.append(info['areaId'])
    areaName.append(info['areaName'])
    parkName.append(info['parkName'])
    totalSpace.append(info['totalSpace'])
    surplusSpace.append(info['surplusSpace'])
    payGuide.append(info['payGuide'])
    introduction.append(info['introduction'])
    address.append(info['address'])
    wgsX.append(info['wgsX'])
    wgsY.append(info['wgsY'])
    parkId.append(info['parkId'])

df1 = pd.DataFrame([areaId,
                    areaName,
                    parkName,
                    totalSpace,
                    surplusSpace,
                    payGuide,
                    introduction,
                    address,
                    wgsX,
                    wgsY,
                    parkId]).T
df1.columns = info_column

charge_df = pd.DataFrame(charge_df['charge'])

df1 = df1.merge(charge_df, how = 'inner', left_index=True, right_index=True)

ops_set = set(df1['areaId'])            #set內容不重複
ops1_set = set(df1['areaName'])
ops_list = list(ops_set)            #各區域選擇
ops1_list = list(ops1_set)
pos_x = 121.2647505
pos_y = 24.9702161

Modes = ['Local','District']
df1['Url'] = ''



#位址網址https://www.google.com.tw/maps/@24.9702161,121.2647505,18z?hl=zh-TW
layout = st.container()
output = st.empty()

with layout:
    st.title("Parking lot management System")
    st.header("PK_dataframe")
output.text("Waiting for your selection......")

form = st.sidebar.form("my_form")
with form:
    Mode = form.radio('SearchMode',Modes)
    AreaName = form.selectbox("District",ops1_list)
    Search_Range = (form.number_input("Input your standard (km)",step=1,format="%d"))/100
    Price = form.slider("Price",min_value=0,max_value=60)
    submitted = st.form_submit_button("Search")
    if submitted and Mode == 'District':        #地區式搜尋
        df1 = df1.loc[df1['areaName'] == AreaName]
    elif submitted and Mode == 'Local':         #定位式搜尋
        df1 = df1.loc[(df1['wgsX'] <= (pos_x + Search_Range))]
        df1 = df1.loc[(df1['wgsX'] >= (pos_x - Search_Range))]
        df1 = df1.loc[(df1['wgsY'] <= (pos_y + Search_Range))]
        df1 = df1.loc[(df1['wgsY'] >= (pos_y - Search_Range))]
    #if submitted and Price != 0:
        #df1 = df1.loc[(df['charge'] <= Price)]

if submitted:
    output.empty()
    output = st.dataframe(df1[['areaName','parkName','surplusSpace','address','charge']])




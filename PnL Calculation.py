# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 10:23:02 2024

@author: TallonCommoditiesINT
"""
import streamlit as st
import pandas as pd


st.set_page_config(layout='wide')
st.title('Position Cash Flow')

file = st.sidebar.file_uploader("Upload Deal Report File", type={"xlsx","xls","csv"}, accept_multiple_files=False)
data = pd.read_excel(file)

data["GMT1"]=""
data["hour1"]=""
data["Minute1"]=""
data["Second1"]=""
data["Trade Date1"]=""

for i in range(0,len(data["Trade Time"])):
    data["GMT1"][i] = data["Trade Time"][i].split()[1]
    if data["GMT1"][i] == "PM":
        data["hour1"][i] = int(data["Trade Time"][i].split()[0].split(":")[0])+13
        data["Minute1"][i] = data["Trade Time"][i].split()[0].split(":")[1]
        data["Second1"][i] = data["Trade Time"][i].split()[0].split(":")[2]
    else:
        data["hour1"][i] = int(data["Trade Time"][i].split()[0].split(":")[0])+1
        data["Minute1"][i] = data["Trade Time"][i].split()[0].split(":")[1]
        data["Second1"][i] = data["Trade Time"][i].split()[0].split(":")[2]
        
    data["Trade Date1"][i] = data["Trade Date"][i].replace(hour =int(data["hour1"][i]), minute = int(data["Minute1"][i]), second = int(data["Second1"][i]))
    
data["Trade Date1"] = pd.to_datetime(data["Trade Date1"])    

data["Code"] = data["Product"] + " " +data["Contract"]


data["Money"]=""

data = data.set_index(data["Trade Date1"])


for i in range(len(data["B/S"])):
    if data["B/S"][i] == "Sold":
        data["Money"][i] = data["Total Quantity"][i]*data["Price"][i]
    else:
        data["Money"][i] = -data["Total Quantity"][i]*data["Price"][i]
        
data["Lot Time"]=""      
for i in range(len(data["B/S"])):
    if data["B/S"][i] == "Sold":
        data["Lot Time"][i] = -data["Lots"][i]
    else:
        data["Lot Time"][i] = +data["Lots"][i]

st.header('Deal Recap')
st.dataframe(data)       


table = pd.DataFrame()

table["PnL"] = data["Money"].groupby(data["Code"]).sum()
table["Quantity"] = data["Lot Time"].groupby(data["Code"]).sum()
table["PnL"].sum()
table["Quantity"].sum()
st.title('Deal Summary')
st.dataframe(table)
st.write("PnL Summary : ",table["PnL"].sum())
st.write("Total Traded Lots : ",table["Quantity"].sum())

table1 = pd.DataFrame()
table1["PnL Time"] = data["Money"].cumsum()
table1["Lots Time"] = data["Lot Time"].cumsum()

st.header('Deal flow')
st.dataframe(table1)

table2 = pd.DataFrame()
table2["Spread Lots"] = data["Lots"].groupby([data["Deal ID"],data["Code"]]).sum()
table2["Spread Pnl"] = data["Money"].groupby([data["Deal ID"],data["Code"]]).sum()
table2["Cash Flow"] = table2["Spread Pnl"].cumsum()

st.header('Spread')
st.dataframe(table2)         
import streamlit as st
import pandas as pd
import json
from time import sleep
# st.write('hi')
@st.cache()
def loadData():
    df = pd.read_csv("1_cat_bus_data.csv")
    df['Time'] = pd.to_datetime(df.Time)
    df = df.sort_values("Time")

    df["latitude"]=df["LatLng.Latitude"]
    df['longitude']=df['LatLng.Longitude']
    return df
df = loadData()


speedOfReplay = st.slider('Speed of replay:',min_value=0,max_value=10,value=0,step=1)
speedOfReplay=speedOfReplay/10

listofbus = list(df.BusId.unique().astype(int).astype(str))
busSelect = st.multiselect('Which bus would you like to track:', listofbus,listofbus)
df = df[df['BusId'].isin(busSelect)]

m = st.map(df)
from datetime import datetime, timedelta
# st.dropdown
# nine_hours_from_now = datetime.now() + timedelta(hours=9)
time = range(0,1000)
timeDisplay = st.info(df['Time'].min())
for t in df['Time'].unique():
    timeDisplay.info(t)
    dfN = df[df['Time'] > t]
    dfN = dfN.groupby('BusId').first()
    m.map(dfN)
    
    sleep(1.1-speedOfReplay)
import streamlit as st
import pandas as pd
import json
from time import sleep

@st.cache()
def loadData():
    df = pd.read_csv("1_cat_bus_data.csv")
    df['Time'] = pd.to_datetime(df.Time)
    df = df.sort_values("Time")

    df["latitude"]=df["LatLng.Latitude"]
    df['longitude']=df['LatLng.Longitude']
    return df
df = loadData().copy()


st.title('Cat bus')

# topGraph = st.map(df)

st.markdown("## Get and inspect")

st.write('To start we will download our dataset from https://www.transperth.wa.gov.au/timetables/live-perth-cat-times and verify it.')

st.write(df.head(3))

st.write('Let see if our data makes sense by plotting all the recordered positional data and in the relevent cat bus color')


df.loc[df['ImageUrl'].str.contains('blueCat'), 'getColorB'] = 255
df.loc[df['ImageUrl'].str.contains('blueCat'), 'RouteCol'] = 'Blue Cat'

df.loc[df['ImageUrl'].str.contains('redCat'), 'RouteCol'] = 'Red Cat'
df.loc[df['ImageUrl'].str.contains('redCat'), 'getColorR'] = 255

df.loc[df['ImageUrl'].str.contains('yellowCat'), 'getColorR'] = 255
df.loc[df['ImageUrl'].str.contains('yellowCat'), 'getColorR'] = 255
df.loc[df['ImageUrl'].str.contains('yellowCat'), 'getColorG'] = 255
df.loc[df['ImageUrl'].str.contains('yellowCat'), 'RouteCol'] = 'Yellow Cat'


df.loc[df['ImageUrl'].str.contains('greenCat'), 'RouteCol'] = 'Green Cat'
df.loc[df['ImageUrl'].str.contains('greenCat'), 'getColorG'] = 255
df['getColorBackground'] = 100
df['radius']=50
dfOriginal = df.copy()

# @st.cache
def drawScatterMapArgs(df):
    return {
        "viewport":{
            'latitude': -31.9505,
            'longitude': 115.8605,
            'zoom': 13,

            'pitch': 0,},
        "layers":[
              {
                'data': df,  
                'raduis':list(df['radius']),
                'type': 'ScatterplotLayer',
                'getColorR':'getColorR',
                'getColorB':'getColorB',
                'getColorG':'getColorG',
                # 'getColorA':'getColorBackground',

            }]}
m=st.deck_gl_chart(drawScatterMapArgs(df))          

from datetime import datetime, timedelta
# m= st.deck_gl_chart()
time = range(0,1000)

playAnimation = st.checkbox('Play animation',value=True)
timeDisplay = st.info(df['Time'].min())

speedOfReplay = st.slider('Speed of replay:',min_value=0,max_value=10,value=10,step=1)
speedOfReplay=speedOfReplay/10

# filter by specific bus
listofbus = list(df.BusId.unique().astype(int).astype(str))
busSelect = st.multiselect('Select which busses to track:', listofbus,listofbus)
df = df[df['BusId'].isin(busSelect)]

from PIL import Image
image = Image.open('catbusmap.jpg')
st.image(image, caption='Our data matches up with the CAT map',use_column_width=True)




st.markdown("## Analysis")
st.write('Lets move on to some analysis. One key aspect of this bus route will be identifying bottlenecks on the route so lets put our bus locations on a heatmap.')
RouteCol = st.radio('Route to visualise',dfOriginal['RouteCol'].unique(), index=0)
df = dfOriginal[dfOriginal['RouteCol']==RouteCol].copy()

st.deck_gl_chart(
    viewport={
                'latitude': -31.9505,
                'longitude': 115.8605,
                'zoom': 13,
               
                'pitch': 0,},
     layers=[{
         'type': 'HexagonLayer',
         'data': df,
         'radius': 150,
         'elevationScale': 4,
         'elevationRange': [0, 300],
         'pickable': True,
         'extruded': True,
     }, {
         'type': 'ScatterplotLayer',
         'data': df,
     }])
     
     
'''
### We can make a couple interesting observations from the data heatmap:

1. Clear "collection point" area where busses are waiting before they start their route.
2. Most busses' "collection point" is at the outskirts of their route (ie. Green Cat is at  leaderville station).
3. Red Cat seems to either have a "collection point" or bottleneck in the middle of it's route on teh corner of Wellington and William.

By focussing on the Red CAT in the animation we it is obvious there is infact a "collection point" at the right most edge of the Red CAT route. What is infact happenlening is because the Red CAT double's back on itself there is twice as much traffic in the middle.

The doubling opnly accounts for, at most, doubling the traffic. This area is clearly a bottleneck, as evident by the 3x-4x higher density of Red CATS on this area.

'''













# animation logic
if playAnimation:
    for t in df['Time'].unique():
        timeDisplay.info(t)
        dfN = dfOriginal[dfOriginal['Time'] > t]
        dfN = dfN.groupby('BusId').first()
        m.deck_gl_chart(drawScatterMapArgs(dfN))          
        sleep(1.1-speedOfReplay)

m.deck_gl_chart(
            viewport={
                'latitude': -31.9505,
                'longitude': 115.8605,
                'zoom': 13,
               
                'pitch': 0,},
            layers = [
                {
                    'data': dfOriginal,
                    'raduis':list(dfOriginal['radius']),
                    'type': 'ScatterplotLayer',
                    'getColorR':'getColorR',
                    'getColorB':'getColorB',
                    'getColorG':'getColorG'
                },
              
                
                ])
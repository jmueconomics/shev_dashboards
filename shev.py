#!/usr/bin/env python3
"""
The purpose of shev.py is to quickly visualize JMU COB and VA Economics Department headcount and graduation data

:: Functions ::
def load_data(path)
  - path: The path to the dataframe

Author(s): Dan Blevins
"""

import streamlit as st
import os
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go

#Read, clean, and cache data
@st.cache(allow_output_mutation=True)
def load_data(path):
    data = pd.DataFrame()
    for folder in os.listdir(path):
        if folder == 'div_data_final.csv':
            div = pd.read_csv(path+'div_data_final.csv',index_col=0)
            #div = pd.read_csv('~/Documents/jmu/schev/dan/data/univs/div_data_final.csv',index_col=0)
        elif folder != '.DS_Store':
            univ_folder = path + folder
            temp = pd.read_csv(univ_folder+'/fall_grad_headcount.csv',index_col=0)
            data = data.append(temp, sort=True)
    return data, div

data, div = load_data('../data/univs/')

#Create Title and sidebar
st.title('Compare JMU Economics against JMU College of Business (COB) and other Economics programs in Virginia')
comparison = st.sidebar.selectbox(
  "I'd like compare JMU Economics to:",
  ('JMU College of Business'
  ,'Other VA Economics Departments')
)
filter_one = st.sidebar.radio(
  "Focusing on:",
  ('Overall Counts'
  , 'Demographics')
)
years = st.sidebar.slider(
  'Looking back through how many years'
  ,4,20
)

#Visualize data
data_year = (max(list(data['year'].unique())) - years)
div_year = (max(list(div['year'].unique())) - years)
data = data[data['year'] >= data_year]
div = div[div['year'] >= div_year]
if comparison == 'JMU College of Business':
    cob = data[data['univ'] == 'jmu']
    if filter_one == 'Overall Counts':
        fig = px.line(cob, x="year", y="fall_perc", color='major', title='Fall Enrollment for each COB Major by Percent')
        st.plotly_chart(fig, use_container_width=True)
        fig = px.line(cob, x="year", y="grad_perc", color='major', title='Graduation Rate for each COB Major by Percent')
        st.plotly_chart(fig, use_container_width=True)
    else:
        div_cob = div[div['univ'] == 'jmu']
        div_cob['bamahu'] = div_cob['perc_black'] + div_cob['perc_alien'] + div_cob['perc_multirace'] + div_cob['perc_asian'] + div_cob['perc_hispanic'] + div_cob['perc_unreported']
        fig = px.line(div_cob, x="year", y='bamahu', color='major', title='Graduation Rate for People of Color (POC)* in COB by Percent')
        st.plotly_chart(fig, use_container_width=True)
        fig = px.line(div_cob, x="year", y="perc_white", color='major', title='Graduation Rate for White in COB by Percent')
        st.plotly_chart(fig, use_container_width=True)
else:
    va = data[data['major'] == 'Econ']

    if filter_one == 'Overall Counts':
        va['va_fall_count'] = va['fall_count'].groupby(va['year']).transform('sum')
        va['va_grad_count'] = va['grad_count'].groupby(va['year']).transform('sum')
        va = va.sort_values(by=['univ', 'year']).reset_index(drop=True)
        va['fall_perc'] = round(va['fall_count']/va['va_fall_count']*100,1)
        va['grad_perc'] = round(va['grad_count']/va['va_grad_count']*100,1)
        fig = px.line(va, x="year", y="fall_perc", color='univ', title='Fall Enrollment for Economics Departments by Percent')
        st.plotly_chart(fig, use_container_width=True)
        fig = px.line(va, x="year", y="grad_perc", color='univ', title='Graduation Rate for Economics Departments by Percent')
        st.plotly_chart(fig, use_container_width=True)
    else:
        div_va = div[div['major'] == 'econ']
        div_va['bamahu'] = div_va['perc_black'] + div_va['perc_alien'] + div_va['perc_multirace'] + div_va['perc_asian'] + div_va['perc_hispanic'] + div_va['perc_unreported']
        fig = px.line(div_va, x="year", y='bamahu', color='univ', title='Graduation Rate for People of Color (POC)* in Economics Departments by Percent')
        st.plotly_chart(fig, use_container_width=True)
        fig = px.line(div_va, x="year", y="perc_white", color='univ', title='Graduation Rate for White in Economics Departments by Percent')
        st.plotly_chart(fig, use_container_width=True)
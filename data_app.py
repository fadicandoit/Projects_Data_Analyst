# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 15:44:49 2023

@author: dell
"""
import streamlit as  st
import pandas as pd
#file = r'C:\Users\dell\Desktop\Karachi.AI\Python\CLASS content\CLASS_2\Billionaire.csv'
#Read the file
df=pd.read_csv('Billionaire.csv')

top_bill = df[df['Rank']==1]

#Find count of billionaires by country
bill_count = df.groupby('Country')[['Name']].count().sort_values(by=['Name'], axis=0, ascending = False).head(10)
st.bar_chart(bill_count)
#Find the most popular source of income 
df.groupby('Source')[['Name']].count().sort_values(by=['Name'], axis=0, ascending = False)
#Get the cumulative wealth of billionaires belonging to US
df['NetWorth'].apply(lambda x: float(x.replace('$','').replace(' B', '')))
USA= df[df['Country']==1]
USA['NetWorth'].sum()

#Interactivity
all_countries= df['Country'].unique()
selection = st.selectbox('Select Country', all_countries)
subset = df[df['Country']==selection]
st.dataframe(subset)

#Container for data (Just like on Tableu)
all_countries = sorted(df['Country'].unique())
col1,col2 = st.columns(2)
selected_country= col1.selectbox('Select your country', all_countries)
subset_country = df[df['Country']== selected_country]

sources= sorted(subset_country['Source'].unique())
#Display on Streamlit
selected_source = col1.multiselect('Select your source of Income', sources)
#subset on selected source
subset_source = subset_country[subset_country['Source'].isin(selected_source)]

#COLUMN 2
main_string ='{} - Billionaires'.format(selected_country)
col2.header(main_string)
col2.table(subset_country)
col2.header('Source Wise Info')
col2.table(subset_source)

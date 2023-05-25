# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 13:57:01 2023

@author: dell
"""

import streamlit as  st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt


st.set_page_config(layout="wide")
st.title('OLYMPIC HISTORY DASHBOARD')
st.header('Created By Fahad Ahmed - Final Assignment')


#Read the file
df1=pd.read_csv('athlete_events.csv')
df2=pd.read_csv('noc_regions.csv')
df2.rename(columns={"region": "Region"}, inplace=True)
df=pd.merge(df1, df2, on="NOC", how="left")
df=df.drop(['ID','notes'],axis=1)
#----------------------------------DATA CLEANING----------------------------------------

df.head()
df.isna().sum() #This gives us the age, weight, height as missing values
data = df[df['Weight'].notnull()&df['Height'].notnull()] #We subset as data after filtering for non-null weight and height
data['Sport'].unique() #Taking all kinds of sports played in the olympics
a=data.groupby('Sport')[['Age']].mean().round(2) #Grouping by sports to the average age of participants
b=a.apply(list).to_dict() #converting groupby data to dictionary 
c=b['Age'] #Taking values for the key[age] which is a dictionary with keys as sports type and mean age as values
data['Age'] = data['Age'].fillna(data['Sport'].map(c)) #This takes keys of dictionary as sports and fills in values of mean ages from dictionary values.
df.isna().sum() #All NaN values are either drop or replaced
data=data.fillna('No Medal') #filling NaN values with No Medal in Medal column for classification
data.duplicated().sum() #This returns all the duplicate values(13 values in total)
#data[data.duplicated()] #Checking the data which is duplicated
data=data.drop(index= [222412,222411,222410,92835,92834,92833,92832,87977,87976,87975,151807,212857,216070]) #This drop rows by index values
data.duplicated().sum() #The result is 0. Data is clean now. 

#                                 We can move to EDA

#---------------------------------EXPLORATORY DATA ANALYSIS----------------------------

#Q1. What are the top 10 countries by participations in the olmpics over the years?

Top_coutries = data.groupby('Region')[['Name']].count().sort_values(by='Name',ascending = False).head(10)
#Country with most athletes is United States.

#Q2. Which Gender has more participants?

Gender = data.groupby('Sex')[['Name']].count().sort_values(by='Name', ascending = False)
round((Gender/data['Sex'].count()) * 100,2)
#Male participant (67.75%) are more than double the female particpants(32.25%)

#Q3. Top 5 athletes with most gold medals won?

Most_gold = data.groupby(['Name','Region'])['Medal'].apply(lambda x: (x=='Gold').sum()).reset_index(name='count').sort_values(by='count',ascending=False).head(5)
#Michael Fred Phelps, has won the most(23) gold medal for his Region 'United States'

#Q4. Which sports had the oldest athletes by average participating and which had the yougest ones?

Avg_ages=data.groupby('Sport')[['Age']].mean().sort_values(by='Age', ascending = False)
Avg_ages.max()
Avg_ages.min()
#We can see that Arts Competetions have highest mean age(41.375yrs) while Rhythmic Gymnastics has lowest age(18.80yrs)

#Q5. What is the avg. Weight and Height for each sports?

avg_WH= data.groupby('Sport').agg(avg_weight=('Weight','mean'),avg_height=('Height','mean'))

#Q6. What is the rate of winning a medal for top 10 winning countries?

M=data[data['Medal']!='No Medal']
athlete_medalcount= M['Name'].nunique()
Medal_win_rate=M.groupby('Region')['Medal'].count().sort_values(ascending=False).head(10)
Rate= (Medal_win_rate/athlete_medalcount)*100
#USA has a total of 21% medal winner of the whole population followed by Russia with 15% athlete of all the medal winners.

#Q7.Which city has hosted most olympic games?

city= data.groupby('City')['Year'].nunique().sort_values(ascending=False)
#Athina and London has hosted most(3) Olympics .
 

#----------------------------VISUALIZATION ON STREAMLIT APP---------------------------------

all_Regions = sorted(data['Region'].unique())
selected_Region= st.selectbox('Select your country', all_Regions)
subset_region= data[data['Region']== selected_Region]
participants= subset_region['Name'].nunique()
subset_gold = data[(data['Region']== selected_Region) & (data['Medal']=='Gold')]
gold=subset_gold['Medal'].count()
subset_silver = data[(data['Region']== selected_Region) & (data['Medal']=='Silver')]
silver=subset_silver['Medal'].count()
subset_bronze = data[(data['Region']== selected_Region) & (data['Medal']=='Bronze')]
bronze=subset_bronze['Medal'].count()
medal_won= data[(data['Region']==selected_Region)&(data['Medal']!='No Medal')]
Bar=medal_won.groupby('Name').agg(Total_Medals_Won=('Medal','count')).head(5)
Table= medal_won.groupby('Name')[['Medal']].count().sort_values(by='Medal', ascending= False).head(5)
Hist= medal_won['Age'].value_counts()
medal_name= medal_won.groupby('Name')['Name'].count().sort_values(ascending=False).head()
season_medal=medal_won.groupby('Season')['Medal'].count().head(5)

col1,col2,col3,col4 = st.columns(4)
col1.metric('Total Participants', participants)
col2.metric('Gold Medals', gold)
col3.metric('Silver Medals',silver)
col4.metric('Bronze Medals', bronze)

with st.container():
    A,B,C= st.columns(3)
    # for dataframe styling, e.g. highlighting max values in a df, refer to the following link: https://docs.streamlit.io/library/api-reference/data/st.dataframe
    g=subset_gold.groupby('Year').agg(Gold=('Medal','count'))
    s=subset_silver.groupby('Year').agg(Silver=('Medal','count'))
    b=subset_bronze.groupby('Year').agg(Bronze=('Medal','count'))
    line= pd.concat([g,s,b],1)
    A.header('Medals Won - Years')
    A.line_chart(line)
    fig, ax=plt.subplots(figsize=(20,15))
    ax= plt.barh(medal_name.index,medal_name.values, color='grey')
    plt.xlabel('No of Medals')
    B.header('Top 5 Medal Winners')
    B.pyplot(fig)
    C.header('Hall of Fame')
    C.table(Table)
    
with st.container():
    D,E,F = st.columns(3)
    fig=plt.figure(figsize=(20,15))
    sns.histplot(medal_won, x='Age',bins=10)
    D.header('Medal vs Age')
    D.pyplot(fig)
    gender= medal_won.groupby(['Medal','Sex'])['Sex'].count()
    fig1, ax1 = plt.subplots()
    ax1.pie(gender, labels = gender.index, autopct='%1.1f%%',shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    E.header('Gender-Wise Winners')
    E.pyplot(fig1)
    figb = plt.figure(figsize=(15,10))
    sns.barplot(season_medal.index,season_medal.values, alpha=0.8)
    F.header('Season Wins')
    F.pyplot(figb)


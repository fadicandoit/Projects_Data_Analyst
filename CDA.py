# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 14:32:06 2023

@author: dell
"""

import streamlit as st
st.header("Greetings")

#take text input
name = st.text_input('Naam Batao?')

#Greet the person
message='Kaisa hai?, ' + name

#add submit buttion
button_press= st.button('Run Me')
if button_press:
    st.text(message)
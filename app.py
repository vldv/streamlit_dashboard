# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 23:34:12 2021

@author: jacqu
"""

import os
import streamlit as st

st.set_page_config(
  page_title="Dashboard",
  layout="wide",
  initial_sidebar_state="expanded",
)

# Session state initialization
if 'current_module' not in st.session_state:
    st.session_state['current_module'] = ''


tool_names = {
              'Finance': ['Asset evolution', 'Stock screener', 'Portfolio analysis'],
              'Servers' : ['Raid status'],
              'Tools' : ['Youtube-dl']
              }


button_value = {}
with st.sidebar:
    st.title('Menu')
    button_value['home'] = st.button("Home")
    for category, tool_list in zip(tool_names.keys(), tool_names.values()):
        st.write(category)
        for name in tool_list:
            button_value[name] = st.button(name)
        
         
#%%
  
with st.sidebar:
    st.write("click pas [ici](https://discuss.streamlit.io/t/hyperlink-in-streamlit-without-markdown/7046/2)")
    if st.button("Cache clear"):
        st.legacy_caching.caching.clear_cache()


for name, is_pressed in zip(button_value.keys(), button_value.values()):
    if is_pressed:
        st.session_state['current_module'] = name.lower()
        
        
if "home" in st.session_state['current_module']:
    from home import main

elif 'portfolio' in st.session_state['current_module']:
    from portfolio import main
    
elif 'screener' in st.session_state['current_module']:
    from screener import main

elif 'raid' in st.session_state['current_module']:
    st.write("todo")

elif 'youtube' in st.session_state['current_module']:
    from youtube_dl import main

else:
    st.write('Welcome! please select a module.')
    def main():
        pass
    
main()

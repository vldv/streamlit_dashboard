# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 08:21:44 2022

@author: Victor Levy dit Vehel, victor.levy.vehel [at] gmail [dot] com
"""

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

def main():
    
    st.subheader('Youtube-dl tool')
        
    links = st.text_area('links of videos to download:', value="enter links here")
        
    print(links)

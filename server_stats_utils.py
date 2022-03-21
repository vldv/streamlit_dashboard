# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 09:00:21 2022

@author: Victor Levy dit Vehel, victor.levy.vehel [at] gmail [dot] com
"""

import subprocess
import pandas as pd
import streamlit as st
import plotly.express as px

#%% general stuff

def whoami():
    """ return hostname """
    return subprocess.Popen("hostname")


def get_confs(path):
    """ load conf file for server stats """
    return None

#%% mandatory checks

def reboot_required():
    """ check wether a system reboot is required """
    out = subprocess.Popen('cat /var/run/reboot-required', shell=True, stdout=subprocess.PIPE).stdout.read()
    if len(out) == 0:
        return False
    else:
        return True


def is_online(address):
    """ ping remote_server to check if online """
    if _ping_rep(address, 1) ==1:
        return True
    else:
        if _ping_rep(address, 3) == 0:
            return False
        else:
            return 0.5
        
        
def _ping_rep(address, n):
    """ ping address n times and return the number of received packets """
    out = subprocess.Popen("ping {} -c {} | grep 'received'".format(address, n))
    return int( out.split('received').split()[-1] )

#%%

def raid_stat():
    return None


def vpn_stat():
    return None

        
def disks_usages(names, pretty_names, remote_server=''):
    """ apply _disk_usage to each name in the list of str 'names' """
    data = {'disk' : [], 'used' : [], 'free' : []}
    for pname, name in zip(pretty_names, names):
        used, free = _disk_usage(name, remote_server)
        data['disk'].append(pname)
        data['used'].append(used / (used+free))
        data['free'].append(free / (used+free))
    diskuse = pd.DataFrame(data)
    fig = px.bar(diskuse, y='disk', x=['used', 'free'], orientation='h')
    fig.update_layout(height=50, showlegend=False, xaxis={'title':None}, yaxis={'side':'right', 'title':None})
    fig.update_layout(margin_t=0, margin_r=100, margin_l=0, margin_b=0)
    st.plotly_chart(fig, use_container_width=True)


def _disk_usage(name, remote_server=''):
    """ return disk usage as tuple of used, free"""
    if remote_server != '':
        out = subprocess.Popen('ssh {} df -h | grep {}'.format(remote_server, name), shell=True, stdout=subprocess.PIPE).stdout.read()
    else:
        out = subprocess.Popen('df -h | grep {}'.format(name), shell=True, stdout=subprocess.PIPE).stdout.read()
    out_split = out.split()
    return int(out_split[2][:-1]), int(out_split[3][:-1])



        
        









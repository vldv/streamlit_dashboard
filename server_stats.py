import streamlit as st
import subprocess
import plotly.express as px
import pandas as pd
import streamlit.components.v1 as components

def main():


    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Haruna")
        loc_u, loc_f = _disk_usage('sda2')
        raid_u, raid_f = _disk_usage('raid')
        data = pd.DataFrame({'disk' : ['local ', 'raid '],
                             'used' : [loc_u/(loc_u+loc_f)*100, raid_u/(raid_u+raid_f)*100],
                             'free' : [loc_f/(loc_u+loc_f)*100, raid_f/(raid_u+raid_f)*100],
                             'values' : [loc_u, raid_u]})

        fig = px.bar(data, y='disk', x=['used', 'free'], orientation='h')
        fig.update_layout(height=50, showlegend=False, xaxis={'title':None}, yaxis={'side':'right', 'title':None})
        fig.update_layout(margin_t=0, margin_r=100, margin_l=0, margin_b=0)
        st.plotly_chart(fig, use_container_width=True)
        if reboot_required():
            st.markdown('reboot required ! \U0000274C')
        else:
            st.markdown('system ok ! :white_check_mark:')
            #components.html("<div style='text-align: center'> system ok ! :white_check_mark: </div>")

    with col2:
        st.subheader("Samidare")
        st.write("disk space")

    with col3:
        st.subheader("Mamiya")
        st.write("disk space")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Nagato")
        st.write("disk space")

    with col2:
        st.subheader("Taihou")
        st.write("disk space")

    with col3:
        st.empty()

def disks_usages(names):
        loc_u, loc_f = disk_usage('sda2')
        raid_u, raid_f = disk_usage('raid')
        data = pd.DataFrame({'disk' : ['local ', 'raid '],
                             'used' : [loc_u/(loc_u+loc_f)*100, raid_u/(raid_u+raid_f)*100],
                             'free' : [loc_f/(loc_u+loc_f)*100, raid_f/(raid_u+raid_f)*100],
                             'values' : [loc_u, raid_u]})

def _disk_usage(name, remote_server=''):
    """ return disk usage as tuple of used, free"""
    if remote_server != '':
        out = subprocess.Popen('ssh {} df -h | grep {}'.format(remote_server, name), shell=True, stdout=subprocess.PIPE).stdout.read()
    else:
        out = subprocess.Popen('df -h | grep {}'.format(name), shell=True, stdout=subprocess.PIPE).stdout.read()
    out_split = out.split()
    return int(out_split[2][:-1]), int(out_split[3][:-1])

def reboot_required():

    out = subprocess.Popen('cat /var/run/reboot-required', shell=True, stdout=subprocess.PIPE).stdout.read()
    if len(out) == 0:
        return False
    else:
        return True


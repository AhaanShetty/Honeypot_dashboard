import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import plotly
import io
import matplotlib.pyplot as plt
import os
import re
import json
import geoip2.database
import dashboard


#Import Snort csv file
data_cowrie = pd.read_csv('data/cowrie_final.csv')
country_cow = pd.read_csv('data/loc_cow.csv',encoding="ISO8859-1")
#ips = data_cowrie['source_ip']

countries = country_cow['Country']
'''
reader = geoip2.database.Reader('data/GeoLite2-City.mmdb')
for ip in ips:
    try:
        response = reader.city(ip)
        countries.append(response.country.name)
    except:
        print("Not found")
reader.close()
'''
#get usernames and passwords
username =[]
password = []

df1 = data_cowrie[['auth_attempts']]
df2 = df1.replace(np.nan, '', regex=True)
col = list(df2.auth_attempts)
col = [i for i in col if i] 
for i in range(len(col)):
    col[i] = col[i].replace('{','').replace('}','').replace('[','').replace(']', '').replace('"', '')
    x = re.split(',', col[i])
    for val in x:
        if 'login' in val:
            username.append(re.split(':', val)[1])
        if 'password' in val:
            password.append(re.split(':', val)[1])

uname = pd.DataFrame(username)
passw = pd.DataFrame(password)
country_names = pd.DataFrame(countries)

def timeofday_cowrie():
    time = list(data_cowrie['timestamp'])
    hr = []

    for i in range(len(time)):
        b = re.split("[T:]", time[i])
        y = int(b[1])

        if y < 12 and y >= 6:
            hr.append("Morning")
        elif y >= 12 and y < 17:
            hr.append("Afternoon")
        elif y >= 17 and y < 20:
            hr.append("Evening")
        elif y >= 20 or y < 6:
            hr.append("Night")

    time_stamp = pd.DataFrame(hr)
    #print(time_stamp)
    timeofday_count = pd.value_counts(time_stamp[0])
    timeofday_ind = timeofday_count.index
    data=[
        go.Pie(
            labels=timeofday_ind, values=timeofday_count
            )
        ]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

def top_usernames(value):
    val = pd.value_counts(uname[0])
    ind = val.index
    x_name = []
    y_count = []
    if value == "5":
        x_name.extend(ind[0:5])
        y_count.extend(val[0:5])
    if value == "10":
        x_name.extend(ind[0:10])
        y_count.extend(val[0:10])
    data=[
            go.Bar(
                    x=x_name,
                    y=y_count,
                    name='Attack',
                    )
        ]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

def top_passwords(value):
    val = pd.value_counts(passw[0])
    ind = val.index
    x_name = []
    y_count = []
    if value == "5":
        x_name.extend(ind[0:5])
        y_count.extend(val[0:5])
    if value == "10":
        x_name.extend(ind[0:10])
        y_count.extend(val[0:10])
    data=[
            go.Bar(
                    x=x_name,
                    y=y_count,
                    name='Attack',
                    )
        ]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

def source_ip_cowrie(value):
    ip_count = pd.value_counts(data_cowrie['source_ip'])
    ip_ind = ip_count.index
    x_name = []
    y_count = []
    if value == "5":
        x_name.extend(ip_ind[0:5])
        y_count.extend(ip_count[0:5])
    if value == "10":
        x_name.extend(ip_ind[0:10])
        y_count.extend(ip_count[0:10])
    data=[
            go.Bar(
                    x=x_name,
                    y=y_count,
                    name='Attack'
                    )
        ]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

def country(value):
    country_count = pd.value_counts(countries)
    country_ind = country_count.index
    x = []
    y=[]
    if value == "5":
        x.extend(country_ind[0:5])
        y.extend(country_count[0:5])
    if value == "10":
        x.extend(country_ind[0:10])
        y.extend(country_count[0:10])
    data=[
            go.Pie(
                    labels=x, values=y
                    )
        ]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

def dest_ports_cowrie(value):
    dest_port_count = pd.value_counts(data_cowrie['destination_port'])
    dest_port_ind = dest_port_count.index
    z = [str(int(item)) for item in dest_port_ind]
    #z = dest_port_ind.astype(object)
    y=list(dest_port_count)
    x_name =[]
    y_count = []
    if value == "5":
        x_name.extend(z[0:5])
        y_count.extend(y[0:5])
    if value == "10":
        x_name.extend(z[0:10])
        y_count.extend(y[0:10])
    data=[
        go.Bar(
                x=x_name,
                y=y_count,
                name='Attack'
            )
        ]
        
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON
    
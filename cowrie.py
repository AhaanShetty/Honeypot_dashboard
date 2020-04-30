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

#get usernames and passwords
# username =[]
# password = []

# df1 = data_cowrie[['auth_attempts']]
# df2 = df1.replace(np.nan, '', regex=True)
# col = list(df2.auth_attempts)
# col = [i for i in col if i] 
# for i in range(len(col)):
#     col[i] = col[i].replace('{','').replace('}','').replace('[','').replace(']', '').replace('"', '')
#     x = re.split(',', col[i])
#     for val in x:
#         if 'login' in val:
#             username.append(re.split(':', val)[1])
#         if 'password' in val:
#             password.append(re.split(':', val)[1])

# uname = pd.DataFrame(username)
# passw = pd.DataFrame(password)
# country_names = pd.DataFrame(countries)

def timeofday_cowrie(data):
    time = data['timestamp']
    #print(data.head)
    hr = []
    #z = re.split("[T:]", time[0])
    #print(z)
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
    timeofday_count = pd.value_counts(time_stamp[0])
    timeofday_ind = timeofday_count.index
    data_graph=[
        go.Pie(
            labels=timeofday_ind, values=timeofday_count
            )
        ]
    graphJSON = json.dumps(data_graph, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

def top_usernames(data):
    value = "5"
    z = [x for x in data['username'] if x]
    val = pd.value_counts(z)
    ind = val.index
    x_name = []
    y_count = []
    if value == "5":
        x_name.extend(ind[0:5])
        y_count.extend(val[0:5])
    if value == "10":
        x_name.extend(ind[0:10])
        y_count.extend(val[0:10])
    data_graph=[
            go.Bar(
                    x=x_name,
                    y=y_count,
                    name='Attack',
                    hovertemplate ='<i>Username</i>: %{x}'+'<br><b>Count</b>: %{y}'
                    )
        ]
    graphJSON = json.dumps(data_graph, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

def top_passwords(data):
    value = "5"
    z = [x for x in data['password'] if x]
    val = pd.value_counts(z)
    ind = val.index
    x_name = []
    y_count = []
    if value == "5":
        x_name.extend(ind[0:5])
        y_count.extend(val[0:5])
    if value == "10":
        x_name.extend(ind[0:10])
        y_count.extend(val[0:10])
    data_graph=[
            go.Bar(
                    x=x_name,
                    y=y_count,
                    name='Attack',
                    hovertemplate ='<i>Password</i>: %{x}'+'<br><b>Value</b>: %{y}'
                    )
        ]
    graphJSON = json.dumps(data_graph, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

def source_ip_cowrie(data):
    value = "5"
    z = [x for x in data['source_ip'] if x]
    ip_count = pd.value_counts(z)
    ip_ind = ip_count.index
    x_name = []
    y_count = []
    if value == "5":
        x_name.extend(ip_ind[0:5])
        y_count.extend(ip_count[0:5])
    if value == "10":
        x_name.extend(ip_ind[0:10])
        y_count.extend(ip_count[0:10])
    data_graph=[
            go.Bar(
                    x=x_name,
                    y=y_count,
                    name='Attack',
                    hovertemplate ='<i>Source IP</i>: %{x}'+'<br><b>Value</b>: %{y}'
                    )
        ]
    graphJSON = json.dumps(data_graph, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

def country_cow(data):
    value = "5"
    z = [x for x in data['country'] if x]
    country_count = pd.value_counts(z)
    country_ind = country_count.index
    x = []
    y=[]
    if value == "5":
        x.extend(country_ind[0:5])
        y.extend(country_count[0:5])
    if value == "10":
        x.extend(country_ind[0:10])
        y.extend(country_count[0:10])
    data_graph=[
            go.Pie(
                    labels=x, values=y
                    )
        ]
    graphJSON = json.dumps(data_graph, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

    
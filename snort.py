import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import plotly
import io
import matplotlib.pyplot as plt
import os
import random
from pathlib import Path
from datetime import datetime
import time
import json

#Import Snort csv file
data_snort = pd.read_csv('data/snort_final.csv')

def get_protocol_graph_snort():
    
    proto_count = pd.value_counts(data_snort['protocol'])
    proto_ind = proto_count.index
    proto_count = list(proto_count)
    data=[
        go.Pie(
            labels=proto_ind, values=proto_count
            )
        ]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

def top_signatures_snort(value):
    
    val = pd.value_counts(data_snort['signature'])
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
                x=y_count,
                y=x_name,
                name='Attack',
                orientation='h'
                )
        ]   
    
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

def source_ip_snort(value):
    ip_count = pd.value_counts(data_snort['source_ip'])
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

def timeofday_snort():
    timeofday_count = pd.value_counts(data_snort['Daytime'])
    timeofday_ind = timeofday_count.index
    timeofday_count = list(timeofday_count)
    data=[
        go.Pie(
            labels=timeofday_ind, values=timeofday_count
            )
        ]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

def attack_types_snort(value):
    attack_count = pd.value_counts(data_snort['attack_type'])
    attack_ind = attack_count.index
    x_name = []
    y_count = []
    if value == "5":
        x_name.extend(attack_ind[0:5])
        y_count.extend(attack_count[0:5])
    if value == "10":
        x_name.extend(attack_ind[0:10])
        y_count.extend(attack_count[0:10])
    data=[
            go.Pie(
                    labels=x_name, values=y_count
                    )
        ]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


def dest_ports_snort(value):
    dest_port_count = pd.value_counts(data_snort['destination_port'])
    dest_port_ind = dest_port_count.index
    z = [str(int(item)) for item in dest_port_ind]
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

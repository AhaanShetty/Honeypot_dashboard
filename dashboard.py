import pandas as pd
import numpy as np
import geoip2.database
from datetime import date
import plotly
import json
import plotly.graph_objects as go
import folium
from folium.plugins import HeatMap
import folium

#reader = geoip2.database.Reader('data/GeoLite2-City.mmdb')
snort = pd.read_csv('data/snort_final.csv')
suricata = pd.read_csv('data/suricata_final.csv')
cowrie = pd.read_csv('data/cowrie_final.csv')

cow = pd.read_csv("data/loc_cow.csv", encoding="ISO8859-1")
suri = pd.read_csv("data/loc_suri.csv", encoding="ISO8859-1")
snor = pd.read_csv("data/loc_snort.csv", encoding="ISO8859-1")

new_cow = cow[cow.Latitude != 'not found']
new_suri = suri[suri.Latitude != 'not found']
new_snort = snor[snor.Latitude != 'not found']
#print(final_loc)
hmap = folium.Map(location=[46.2, 2.2], zoom_start=2.25)

lat_cow = cow['Latitude']
long_cow = cow['Longitude']

lat_snort = snor['Latitude']
long_snort = snor['Longitude']

lat_suri = suri['Latitude']
long_suri = suri['Longitude']

hm = HeatMap(list(zip(new_snort.Latitude, new_snort.Longitude)), radius=3, blur=5, min_opacity=0.9)
hmap.add_child(hm)

hm1 = HeatMap(list(zip(new_cow.Latitude, new_cow.Longitude)), radius=3, blur=5, min_opacity=0.9)
hmap.add_child(hm1)

hm2 = HeatMap(list(zip(new_suri.Latitude, new_suri.Longitude)), radius=3, blur=5, min_opacity=0.9)
hmap.add_child(hm2)

hmap.save("templates/heat.html")

#Date
today = date.today()
today = str(today)

def get_count():
    #Total Count
    total_rows=len(snort.axes[0]) + len(suricata.axes[0]) + len(cowrie.axes[0])
    timestamp_snort = snort['timestamp']
    timestamp_suricata = suricata['timestamp']
    timestamp_cowrie = cowrie['timestamp']
    day=0
    week=0
    month=0
    #For snort
    for x in timestamp_snort:
        time_1 = x[:10]
        f_date = date(int(time_1[:4]), int(time_1[5:7]), int(time_1[8:10]))
        l_date = date(int(today[:4]), int(today[5:7]), int(today[8:10]))
        diff = l_date - f_date
        diff = diff.days
        if diff == 1:
            day = day + 1
        if diff <= 7 and diff>1:
            week = week + 1
        if diff<=30 and diff >7:
            month = month +1
    #For suricata
    for x in timestamp_suricata:
        time_1 = x[:10]
        f_date = date(int(time_1[:4]), int(time_1[5:7]), int(time_1[8:10]))
        l_date = date(int(today[:4]), int(today[5:7]), int(today[8:10]))
        diff = l_date - f_date
        diff = diff.days
        if diff == 1:
            day = day + 1
        if diff <= 7 and diff>1:
            week = week + 1
        if diff<=30 and diff >7:
            month = month +1
    #For cowrie
    for x in timestamp_cowrie:
        time_1 = x[:10]
        f_date = date(int(time_1[:4]), int(time_1[5:7]), int(time_1[8:10]))
        l_date = date(int(today[:4]), int(today[5:7]), int(today[8:10]))
        diff = l_date - f_date
        diff = diff.days
        if diff == 1:
            day = day + 1
        if diff <= 7 and diff>1:
            week = week + 1
        if diff<=30 and diff >7:
            month = month +1

    tot_count = [total_rows,day,week,month]
    return tot_count

def overall_threat_categories():

    df_snort = snort['attack_type']
    df_suricata = suricata['attack_type']
    final_df = pd.concat([df_snort, df_suricata], ignore_index=True)
    attack_count = pd.value_counts(final_df)
    attack_ind = attack_count.index
    x_name = []
    y_count = []
    x_name.extend(attack_ind[0:5])
    y_count.extend(attack_count[0:5])
    data=[
            go.Pie(
                    labels=x_name, values=y_count
                    )
        ]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


'''
response = reader.city('36.81.2.163')
print(response.country.iso_code)
print(response.country.name)
print(response.postal.code)
print(response.subdivisions.most_specific.name)
print(response.city.name)
print(response.location.latitude)
print(response.location.longitude)
reader.close()
'''

import pandas
import numpy
#from ip2geotools.databases.noncommercial import DbIpCity
import geoip2.database
import folium
from folium.plugins import HeatMap

cow = pandas.read_csv("loc_cow.csv", encoding="ISO8859-1")
suri = pandas.read_csv("loc_suri.csv", encoding="ISO8859-1")
snort = pandas.read_csv("loc_snort.csv", encoding="ISO8859-1")

new_cow = cow[cow.Latitude != 'not found']
new_suri = suri[suri.Latitude != 'not found']
new_snort = snort[snort.Latitude != 'not found']

hmap = folium.Map(location=[46.2, 2.2], zoom_start=2.25)


lat_cow = cow['Latitude']
long_cow = cow['Longitude']

lat_snort = snort['Latitude']
long_snort = snort['Longitude']

lat_suri = suri['Latitude']
long_suri = suri['Longitude']




hm = HeatMap(list(zip(new_snort.Latitude, new_snort.Longitude)), radius=3, blur=5, min_opacity=0.9)
hmap.add_child(hm)

hm1 = HeatMap(list(zip(new_cow.Latitude, new_cow.Longitude)), radius=3, blur=5, min_opacity=0.9)
hmap.add_child(hm1)

hm2 = HeatMap(list(zip(new_suri.Latitude, new_suri.Longitude)), radius=3, blur=5, min_opacity=0.9)
hmap.add_child(hm2)

hmap.save("heat.html")


#### OPTIONAL
'''
for i in range(len(lat_cow)):
    if lat_cow[i] != 'not found':
        point = folium.CircleMarker((lat_cow[i], long_cow[i]), fill_color='#43d9de', radius=1)
        hmap.add_child(point)
        hmap.save("finalhm.html")

    print(i)


for i in range(len(lat_snort)):
    if lat_snort[i] != 'not found':
        
        point = folium.CircleMarker((lat_snort[i], long_snort[i]), fill_color='red', color='red', radius=1)
        
        hmap.add_child(point)


    print(i)

hmap.save("tempo.html")

for i in range(len(lat_suri)):
    if lat_suri[i] != 'not found':
        point = folium.CircleMarker((lat_suri[i], long_suri[i]), fill_color='green', color='green', radius=1)
        hmap.add_child(point)


    print(i)


hmap.save("finalmap.html")
print('bye')

'''
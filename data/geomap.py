import pandas

#from ip2geotools.databases.noncommercial import DbIpCity
import geoip2.database
import folium
from folium.plugins import HeatMap
from ip2geotools.databases.noncommercial import DbIpCity



reader = geoip2.database.Reader('GeoLite2-City.mmdb')
hmap = folium.Map(location=[46.2, 2.2], zoom_start=2.25)
loc = []

snort = pandas.read_csv("snort_final.csv")
cow = pandas.read_csv("cowrie_final.csv")
suri = pandas.read_csv('suricata_final.csv')

ips = cow['source_ip']
for ip in ips:
    z=[]
    try:
        response = reader.city(ip)
        z.append(response.location.latitude)
        z.append(response.location.longitude)
        loc.append(z)
    except:
        print("Not found")

reader.close()

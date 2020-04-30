from flask import Flask, render_template,url_for,send_file, request, jsonify
from snort import get_protocol_graph_snort, top_signatures_snort, source_ip_snort,timeofday_snort,attack_types_snort,dest_ports_snort
from suricata import get_protocol_graph_suri,top_signatures_suri,source_ip_suri,timeofday_suri,attack_types_suri,dest_ports_suri
from cowrie import source_ip_cowrie,timeofday_cowrie,top_passwords,top_usernames, country_cow
from dashboard import get_count,overall_threat_categories, get_country_map, getData,getLatestAlerts
#from classify import get_graph
import plotly
import plotly.graph_objects as go
import json
from firebase import firebase
import pandas as pd
#from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

last=0
i=1
country =[]
date=[]
latitude=[]
longitude=[]
username=[]
password=[]
src_ip = []
timestamp=[]

firebase = firebase.FirebaseApplication("https://honeypot-c9793.firebaseio.com/", None)
result = firebase.get("log10/", '')
data ={}

countries = []
layout = go.Layout(
            xaxis_type='category'
        )
lay = json.dumps(layout, cls=plotly.utils.PlotlyJSONEncoder)

layout_class = go.Layout(
    title="Decision Tree Classifier(Blue) vs Random Forest Classifier(Red)",
    xaxis_title="No. of Alerts",
    yaxis_title="Accuracy",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="#7f7f7f"
    )
)
lay1 = json.dumps(layout_class, cls=plotly.utils.PlotlyJSONEncoder)

for i in range(last+1, len(result)):
    x=result[i]
    try:
        username.append(x['username'])
        password.append(x['password'])
    except:
        continue
    try:
        country.append(x['city'])
        latitude.append(result[i]['latitude'])
        longitude.append(result[i]['longitude'])
    except:
        country.append('')
        latitude.append('')
        longitude.append('')
    try:
        src_ip.append(result[i]['src_ip'])
        timestamp.append(result[i]['timestamp'])
        date.append(result[i]['date'])
    except:
        src_ip.append('')
        timestamp.append('')
        date.append('')
temp ={
    'country':country,
    'date':date,
    'latitude':latitude,
    'longitude':longitude,
    'source_ip':src_ip,
    'timestamp':timestamp,
    'username':username,
    'password':password
}
last = i 
data = pd.DataFrame(temp)
temp.clear()

def getDataCowrie():
    #Get cowrie data
    temp={}
    global data
    global last
    global i
    for i in range(last+1, len(result)):
        x=result[i]
        try:
            username.append(x['username'])
            password.append(x['password'])
        except:
            continue
        try:
            country.append(x['city'])
            latitude.append(result[i]['latitude'])
            longitude.append(result[i]['longitude'])
        except:
            country.append('')
            latitude.append('')
            longitude.append('')
        try:
            src_ip.append(result[i]['src_ip'])
            timestamp.append(result[i]['timestamp'])
            date.append(result[i]['date'])
        except:
            src_ip.append('')
            timestamp.append('')
            date.append('')
    temp ={
        'country':country,
        'date':date,
        'latitude':latitude,
        'longitude':longitude,
        'source_ip':src_ip,
        'timestamp':timestamp,
        'username':username,
        'password':password
    }
    last = i
    temp1 = pd.DataFrame(temp)
    data.drop(data.index,inplace =True)
    data = pd.concat([data,temp1],verify_integrity=True)

@app.route('/')
def index():
    # global data
    # getDataCowrie()
    # print(data.head())
    # getData(data)
    # count = get_count()
    # attack_graph = overall_threat_categories()
    # country_graph = get_country_map()
    # print(attack_graph)
    # return render_template('index.html',total_count = count[0],last_day = count[1],last_week = count[2],last_month = count[3],attack_graph = attack_graph,country_graph = country_graph)
    return render_template('index.html')

@app.route('/dashgetdata')
def dash():
    global data
    getDataCowrie()
    getData(data)
    count = get_count(data)
    attack_graph = overall_threat_categories(data)
    country_graph = get_country_map(data)
    alerts = getLatestAlerts(data)
    return jsonify(count = count,att_graph = attack_graph,country_gra = country_graph,alerts= alerts)

@app.route('/snort', methods=['GET','POST'])
def snort():
    proto = get_protocol_graph_snort()
    val = "5"
    sig = top_signatures_snort(val)
    ip = source_ip_snort(val)
    tod = timeofday_snort()
    attacks = attack_types_snort(val)
    dest_port = dest_ports_snort(val)
    return render_template('snort_page.html',protocol = proto,signature_plot = sig,ipaddr = ip,tod=tod,attack = attacks,dest_port = dest_port,layout = lay)

@app.route('/suricata')
def suricata():
    proto = get_protocol_graph_suri()
    val = "5"
    sig = top_signatures_suri(val)
    ip = source_ip_suri(val)
    tod = timeofday_suri()
    attacks = attack_types_suri(val)
    dest_port = dest_ports_suri(val)
    return render_template('suricata_page.html',protocol = proto, signature_plot = sig,ipaddr = ip,tod=tod,attack = attacks,dest_port = dest_port,layout = lay)

@app.route('/cowrie')
def cowrie():
    # global data
    # tod = timeofday_cowrie(data)
    # unames = top_usernames(data)
    # passw = top_passwords(data)
    # ip = source_ip_cowrie(data)
    # country_names = country_cow(data)
    # return render_template('cowrie_page.html', tod = tod,usernames = unames,passwords = passw,ipaddr = ip,country_names = country_names,layout = lay)
    return render_template('cowrie_page.html')

@app.route('/cowriedata')
def cowriedata():
    global data
    tod = timeofday_cowrie(data)
    unames = top_usernames(data)
    passw = top_passwords(data)
    ip = source_ip_cowrie(data)
    country_names = country_cow(data)
    return jsonify(tod = tod,unames = unames,passw = passw,ip = ip,country_names=country_names,layout=lay)

@app.route('/map')
def map():
    return render_template('heat.html')


@app.route('/classification')
def classify():
    # classification_graph = get_graph()
    # print(classification_graph)
    # return render_template('classification_page.html',classification_graph = classification_graph, layout = lay1)
    return render_template('classification_page.html')

@app.route('/correlation')
def corr():
    return render_template('correlation_page.html')

@app.route('/run')
def compute():
    temp={}
    global data
    global last
    global i
    for i in range(last+1, len(result)):
        x=result[i]
        try:
            username.append(x['username'])
            password.append(x['password'])
        except:
            continue
        try:
            country.append(x['city'])
            latitude.append(result[i]['latitude'])
            longitude.append(result[i]['longitude'])
        except:
            country.append('')
            latitude.append('')
            longitude.append('')
        try:
            src_ip.append(result[i]['src_ip'])
            timestamp.append(result[i]['timestamp'])
            date.append(result[i]['date'])
        except:
            src_ip.append('')
            timestamp.append('')
            date.append('')
    temp ={
        'country':country,
        'date':date,
        'latitude':latitude,
        'longitude':longitude,
        'source_ip':src_ip,
        'timestamp':timestamp,
        'username':username,
        'password':password
    }
    last = i
    temp1 = pd.DataFrame(temp)
    #print(len(temp1))
    data.drop(data.index,inplace =True)  
    data = pd.concat([data,temp1],verify_integrity=True)
    print(len(data))
    #data.combine(temp1)
    return "Working Properly"

# sched = BackgroundScheduler(daemon=True)
# sched.add_job(compute,'interval',seconds=5)
# sched.start()

if __name__ == '__main__':
    app.run(debug=True)
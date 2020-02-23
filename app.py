from flask import Flask, render_template,url_for,send_file, request
from snort import get_protocol_graph_snort, top_signatures_snort, source_ip_snort,timeofday_snort,attack_types_snort,dest_ports_snort
from suricata import get_protocol_graph_suri,top_signatures_suri,source_ip_suri,timeofday_suri,attack_types_suri,dest_ports_suri
from cowrie import source_ip_cowrie,dest_ports_cowrie,timeofday_cowrie,top_passwords,top_usernames, country
from dashboard import get_count,overall_threat_categories, get_country_map
import plotly
import plotly.graph_objects as go
import json

app = Flask(__name__)
countries = []
layout = go.Layout(
            xaxis_type='category'
        )
lay = json.dumps(layout, cls=plotly.utils.PlotlyJSONEncoder)
'''
config = go.Layout(
            xaxis_type='category'
        )
lay = json.dumps(layout, cls=plotly.utils.PlotlyJSONEncoder)
'''
@app.route('/')
def index():
    count = get_count()
    attack_graph = overall_threat_categories()
    country_graph = get_country_map()
    return render_template('index.html',total_count = count[0],last_day = count[1],last_week = count[2],last_month = count[3],attack_graph = attack_graph,country_graph = country_graph)

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
    val = "5"
    tod = timeofday_cowrie()
    unames = top_usernames(val)
    passw = top_passwords(val)
    dest_port = dest_ports_cowrie(val)
    ip = source_ip_cowrie(val)
    country_names = country(val)
    return render_template('cowrie_page.html', tod = tod,usernames = unames,passwords = passw,dest_port = dest_port,ipaddr = ip,country_names = country_names,layout = lay)

@app.route('/snort/change',methods=['GET','POST'])
def on_change():
    feature = request.args['selected']
    print(feature)
    sig = top_signatures_snort(feature)
    print(sig)
    return sig

@app.route('/map')
def map():
    return render_template('heat.html')

if __name__ == '__main__':
    app.run(debug=True)
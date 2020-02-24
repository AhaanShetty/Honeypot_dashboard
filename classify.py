import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import plotly
import json
from sklearn import datasets
from sklearn import metrics
from sklearn import tree
from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix
from sklearn.utils import shuffle
import time
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

dataset = pd.read_csv('data/snort_final.csv')

df1 = dataset[['protocol', 'source_ip', 'source_port', 'destination_ip', 'destination_port', 'Sign_id']]

df1['protocol'] = df1['protocol'].map({'TCP':1, 'UDP':2, 'ICMP':3})
df1['source_ip'] = df1['source_ip'].str.replace(".", "")
df1['destination_ip'] = df1['destination_ip'].str.replace(".", "")
df1['source_ip'] = df1['source_ip'].astype('float')
df1['destination_ip'] = df1['destination_ip'].astype('float')
#print(list(df1['source_ip']))

df1 = df1.dropna()

x = df1.drop('Sign_id', axis=1)
y = df1['Sign_id']

t = 500
arr = []
arr1 = []
for i in range(40):

    x1 = x.loc[0:t]
    y1 = y.loc[0:t]
    x_train, x_test, y_train, y_test = train_test_split(x1, y1, random_state=1)

    model = DecisionTreeClassifier()

    t0 = round(time.time(),4)

    model.fit(x_train, y_train)

    t1 = round((time.time() - t0),4)

    #print(model)

    y_predict = model.predict(x_test)

    t2 = round((time.time() - t1 - t0),4)
    #print(y_predict)

    z = accuracy_score(y_test, y_predict)

    #print(z)

    ##### Random Forest CLassifier

    

    RF = RandomForestClassifier()

    t0 =0
    t1 =0
    t2 =0
    #t0 = round((time.time()),4)

    RF.fit(x_train, y_train)
    t1 = round((time.time() - t0),4)
    y_predict = RF.predict(x_test)
    t2 = round((time.time() - t1 - t0),4)

    #print(t1,t2)
    z1 = accuracy_score(y_test, y_predict)

    t = t+500
    arr.append(z*100)
    arr1.append(z1*100)

tem=[]

g = 500
for i in range(40):
    tem.append(g)
    g += 500


def get_graph():
    #fig = go.Figure()

    trace1 = go.Scatter(
        x=tem,
        y=arr,
        name="Decision Tree Classifier"       # this sets its legend entry
        )
    
    trace2 = go.Scatter(
        x=tem,
        y=arr1,
        name="Random Forest Classifier"
        )
  

    data = [trace1,trace2]
   
    graph_json = json.dumps(data,cls = plotly.utils.PlotlyJSONEncoder)
    return graph_json
    
import plotly
# from plotly.graph_objs import Scatter, Layout
import pandas as pd
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go
import socket
import os
import time

#UDP_IP = "10.10.1.15"
#UDP_PORT = 55555
#sock = socket.socket(socket.AF_INET, # Internet
#                     socket.SOCK_DGRAM) # UDP
#sock.bind((UDP_IP, UDP_PORT))


#while True:
#data, addr = sock.recvfrom(2048) # buffer size is 1024 bytes


# df = pd.read_csv('line_data.csv')
df = pd.read_csv("/home/localadmin/MoonGen/histogram.csv",  header=None, skipinitialspace=True, delimiter=',', encoding="utf-8-sig")
df.head()



trace1 = go.Histogram(
                   #x=df['Latency'], y=df['Packets'], # Data
           x=df[0], y=df[1],
          # xbins=dict(
              #     start=2000,
              # end=2200,
              # size=30
          # ),
                   name='Latency Histo' # Additional options
                   )
#trace2 = go.Scatter(
#                    x=df['Time'], y=df['Avg RX Packet Rate'], # Data
#                    mode='lines', name='Avg RX Packet Rate Name' # Additional options
#                   )



layout = go.Layout(title='Forwarding Delay',xaxis=dict(title='Latency (nsec)',titlefont=dict(family='Courier New, monospace',size=18,color='#7f7f7f')),yaxis=dict(title='# of Packets',titlefont=dict(family='Courier New, monospace',size=18,color='#7f7f7f')),plot_bgcolor='rgb(230, 230,230)')

#fig = go.Figure(data=[trace1,trace2], layout=layout)
fig = go.Figure(data=[trace1], layout=layout)

# Plot data in the notebook
# py.iplot(fig, filename='simple-plot-from-csv')

config={'showLink': False}

plotly.offline.plot( { "data": [trace1], "layout": layout }, config=config,  auto_open=False,  filename="/var/www/html/latest.html")
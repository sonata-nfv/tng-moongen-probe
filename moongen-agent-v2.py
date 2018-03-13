import socket
import os
import time
import paramiko
import scpclient
import json


UDP_IP = "10.10.1.15"
UDP_PORT = 33339
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))


sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
        data, addr = sock.recvfrom(2048) # buffer size is 1024 bytes
        data2 = data.split(':')
        print data2
        time.sleep(1)
        #os.system("./moongen-simple start chris:2:3:rate="+data2[2]+"mbit/s,timeLimit="+data2[3])
        os.system("./build/MoonGen moongentest.lua "+data2[5]+" "+data2[6]+" "+data2[3]+" "+data2[2])
        time.sleep(2)

        arrayTX=''
        i=0
        with open('tx.csv') as f:
            for line in f:
                if (i!=0):
                    linehelper = line.split(",")
                    arrayTX = arrayTX + '{"Time": '+str(i-1)+',"Mbit": '+linehelper[4]+',"TotalPackets": '+linehelper[6]+',"TotalBytes": '+linehelper[7][:-1]+'},'
                i = i + 1

        arrayTX = arrayTX[:-1]

        arrayRX = ''
        i=0
        with open('rx.csv') as f:
            for line in f:
                if (i!=0):
                    linehelper = line.split(",")
                    arrayRX = arrayRX + '{"Time": '+str(i-1)+',"Mbit": '+linehelper[4]+',"TotalPackets": '+linehelper[6]+',"TotalBytes": '+linehelper[7][:-1]+'},'
                i = i + 1

        arrayRX = arrayRX[:-1]


        latency = ''
        with open('histogram.csv') as f:
            for line in f:
                linehelper = line.split(",")
                latency = latency + '{"Latency": '+linehelper[0]+',"NumberOfPackets": '+linehelper[1][:-1]+'},'

        latency = latency[:-1]


        resultsJSON = '{"TestID": "'+data2[4]+'","Timestamp": "'+str(time.time())+'","TestConfig": {"Time": '+data2[3]+',"Mbit": '+data2[2]+',"PktSize": 1300,"IpSrc": "10.0.0.10","IpDst": "10.1.0.10","PortSrc": 1234,"PortDst": 319},"Results": {"PktStatsTx": ['+arrayTX+'],"PktStatsRx": ['+arrayRX+'],"LatencyStats": ['+latency+']}}'



        d = json.loads(resultsJSON)

        DataFile = open(data2[4]+".json", "w")
        DataFile.write(json.dumps(d, indent=4, sort_keys=True))
        DataFile.close()

        time.sleep(2)
        print "sending json to orch"
        ssh_client = paramiko.SSHClient()
        ssh_client.load_system_host_keys()
        ssh_client.connect('public_server_ip/hostname', username='myusername', password='mypassword')

        with scpclient.closing(scpclient.Write(ssh_client.get_transport(), '.')) as scp:
            scp.send_file(data2[4]+'.json', remote_filename=data2[4]+'.json')
        time.sleep(2)
        sock2.sendto(data2[4]+".json",("public_server_ip/hostname", 33339))
        print "send done"










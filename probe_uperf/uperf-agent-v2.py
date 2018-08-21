import socket
import os
import time
import paramiko
import json


UDP_IP = "172.16.1.18"
UDP_PORT = 33333
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))


sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
        data, addr = sock.recvfrom(2048) # buffer size is 1024 bytes
        data2 = data.split(':')
        print data2
        time.sleep(1)
        os.environ["rhost"] = "172.16.1.15"
        os.environ["size"] = data2[2]
        os.environ["time"] = data2[3]
        time.sleep(1)
        #os.system("./moongen-simple start chris:2:3:rate="+data2[2]+"mbit/s,timeLimit="+data2[3])
        print("uperf -m kristo.xml -a > myfile.test")
        os.system("uperf -m kristo.xml -a > myfile.test")
        time.sleep(2)


        file = open("myfile.test", "r")
        filedata = file.read()

        splitdata = filedata.split('\n')

        for x in splitdata:
            if ("master" in x):
                helper = x.split(' ')
                helperlist = []
                for y in helper:
                    if (y!=''):
                        helperlist.append(y)
                pktSent=helperlist[2]
                bandwidthSent=helperlist[3]
                operationsSent=helperlist[4]
            if ("172.16.1.15" in x and "Warning" not in x):
                helper = x.split(' ')
                helperlist = []
                for y in helper:
                    if (y!=''):
                        helperlist.append(y)
                pktReceived=helperlist[2]
                bandwidthReceived=helperlist[3]
                operationsReceived=helperlist[4]

        print pktSent
        print bandwidthSent


        print pktReceived
        print bandwidthReceived

        resultsJSON = '{"TestID": "'+data2[4]+'","Timestamp": "'+str(time.time())+'","TestConfig": {"Time": '+data2[3]+',"Size": '+data2[2]+',"PktSize": 43,"IpSrc": "172.16.1.18","IpDst": "172.16.1.15","PortSrc": 0,"PortDst": 0},"Results": {"RateTx": "'+bandwidthSent+'","TotalTx": "'+pktSent+'","RateRx": "'+bandwidthReceived+'","TotalRx":"'+pktReceived+'"}}'



        d = json.loads(resultsJSON)

        DataFile = open(data2[4]+".json", "w")
        DataFile.write(json.dumps(d, indent=4, sort_keys=True))
        DataFile.close()

        time.sleep(2)


        print "json generated"


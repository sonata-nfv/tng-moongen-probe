import socket
import os
import time
import paramiko
import scpclient
import json


UDP_IP = "10.30.0.253"
UDP_PORT = 33333
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))


sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



def runTest(var0, var1,var2,var3,var4,var5):

        if (var5=="64" or var5=="128" or var5=="256" or var5=="512" or var5=="1024" or var5=="1280" or var5=="1518"):
            var0 = var0 + "-" + var5


        print "================================"
        print var0
        print var1
        print var2
        print var3
        print var4
        print var5
        print "================================"

        #os.system("./moongen-simple start chris:2:3:rate="+data2[2]+"mbit/s,timeLimit="+data2[3])
        var5value = int(var5)-18
        print("./build/MoonGen examples/kristo.lua "+var1+" "+var2+" "+var3+" "+var4 +" -s " + str(var5value))
        os.system("./build/MoonGen examples/kristo.lua "+var1+" "+var2+" "+var3+" "+var4+" -s " + str(var5value))
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

        os.system('python shorten.py 35 histogram.csv')

        with open('histogram.csv') as f:
            for line in f:
                linehelper = line.split(",")
                latency = latency + '{"Latency": '+linehelper[0]+',"NumberOfPackets": '+linehelper[1][:-1]+'},'

        latency = latency[:-1]


        resultsJSON = '{"TestID": "'+var0+'","Timestamp": "'+str(time.time())+'","TestConfig": {"Time": '+var3+',"Mbit": '+var4+',"PktSize": '+var5+',"IpSrc": "10.0.0.10","IpDst": "10.1.0.10","PortSrc": 1234,"PortDst": 319},"Results": {"PktStatsTx": ['+arrayTX+'],"PktStatsRx": ['+arrayRX+'],"LatencyStats": ['+latency+']}}'



        d = json.loads(resultsJSON)

        DataFile = open(var0+".json", "w")
        DataFile.write(json.dumps(d, indent=4, sort_keys=True))
        DataFile.close()

        time.sleep(2)
        print "sending json to orch"
        #ssh_client = paramiko.SSHClient()
        #ssh_client.load_system_host_keys()
        #ssh_client.connect('aias.iit.demokritos.gr', username='myusername', password='mypassword')

        #with scpclient.closing(scpclient.Write(ssh_client.get_transport(), '.')) as scp:
        #    scp.send_file(data2[4]+'.json', remote_filename=data2[4]+'.json')
        #time.sleep(2)
        #sock2.sendto(data2[4]+".json",("aias.iit.demokritos.gr", 33339))
        os.system('curl -X POST http://pre-int-sp-ath.5gtango.eu:8000/api/v1/active/service/1235/test/'+var0+'/data -d @'+var0+'.json --header "Content-Type: application/json"')
        os.system('cp '+var0+'.json /var/www/html/latest.json')
        print 'cp '+var0+'.json /var/www/html/latest.json'

        os.system('python /root/plot-bar-csv.py')
        print "send done"




while True:
    data, addr = sock.recvfrom(2048) # buffer size is 1024 bytes
    print data
    data2 = data.split(':')
    print data2
    print "testType -> "+data2[7]
    time.sleep(1)
    if (data2[7]=="simple"):

        runTest(data2[4], data2[5], data2[6][0], data2[3], data2[2], "1300")

    elif (data2[7]=="rfc"):
        print "rfc testing"

        runTest(data2[4], data2[5], data2[6][0], data2[3], data2[2], "64")
        runTest(data2[4], data2[5], data2[6][0], data2[3], data2[2], "128")
        runTest(data2[4], data2[5], data2[6][0], data2[3], data2[2], "256")
        runTest(data2[4], data2[5], data2[6][0], data2[3], data2[2], "512")
        runTest(data2[4], data2[5], data2[6][0], data2[3], data2[2], "1024")
        runTest(data2[4], data2[5], data2[6][0], data2[3], data2[2], "1280")
        runTest(data2[4], data2[5], data2[6][0], data2[3], data2[2], "1518")

    else:
        print "default"

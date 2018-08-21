import socket
import sys
import os
import time

brintport = '2'
brexportin = '2'
brexportout = '1'
breth0portin = '1'
breth0portout = '3'

cloudip = '10.100.33.2'
cloudnetworkid = '5ecd9658-37e3-4a04-bbcc-77e3c1c5150a'


def findPort(mac):
   mac = mac[9:17]
   #print mac
   helper3 = os.popen("ovs-ofctl dump-ports-desc br-int | grep "+mac).read()
   #print helper3
   helping = ""
   for i in range(1,len(helper3)):
      #print helper3[i]
      if (helper3[i]=="("):
          break
      helping = helping+helper3[i]
   #print helping
   return helping
   #return "ok"

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


server_address = (cloudip, 33338)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

while True:
    data, address = sock.recvfrom(4096)
    print >>sys.stderr, data
    datas = data.split(':')
    ingress = datas[0]
    egress = datas[1]
    source = "172.16.1.18"
    destination = "172.16.1.15"


    helper2 = os.popen("neutron port-list | grep "+ingress).read()
    helperarray2 = helper2.split(" ")
    theone2 = ""
    for helperitem2 in helperarray2:
        if "fa:16:3e" in helperitem2:
            theone2 = helperitem2
            print theone2

    ingressport = findPort(theone2)
    print ingressport

    helper2 = os.popen("neutron port-list | grep "+egress).read()
    helperarray2 = helper2.split(" ")
    theone2 = ""
    for helperitem2 in helperarray2:
        if "fa:16:3e" in helperitem2:
            theone2 = helperitem2
            print theone2

    egressport = findPort(theone2)
    print egressport


    if (datas[2]=="start"):

        os.system("ovs-ofctl add-flow br-int priority=102,dl_type=0x800,in_port=341,nw_src="+source+",nw_dst="+destination+",actions=output:"+ingressport)
        os.system("ovs-ofctl add-flow br-int priority=102,dl_type=0x800,in_port="+egressport+",nw_src="+source+",nw_dst="+destination+",actions=output:340")

    else:

        os.system("ovs-ofctl --strict del-flows br-int priority=102,dl_type=0x800,in_port="+brintport+",nw_src="+source+",nw_dst="+destination)
        os.system("ovs-ofctl --strict del-flows br-int priority=102,dl_type=0x800,in_port="+egressport+",nw_src="+source+",nw_dst="+destination)





# MoonGen probe

<p align="center"><img src="https://github.com/sonata-nfv/tng-api-gtw/wiki/images/sonata-5gtango-logo-500px.png" /></p>


#### Description

The MoonGen probe is based on the MoonGen packet generator. It is fully scriptable and it works on high speeds, thus making it suitable for testing various network services. Specific tests for latency and bandwidth are available for the 5G-TANGO V&V Platform. This probe comes with a wrapper API that makes using the MoonGen packet generator automatic and easy. Also there is an automatic openflow-based way to perform traffic steering in OpenStack to guide the generated traffic toward and form the network service that is under test.

#### Files

  - moongen-agent-v3.py is used to manage the MoonGen packet generator, run the test and send the results to the appropriate database.
  - kristo.lua is the actual test that will be run on the system under test.
  - moongenstart.php and moongendone.php are the files that implement the API that is used to communicate with the moongen probe.
  - mg-agentMOONGEN.py is used to apply the SDN rules in the OpenStack in order to perform traffic steering to the network service under test.

#### System Input

To invoke a test a REST HTTP POST request at 10.30.0.253/moongenstart.php is needed. This can be done easily by CURL or POSTMAN. The body of the POST request must be JSON and have the following format as the example: {"ingressIP":"10.0.0.100", "egressIP":"10.0.0.131", "testBandwidth":"10", "testTime":"10", "testID":"mytestid17", "moongenOutput":"2", "moongenInput":"3", "testType":"simple"}

  - ingressIP: ingress IP endpoint of the service under test
  - egressIP: egress IP endpoint of the service under test
  - testBandwidth: bandwidth of the test that will be executed
  - testTime: time in seconds that the test will be executed
  - testID: random ID of the test to be executed
  - moongenOutput: moongen port used to send packets
  - moongenInput: moongen port used to receive packets
  - testType: This has 2 options, simple/rfc, meaning 2 different tests

#### System output

To get the status of a test and some basic measurements there is a GET request in the following format: 10.30.0.253/moongendone.php?tid=mytestid17&ingressip=10.0.0.100&egressip=10.0.0.131

Also a JSON file is produced containing all the measurements of the test. This file is sent to a mongoDB in order to be stored and be available for further analysis. To see the format of the JSON file, there are 2 examples in the folder named results.

#### Requirements

  - A machine with DPDK installed
  - MoonGen packet generator installed
  - Python 2.7
  - Apache2 with PHP enabled
  - An SDN/NFV infrastructure based on OpenStack and SONATA platform

#### Installation

moongen-agent-v3.py and moongentest.lua need to be in the folder of MoonGen. moongen-agent-v3.py needs to be edited in order to have correct IP and PORT depending on the configuration of your network.

To run moongen-agent-v3.py in the background use:

```sh
$ nohup python moongen-agent-v3.py &
```

The files in php-scripts folder must be available under a webserver in the moongen machine. (eg. Apache)

mg-agentMOONGEN.py need to be in the OpenStack machine and must be edited in order to have the correct port interfaces for the OpenStack deployemnt.

To run mg-agentMOONGEN.py in the background use:

```sh
$ nohup python mg-agentMOONGEN.py &
```


License
----

tng-probes is published under Apache 2.0 license. Please see the LICENSE file for more details.


# UPERF probe

<p align="center"><img src="https://github.com/sonata-nfv/tng-api-gtw/wiki/images/sonata-5gtango-logo-500px.png" /></p>


#### Description

The UPERF probe is based on the uperf packet generator. It is fully scriptable and it works on high speeds, thus making it suitable for testing various network services. Specific tests for latency and bandwidth are available for the 5G-TANGO V&V Platform. This probe comes with a wrapper API that makes using the MoonGen packet generator automatic and easy. Also there is an automatic openflow-based way to perform traffic steering in OpenStack to guide the generated traffic toward and form the network service that is under test.

#### Files

  - uperf-agent-v2.py is used to manage the uperf, run the test and send the results to the appropriate database.
  - kristo.xml is the actual test that will be run on the system under test.
  - uperfstart.php and uperfdone.php are the files that implement the API that is used to communicate with the uperf probe.
  - mg-agentUPERF.py is used to apply the SDN rules in the OpenStack in order to perform traffic steering to the network service under test.

#### System Input

To invoke a test a REST HTTP POST request at 10.100.33.119/uperfstart.php is needed. This can be done easily by CURL or POSTMAN. The body of the POST request must be JSON and have the following format as the example: {"ingressIP":"10.0.0.100", "egressIP":"10.0.0.131", "testBandwidth":"1", "testTime":"10", "testID":"mytestid17", "placeholder1":"0", "placeholder2":"0", "testType":"simple"}

  - ingressIP: ingress IP endpoint of the service under test
  - egressIP: egress IP endpoint of the service under test
  - testBandwidth: integer number (1 is approximately 3.2Mb)
  - testTime: time in seconds that the test will be executed
  - testID: random ID of the test to be executed
  - placeholder1: empty field for future use
  - placeholder2: moongen port used to receive packets
  - testType: simple

#### System output

To get the status of a test and some basic measurements there is a GET request in the following format: 10.100.33.119/uperfdone.php?tid=mytestid17&ingressip=10.0.0.100&egressip=10.0.0.131

Also a JSON file is produced containing all the measurements of the test. To see the format of the JSON file, there are 2 examples in the folder named results.

#### Requirements

  - 2 machines with uperf installed
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

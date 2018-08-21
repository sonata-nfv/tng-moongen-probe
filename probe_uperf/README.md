# UPERF probe

<p align="center"><img src="https://github.com/sonata-nfv/tng-api-gtw/wiki/images/sonata-5gtango-logo-500px.png" /></p>


#### Description

The UPERF probe is based on the uperf network performance tool. A test for bandwidth is available for the 5G-TANGO V&V Platform. This probe comes with a wrapper API that makes using the uperf automatic and easy. Also there is an automatic openflow-based way to perform traffic steering in OpenStack to guide the generated traffic toward and form the network service that is under test.

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
  - placeholder2: empty field for future use
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

uperf-agent-v2.py and uperftest.xml need to be in the folder of uperf. uperf-agent-v2.py needs to be edited in order to have correct IP and PORT depending on the configuration of your network.

To run uperf-agent-v2.py in the background use:

```sh
$ nohup python uperf-agent-v2.py &
```

The files in php-scripts folder must be available under a webserver in the uperf master machine. (eg. Apache)

mg-agentUPERF.py need to be in the OpenStack machine and must be edited in order to have the correct port interfaces for the OpenStack deployemnt.

To run mg-agentUPERF.py in the background use:

```sh
$ nohup python mg-agentUPERF.py &
```


License
----

tng-probes is published under Apache 2.0 license. Please see the LICENSE file for more details.

# MoonGen probe

<p align="center"><img src="https://github.com/sonata-nfv/tng-api-gtw/wiki/images/sonata-5gtango-logo-500px.png" /></p>


# Description


#### Files

  - moongen-agent-v3.py is used to manage the MoonGen packet generator, run the test and send the results to the appropriate database.
  - kristo.lua is the actual test that will be run on the system under test.
  - moongenstart.php and moongendone.php are the files that implement the API that is used to communicate with the moongen probe.

#### System Input

To invoke a test a REST HTTP POST request is needed. This can be done easily by CURL or POSTMAN. The body of the POST request must be JSON and have the following format as the example: {"ingressIP":"10.0.0.100", "egressIP":"10.0.0.131", "testBandwidth":"10", "testTime":"10", "testID":"mytestid17", "moongenOutput":"2", "moongenInput":"3", "testType":"simple"}

  - ingressIP
  - egressIP
  - testBandwidth
  - testTime
  - testID
  - moongenOutput
  - moongenInput
  - testType -> dasd

#### System output

A JSON file is produced containing all the measurements of the test. This file is sent to a web server to be available for further usage. To see the format of the JSON file, there are 2 examples in the folder named results.

# Requirements

  - A machine with DPDK installed
  - MoonGen packet generator installed
  - Python 2.7
  - Apache2 with PHP enabled
  - An SDN/NFV infrastructure based on OpenStack and SONATA platform

# Installation

moongen-agent-v3.py and moongentest.lua need to be in the folder of MoonGen. moongen-agent-v3.py needs to be edited in order to have correct IP and PORT depending on the configuration of your network.

To run moongen-agent-v3.py in the background use:

```sh
$ nohup python moongen-agent-v3.py &
```


License
----

tng-probes is published under Apache 2.0 license. Please see the LICENSE file for more details.


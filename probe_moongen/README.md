# MoonGen probe

<p align="center"><img src="https://github.com/sonata-nfv/tng-api-gtw/wiki/images/sonata-5gtango-logo-500px.png" /></p>


# Description

  - moongen-agent-v3.py is used to receive the start test command with test parameters and to send the results back to the the entity that started the test.
  - kristo.lua is the test the actual test that will be run on the system.

#### System Input

To invoke

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


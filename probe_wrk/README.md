# WRK probe

<p align="center"><img src="https://github.com/sonata-nfv/tng-api-gtw/wiki/images/sonata-5gtango-logo-500px.png" /></p>


#### Description

The wrk probe is based on the [wrk2](https://github.com/giltene/wrk2) a HTTP benchmarking tool based mostly on wrk. It is contained inside a docker container ready to be used passing a configuration file via docker volume. It can generate an specific rate of http request to a server in order to stress it and get when in the point where the service starts to degradate.

#### Files

- **config.cfg** is a template of the file that can be used with tng-wrk container. It will be located inside the vnv test package and configured depending on the tests.
- **result.lua** is a lua script to generate the hdrhistogram output in a json format to be parsed by the VnV
- **entrypoint.sh** is the script used to start the wrk inside the container
- **Dockerfile** is the definition of the container creation
- **log_parser.sh** is the script to get the json generated for the VnV

#### System Input

To invoke a test a the VnV will start the container with the config.cfg mounted in the workspace directory. This file will be used to confure the parameters of the test.

- **LogFile** is the place of the result.log
- **DataFile** is the place of the details.json
- **EXTERNAL_IP** is the floating IP of the VNF where wrk will send the requests
- **PORT** is the http where wrk will send the requests
- **CONNECTIONS** Connections to keep open
- **DURATION** Duration of test
- **THREADS** Number of threads to use
- **HEADER**  Add header to request
- **TIMEOUT** Socket/request timeout
- **RATE** work rate (throughput) in requests/sec

#### System output

The output of the test is the raw data of the wrk placed in the file defined in the variable LogFile as result.log and also the hdrhistogram in json format defined in the variable DataFile as details.json

#### Requirements

- Docker Engine
- Config file

#### Usage

It is used in combination with the VnV that will trigger the probe with the command: `docker run --rm -v ./:/workspace sonatanfv/tng-wrk /workspace/config.cfg`

License
----

tng-probes is published under Apache 2.0 license. Please see the LICENSE file for more details.


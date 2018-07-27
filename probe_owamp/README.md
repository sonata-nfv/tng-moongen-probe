# OWAMP (one-way active measurement protocol) to Prometheus

<p align="center"><img src="https://github.com/sonata-nfv/tng-api-gtw/wiki/images/sonata-5gtango-logo-500px.png" /></p>


OWAMP needs to be installed on both hosts taking part in the measurement. The owamp-prometheus-exporter should be installed at the destination host. From there when run, the source host of the one-way-ping can be chosen as an argument.

Configure apt (as user “root”):

    wget -P /etc/apt/sources.list.d/ http://downloads.perfsonar.net/debian/perfsonar-jessie-release.list
    wget -qO - http://downloads.perfsonar.net/debian/perfsonar-debian-official.gpg.key | apt-key add -


Install perfsonar suite, which includes owampd and then run the “install-optional-packages.py” script :

    apt update
    apt install perfsonar-tools

Clone the repository

    git clone 

Install dependencies with pip (using virtual environment is recommended)

    cd owamp-prometheus-exporter
    pip install -r requirements

Run the exporter:

    python3 main.py {SOURCE_HOST_IP}

SOURCE_HOST_IP should be an IP whose host has the package “perfsonar-tools” installed.


Setup Prometheus to monitor the owamp exporter
 In “scrape_config” field add the following:

      - job_name: 'owamp'
        scrape_interval: 10s
        scrape_timeout:  10s
        static_configs:
          - targets: ['10.100.160.45:9101'] # IP and PORT where owamp-prometheus-exporter is exposed

Reload Prometheus (or kill -H {pid}):

    systemctl reload prometheus

*Log rotation not currently implemented, you can use this in cron:

    /usr/bin/find /path/to/owamp-prometheus-exporter/powstream_log_dir -mmin +5 ! -name .powlock -delete


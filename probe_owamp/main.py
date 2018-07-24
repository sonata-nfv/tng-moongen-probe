import os
import argparse
import warnings
from prometheus_client import start_http_server, Metric, REGISTRY
import time
import requests
import socket
import subprocess
import sys

# Base Directory
BASE_DIR = os.path.dirname(__file__)
OWPING_RESULT_DIR = os.path.join(BASE_DIR, 'powstream_log_dir/')
PORT = 9101


def make_log_dir():
    cmd = ['mkdir', "-p", OWPING_RESULT_DIR]
    subprocess.Popen(cmd)

def starts_with(initial_string, string_to_check):
    result = True
    for n, char in enumerate(string_to_check):
        if initial_string is not None:
            if initial_string.__len__() > string_to_check.__len__():
                if initial_string[n] != char:
                    result = False
            else:
                return False
        else:
            return False
    return result


def get_last_result_item(path):
    import os
    sum_list = []
    for root, dirs, files in os.walk(path):
        sum_list = []
        for filename in files:
            step1 = filename.split("_")
            if step1.__len__() > 1:
                step2 = step1[1].split(".")
                if step2.__len__() > 1:
                    if step2[1] == "sum":
                        sum_list.append((step1[0], step2[0]))

    sum_list.sort(key=lambda tup: tup[1], reverse=True)
    result = None
    if sum_list.__len__() > 0:
        return sum_list[0]
    else:
        return None

def get_vals_from_file(the_file):
    min_val = 0.0
    max_val = 0.0
    for line in the_file:
        if starts_with(line, "MIN"):
            min_val = float(line[line.find("\t"):])
        elif starts_with(line, "MAX"):
            max_val = float(line[line.find("\t"):])
    med_val = (max_val+min_val)/2
    return (min_val, med_val, max_val)

def get_hosts_from_file(the_file):
    from_host = "unknown"
    to_host = "unknown"
    for line in the_file:
        if starts_with(line, "FROM_HOST"):
            from_host = line[line.find("\t"):].strip()
        elif starts_with(line, "TO_HOST"):
            to_host = line[line.find("\t"):].strip()
    return (from_host, to_host)


def run_powstream(source_ip):
#    print("powstream -c 100 -i 0.1 -P 8760-9960 -4 -d ./test_dir/ -p {}".format(source_ip))
## TODO: WARNING: powstream[24158]: Warning: Holes in data are likely because lossThreshold(10) is too large a fraction of approx summary session duration(7)
##       needs further investigation
    subprocess.Popen(["/usr/bin/powstream", "-c", "70", "-i", "0.1", "-P", "8760-9960", "-4", "-d", OWPING_RESULT_DIR, "-p", source_ip], stdout=subprocess.PIPE)



class JsonCollector():
    def __init__(self, source_ip):
        try:
            self.source_ip = source_ip
            make_log_dir()
            run_powstream(self.source_ip)
            last_res_item = get_last_result_item(OWPING_RESULT_DIR)
            self.old_filename = ""
            if last_res_item is None:
                raise Exception("No items found! Make sure powstream is running and saving logs in the correct directory. But give it 30sec before you start worrying..")
            self.old_filename = last_res_item[0] + "_" + last_res_item[1] + ".sum"

        except Exception as e:
            print(e)

    def collect(self):

        try:
            metric_owping_min = Metric("net_active_owping_min", 'Active Network Monitoring Metrics', 'gauge')
            metric_owping_avg = Metric("net_active_owping_avg", 'Active Network Monitoring Metrics', 'gauge')
            metric_owping_max = Metric("net_active_owping_max", 'Active Network Monitoring Metrics', 'gauge')

            last_res_item = get_last_result_item(OWPING_RESULT_DIR)
            if last_res_item is None:
                raise Exception("No items found! Make sure powstream is running and saving logs in the correct directory.")

            filename = last_res_item[0] + "_" + last_res_item[1] + ".sum"
            print(filename)
            if filename != self.old_filename:
                self.old_filename = filename
                with open(OWPING_RESULT_DIR + filename, "r") as the_file:
                    hosts = get_hosts_from_file(the_file)
                    print("Source Host : {}".format(hosts[0]))
                    print("Destination Host : {}".format(hosts[1]))
                    the_file.seek(0)
                    vals = get_vals_from_file(the_file)
                    print("MIN is : {}".format(vals[0]))
                    print("MED is : {}".format(vals[1]))
                    print("MAX is : {}".format(vals[2]))

                metric_owping_min.add_sample("net_active_owping_min",
                                            value=vals[0],
                                            labels={'source_ip': hosts[0], "destination_ip": hosts[1]}
                )

                yield metric_owping_min

                metric_owping_avg.add_sample("net_active_owping_avg",
                                            value=vals[1],
                                            labels={'source_ip': hosts[0], "destination_ip": hosts[1]}
                )

                yield metric_owping_avg

                metric_owping_max.add_sample("net_active_owping_max",
                                            value=vals[2],
                                            labels={'source_ip': hosts[0], "destination_ip": hosts[1]}
                )

                yield metric_owping_max

        except Exception as e:
            print(e)



if __name__ == '__main__':
    # Usage: json_exporter.py port endpoint
    start_http_server(PORT)
#    TEST_VAR = sys.argv[1]
    json_collector_instance = JsonCollector(sys.argv[1])
    REGISTRY.register(json_collector_instance)
    #  print(sys.argv[1])
    while True: time.sleep(1)

import logging as log
import ipaddr as ipaddress
import math

# setup logging
LOG_FILENAME="ipam.log"
log.basicConfig(filename=LOG_FILENAME, level=log.DEBUG)
# create console handler and set level to debug
ch = log.StreamHandler()
ch.setLevel(log.DEBUG)
# create formatter
formatter = log.Formatter("%(asctime)s - %(levelname)s - %(message)s")
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
log.getLogger().addHandler(ch)


class IPAddressManager:

    network = ipaddress.IPv4Network("0.0.0.0")

    def __init__(self, network_):
        log.debug("started network: " + network_)
        self.network = ipaddress.IPv4Network(network_)
        self.unallocated = [self.network]

    def add_network(self, size):
        log.debug("begin")
        # 1. parse the unallocated list for a network with sufficient space
        self.get_prefix_for_size(size)
        for test_network in self.unallocated:
            log.debug("network: " + str(test_network) + " has hosts: " + str(test_network.numhosts))
            if test_network.numhosts > size:
                log.debug("network " + str(test_network) + " has sufficient space")

        # 2. break the network that was used to allocate

    def get_prefix_for_size(self, size):
        prefix = 32 - math.ceil(math.log(size, 2))
        log.debug("size: %d prefix length: %d", size, prefix)

ipam = IPAddressManager("192.168.0.0/24")
ipam.add_network(256)
ipam.add_network(512)
ipam.add_network(1024)
ipam.add_network(8000)

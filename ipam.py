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

    def __init__(self, network_):
        log.debug("started network: " + network_)
        self.network = ipaddress.IPv4Network(network_)
        self.allocated = []
        self.unallocated = [self.network]
        self.waiting = []

    def add_network(self, size):
        log.debug("begin")
        prefix = self.get_prefix_for_size(size)
        flag = False
        for test_network in self.unallocated:
            if test_network.prefixlen <= prefix:
                prefix_diff = int(prefix - test_network.prefixlen)
                split_network = test_network.subnet(prefixlen_diff=prefix_diff)
                log.info("Allocated: " + str(split_network[0]))
                self.allocated.append(split_network[0])
                self.unallocated.remove(test_network)
                for i in range(1, prefix_diff + 1):
                    self.unallocated.append((test_network.subnet(prefixlen_diff=i))[1])
                flag = True
                break

        if flag is False:
            log.info("insufficient address space")
            self.waiting.append(size)

        print "====Unallocated===="
        for netw in self.unallocated:
            print netw
        print "====Allocated======"
        for netw in self.allocated:
            print netw
        print "====Waiting========"
        for size in self.waiting:
            print size

    def get_prefix_for_size(self, size):
        prefix = 32 - math.ceil(math.log(size, 2))
        log.debug("size: %d prefix length: %d", size, prefix)
        return prefix

ipam = IPAddressManager("192.168.0.0/23")
ipam.add_network(250)
ipam.add_network(256)
ipam.add_network(256)

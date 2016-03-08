import logging as log
import ipaddr as ipaddress
import math
from operator import itemgetter

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


class IPAM:

    def __init__(self, network_):
        log.debug("started network: " + network_)
        self.network = ipaddress.IPv4Network(network_)
        self.network_view = [self.network]
        self.allocated = []
        self.unallocated = [self.network]
        self.waiting = []

    @staticmethod
    def get_prefix(size):
        prefix = 32 - math.ceil(math.log(size, 2))
        log.debug("size: %d prefix length: %d", size, prefix)
        return prefix

    def add(self, size):
        log.debug("begin")
        prefix = IPAM.get_prefix(size)
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

        self.unallocated.sort()
        self.allocated.sort()
        self.waiting.sort()
        self.network_view = []
        for netw in self.unallocated:
            self.network_view.append([1, netw])
        for netw in self.allocated:
            self.network_view.append([0, netw])
        self.network_view.sort(key=itemgetter(1))

    def show(self):
        print "====Waiting========"
        for size in self.waiting:
            print size
        print "====View==========="
        for netw in self.network_view:
            if netw[0] is 1:
                print '-'*(netw[1].prefixlen - self.network.prefixlen) + str(netw[1]) + " free"
            else:
                print '-'*(netw[1].prefixlen - self.network.prefixlen) + str(netw[1])
        print "====View End======="

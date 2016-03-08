import logging as log
import ipaddr as ipaddress
import math
from operator import itemgetter

# setup logging
LOG_FILENAME="ipam.log"
log.basicConfig(filename=LOG_FILENAME, level=log.DEBUG)
ch = log.StreamHandler()
ch.setLevel(log.DEBUG)
formatter = log.Formatter("%(asctime)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
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
        log.debug("end")

    def show(self):
        print "====Waiting========"
        for size in self.waiting:
            print size
        print "====View==========="
        smallest_prefix = max(netw[1].prefixlen for netw in self.network_view)

        for netw in self.network_view:
            prefix_diff = (netw[1].prefixlen - self.network.prefixlen)
            lines = (smallest_prefix - netw[1].prefixlen)
            if netw[0] is 1:
                print '-'*20
                print '\n'*lines
                print '-'*prefix_diff + "|" + str(netw[1]) + " free"
                # print '\n'*lines
            else:
                print '-'*20
                print '\n'*lines
                print '-'*prefix_diff + "|" + str(netw[1])
                # print '\n'*lines
        print '-'*20
        print "====View End======="

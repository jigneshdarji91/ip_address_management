import logging as log
import socket.ipaddress as ipaddress


class IPAddressManager:

    network = ipaddress.IPv4Network("0.0.0.0")

    def __init__(self, network_):
        log.debug("started network: " + network_)
        self.networknetwork = network_
        self.unallocated.append(self.network)

    def add_network(self, size):
        log.debug("begin")
        #1. parse the unallocated list for a network with sufficient space
        for test_network in self.unallocated:
            if test_network.hosts().size() > size:
                log.debug("test_network " + str(test_network) + " has sufficient space")

        #2. break the network that was used to allocate

from bokeh.plotting import figure, output_file, show
import math
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

graph_width = 1000

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
        self.update()

    def update(self):
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
            lines = int(math.pow(2, (smallest_prefix - netw[1].prefixlen) + 1))
            if netw[0] is 1:
                print '-'*20
                # print '\n'*lines
                print '-'*prefix_diff + "|" + str(netw[1]) + " free"
                # print '\n'*lines
            else:
                print '-'*20
                # print '\n'*lines
                print '-'*prefix_diff + "|" + str(netw[1])
                # print '\n'*lines
        print '-'*20
        print "====View End======="

    def plot(self):
        size = []
        text = []
        free = []
        for i in xrange(0, len(self.network_view)):
            temp_size = 1/(math.pow(2, self.network_view[i][1].prefixlen - self.network.prefixlen))
            size.append(temp_size)
            text.append(str(self.network_view[i][1]))
            free.append(self.network_view[i][0])
        PlotAddressSpace.plot(size, text, free)


class PlotAddressSpace:

    @staticmethod
    def plot(size, text, free):

        print text
        print size
        print free
        data = {
            'left': [],
            'right': [],
            'text': [],
            'color': [],
            'text_center': []
        }

        left = 0
        for i in xrange(0, len(size)):
            data['left'].append(left)
            data['right'].append(left + size[i] * graph_width)
            left = data['right'][i]
            if free[i] is 1:
                data['color'].append("Green")
            else:
                data['color'].append("Yellow")
            data['text'].append(text[i])
            data['text_center'].append((data['right'][i] - data['left'][i])/2 + data['left'][i])

        print data['text']
        output_file("test.html")
        plot = figure(width=graph_width, height=300)
        plot.quad(top=1, bottom=0, left=data['left'], right=data['right'],
                  color=data['color'],
                  name="hello", line_color="black")
        plot.text(x=data['text_center'], y=0.5, angle=math.pi/2, text=data['text'], text_align="center")

        show(plot)

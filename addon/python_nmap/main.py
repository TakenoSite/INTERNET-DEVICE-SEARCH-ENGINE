##!/usr/bin/env python3

from src import Nmap


"""
Thread(
    
    IP:str,       # Target host in list only
    ARGS:str,     # Nmap option
    ThreadNum:int # Thread Select
    TimeOut:int   # TimeOut Count
):

"""

ip_address = ["127.0.0.1", "127.0.0.1"]
opt = "-A"

Nmap.Thread(IP=ip_address, ARGS=opt, ThreadNum=2)

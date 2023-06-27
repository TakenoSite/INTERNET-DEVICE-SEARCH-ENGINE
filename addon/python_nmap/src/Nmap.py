
import nmap 
import threading
import numpy as np
import time 

color0 = "\033[0m"
color1 = "\033[31m"
color2 = "\033[32m"
color3 = "\033[33m"
color4 = "\033[34m"

report_list,ALLReportList = [],[]

class Nmap:
    def __init__(self,**kwargs):

        self.nm = nmap.PortScanner()
        self.ip_address = kwargs["ip"]
        self.protocol = ["tcp", "udp"]
        self.ScanHis = []
    
    
    def scan(self, opt)->bool:
        try:
            self.nm.scan(str(self.ip_address),arguments = opt)
        except:
            return False
        return True

    def report(self):
        self.ScanHis.clear()
        if len(self.nm.all_hosts()) != 0:
            for host in self.nm.all_hosts():
                v1 = self.nm[host]
                v1_keys = v1.keys()
                i_a = v1["addresses"]
                i_a_keys = i_a.keys()

                ip_addresses =[i_a[r] for r in i_a_keys][0]
                
                for r in v1_keys:
                    for proto in self.protocol:
                        if r in proto:
                            v1  = self.nm[host]
                            v2 = v1[proto]
                            v2_keys = v2.keys()
                            
                            port = [ip for ip in list(v2_keys)]

                            for v3 in v2_keys:
                                v4 = v2[v3]
                                v4_keys = v4.keys()
                                v4 = [v4[i] for i in v4_keys]
                                
                                self.ScanHis.append(v4)
        
        try:
            return ip_addresses, port, self.ScanHis, v1
        except:
            ip_addresses = self.ip_address
            port = [0]
            v1  = {"host":0}
            return ip_addresses, port, self.ScanHis, v1



    
    
def RunThread(PROCESS_LIST:list,PROCESS_LIST_LEN:int,IP_LEN:int,ARGS:str):
    
    for IP in PROCESS_LIST:

        print(f"{color3}[~]Scaning ... {IP} {ARGS} {color0}")
        nmap_func = Nmap(ip=IP,args=ARGS)
        if not nmap_func.scan(ARGS):
            print(f"{color1}[!]{color0}Option Value Error e: {ARGS}") 
            return 0 

        scan_report = nmap_func.report()

        IP = scan_report[0]
        PROT = {"port":scan_report[1]}
        REPORT = {"report":scan_report[2]}
        ALL_REPORT = scan_report[3]
        
        print("\033[33m[*]{ip} OK\033[0m".format(ip=IP))
        
        MAIN_REPROT = PROT|REPORT
        DICT_REPORT = {IP:MAIN_REPROT}
        report_list.append(DICT_REPORT)
        ALLReportList.append(ALL_REPORT)

    if IP_LEN == len(report_list):
        resolve_print() 




def Thread(IP:str,ARGS=None,ThreadNum=1,TimeOut=300):
    
    THREAD_NUM = ThreadNum
    IP_LEN = len(IP)
    TIMEOUT = "--host-timeout "+str(TimeOut)
    AddArgs = {

            "timeout":str(TIMEOUT)

            }
    ARGS = str(ARGS) +" "+ str(AddArgs["timeout"])

    THREAD_PROCESS_LIST = np.array_split(IP,ThreadNum)
     
    if len(IP) < THREAD_NUM:
        print("Over Thread .. ")
        return 0

    else:
        for PROCESS_LIST in THREAD_PROCESS_LIST:
            PROCESS_LIST_LEN = len(PROCESS_LIST)     
            TH = threading.Thread(target=RunThread,args=(PROCESS_LIST,PROCESS_LIST_LEN,IP_LEN,ARGS))
            TH.start()
        TH.join() 




def resolve_print(max_print_line = 15):

    report = report_list
    Scan_count = 0

    for v1 in report:
        print('\n\n{f} |{count}|'.format(f='-'*80,count=Scan_count))
        v1_keys = list(v1.keys())
        ip =  list(v1.keys())[0]
        for i in v1_keys:
            v2 = v1[i]
            v2_keys = list(v2.keys())
             
            port = v2['port']
            ScanReport= v2['report']
            ScanPort = port
            Scan_Port_Count = 1

            
            if ScanPort[0] == 0:
                show_info = f"""{color3}

                IP      ===     {ip}
                
                Unavbe to connect
                    
                {color0}"""
                print(show_info)
            
            elif ScanPort[0] == 1:
                show_info= f"""{color3}
                
                IP    ===      {ip}
                
                No opne port
                
                {color0}"""
                print(show_info)
                
                pass 
        
            for ScanPort,ScanReport in zip(ScanPort,ScanReport):
                show_info = f"""{color3}
                
                IP         ===  {ip}
                COUNT      ===  {ScanReport[0]}
                PORT       ===  {ScanPort}
                JOB        ===  {ScanReport[2]}
                JOBNAME    ===  {ScanReport[3]}
                JOBVARSION ===  {ScanReport[4]}

                KEYs       ===  {v2_keys}  
                
                {color0}"""
                print(show_info)
                
                for vuln in ScanReport:
                    if type(vuln)  is dict:
                        vuln_info = list(vuln.keys())
                        
                        for vuln_key in vuln_info:
                            print(f"{color3}                 {vuln[vuln_key]}{color0}")
                
                if Scan_Port_Count == max_print_line:
                    ScanPortLen = len(list(port))
                    print(f"{color3}\n\nOutLine ... Remaining Line are {ScanPortLen}{color0}")
                    break

                Scan_Port_Count += 1
                
        Scan_count += 1



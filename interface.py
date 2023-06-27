import os 
import sys
import time 
import numpy as np 
import json 
import random
import shodan 

import utils.args as ARGS
import utils.string_prop as strprop
import utils.shodan_ctl as shodan_ctl
import utils.ctl_dict as ctl_dict

color0 = "\033[0m"
color1 = "\033[31m"
color2 = "\033[32m"
color3 = "\033[33m"
color4 = "\033[34m"


class AUTH:
    def __init__(self, api_keyfilename="./conf/API_KEYs.txt"):
        self.api_keyfilename = api_keyfilename
        self.api_auth = None
        
        pass 

    def login(self):
        
        login_n = 0

        while 1:
            if os.path.exists(self.api_keyfilename) and os.path.getsize(self.api_keyfilename) > 5 and login_n == 0:
                api_keys = self.read_api_keys()
                #print(api_keys) #debug 

            else:
                api_keys = input(f"{color1}[!]{color0} Please enter valid API KEYs : ")
                self.write_api_keys(value=api_keys)

            print(f"{color3}[~]{color0} API Confirmation..")
            self.api_auth = shodan.Shodan(api_keys)

            try:
                self.api_auth.search("xyz")
                print(f"{color3}[*]{color0} Api Cretification Success :)\n")
                break
            except:
                print(f"{color1}[!]{color0} Accsess Certification Failure :(")
                recovery_set = input("Would you like to start over?  Y/n").strip()
                recovery_set = recovery_set.upper()
                if recovery_set.startswith("Y" or "N"):
                    login_n += 1
                else:
                    return False
            
        return self.api_auth

    def read_api_keys(self):
        api_key_read = open(self.api_keyfilename, "r")
        api_keys = api_key_read.readline().split("\n")[0]
        return api_keys

    def write_api_keys(self, value:str):
        api_key_write = open(self.api_keyfilename, "w")
        api_key_write.write(value)  


class CLI_TEXT_MESSAGE:
    def __init__(self):
        
        self.main_menu_help = """
            shomap  : Search for network-connected devices around the world
            setting : Various settings of the tool
            exiit   : Application Finish
        """
         
        self.conf_menu_help = """
            API : API Config 
            EXIT
            
        """
        
        self.api_setting_menu = """
        
        1 : Show currently displayed APIs
        2 : Reconfigure the API
        3 : exit
        
        """
        
        rand_color = [color1, color2, color3, color4][random.randint(0, 3)]
        self.shomap_menu = f"""{rand_color}
            

       ▄▄▄▄▄    ▄  █ ████▄ ██▄   ██      ▄   
      █     ▀▄ █   █ █   █ █  █  █ █      █  
    ▄  ▀▀▀▀▄   ██▀▀█ █   █ █   █ █▄▄█ ██   █ 
     ▀▄▄▄▄▀    █   █ ▀████ █  █  █  █ █ █  █ 
                  █        ███▀     █ █  █ █ 
                 ▀                 █  █   ██ 
                                  ▀          
                                                    v1.0{color0}"""
        
        self.shomap_help = f"""
    {color1} 
                ##  search  ##
    -k --keys  [keywords]       To specify search keywords
    -l --limit [n]              To specify a limit, use   
    -s --save                   To save the acquired data   
    -f --file  [filenames]      To specify a filename, use
    -p --print [1 or 2 or 3]    

    state, all ,asn ,city ,country, cpe, device, geo, has_ipv6 ,has_screenshot
    has_ssl, has_vuln, hash, hostname, ip ,isp ,link ,net, org, os, port, postal
    product, region, scan, shodan.module, state, version, screenshot.hash, screenshot.label
    cloud.provider, cloud.region, cloud.service, http.component, http.component_category
    http.favicon.hash, http.headers_hash, http.html, http.html_hash, http.robots_hash
    http.securitytxt, http.status, http.title, http.waf, bitcoin.ip, bitcoin.ip_count, bitcoin.port
    bitcoin.version, tag, vuln, ssl, ssl.alpn, ssl.cert.alg, ssl.cert.expired, ssl.cert.extension
    ssl.cert.fingerprint, ssl.cert.issuer.cn, ssl.cert.pubkey.bits, ssl.cert.pubkey.type
    ssl.cert.serial, ssl.cert.subject.cn, ssl.chain_count, ssl.cipher.bits, ssl.cipher.name
    ssl.cipher.version, ssl.ja3s, ssl.jarm, ssl.version, ntp.ip, ntp.ip_count, ntp.more, ntp.port
    telnet.do, telnet.dont, telnet.option, telnet.will, telnet.wont, ssh.hassh, ssh.type


                ##  data  ##
    -s --show                   To open the retrieved data
             
                ##  shodan  ##
    
    alert       Manage the network alerts for your account
    convert     Convert the given input data file into a different format.
    count       Returns the number of results for a search
    data        Bulk data access to Shodan
    domain      View all available information for a domain
    download    Download search results and save them in a compressed JSON...
    honeyscore  Check whether the IP is a honeypot or not.
    host        View all available information for an IP address
    info        Shows general information about your account
    init        Initialize the Shodan command-line
    myip        Print your external IP address
    org         Manage your organization's access to Shodan
    parse       Extract information out of compressed JSON files.
    radar       Real-Time Map of some results as Shodan finds them.
    scan        Scan an IP/ netblock using Shodan.
    search      Search the Shodan database
    stats       Provide summary information about a search query
    stream      Stream data in real-time.
    version     Print version of this tool.

               

        {color0}"""

        pass 

class CLI_INTERFACE:
    def __init__(self, api_auth, api_keys_fname:str):
         
        self.api_auth = api_auth
        self.auth = AUTH(api_keyfilename=api_keys_fname)
        self.cli_text = CLI_TEXT_MESSAGE()
        
        self.dict_data = {}
        self.main_menu()
        pass 
        
    def main_menu(self):

        while 1:
            in_key = input(f"{color3}[$]{color0}Menu > ").strip()
            if strprop.str_comparison((in_key.upper()), ["EXIT","!","QUIT","Q!"]):
                break
            
            elif (in_key.upper()).startswith("SHOMAP"):
                self.shodan_search_func()
                pass 
            
            elif (in_key.upper()).startswith("DATA"):
                ctl_dict.USER_INTERFACE(dict_data=self.dict_data, Mode="SHOMAP").ctl()
                pass 
            
            elif (in_key.upper()).startswith("ADDON"):
                pass 

            elif (in_key.upper()).startswith("SETTING"):
                self.setting_menu()
                pass 
            
            elif (in_key.upper()).startswith("HELP"):
                print(self.cli_text.main_menu_help)
                
            else:
                os.system(in_key)
        
        return 0        
    
    
    def setting_menu(self):
        
        while 1:
            in_key = input(f"{color4}[$]{color0} Setting > ").strip()
            in_key_upper = in_key.upper()
            
            if strprop.str_comparison(in_key_upper, ["EXIT","!","QUIT","Q!"]):
                break
            
            elif in_key_upper.startswith("API"):
                print(self.cli_text.api_setting_menu)
                while 1:
                    in_key = input(f"{color4}[$] API > {color0}").strip()
                    if in_key.startswith("1"):
                        get_api_keys = self.auth.read_api_keys()            
                        print(f"The configured API KEYs are {color3}{get_api_keys}{color0}")

                    elif in_key.startswith("2"):
                        old_apikey = self.auth.read_api_keys()
                        new_apikey = input(f"{color1}[!]{color0} Please enter valid API KEYs : ")
                         
                        self.auth.write_api_keys(new_apikey)
                        login = self.auth.login()
                        
                        if not login:
                            print(f"{color1}[!] Failed to change API KEYs")
                            self.auth.write_api_keys(old_apikey)
                            continue

                        print(f"{color4}[*]{color0} Updated API KEYs{color0}")
                        self.api_auth = login                         
                        
                        pass 
                    elif in_key.startswith("3"):
                        break
                    else:
                        print(f"{color1}[!]{color0}Please select from the above items")

                pass 
            
            elif in_key_upper.startswith("HELP"):
                print(self.cli_text.conf_menu_help)

            ## .. 
        pass
            
    
    def shodan_search_func(self):
        print(self.cli_text.shomap_menu, self.cli_text.shomap_help)
        ctl = shodan_ctl.SHODAN_CTL(self.api_auth) 

        while 1:
            in_key = input(f"{color2} shodan > {color0}").strip()
            if strprop.str_comparison((in_key.upper()), ["EXIT","!","QUIT","Q!"]):
                break

            elif(in_key.startswith("search")):
                resolve = ctl.search(search_keywords=in_key.split("search")[1])
                self.dict_data.update(resolve)
                pass 
            
            elif(in_key.startswith("data")):
                ctl_dict.USER_INTERFACE(dict_data=self.dict_data, Mode="SHOMAP").ctl()
                pass
            
            elif(in_key.startswith("help")):
                print(self.cli_text.shomap_help)
            else:
                os.system(in_key)
        

        pass 
     

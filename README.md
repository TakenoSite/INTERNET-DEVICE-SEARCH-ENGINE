# Internet device search engine


## How to Install
	
	pip install -r requirements.txt


## How to Run

	python application.py


#
## 1 : FIRST STEP
This search tool uses Shodan.

First, please obtain the API from this URL.

  https://developer.shodan.io/    

  
To use the tag search, you must be a member.

For more advanced searches, you will need to subscribe for more subscriptions.


## 2 : SEARCH STEP 
For search function, type menu -> shomap

for a start 
       
       search -k apache -l 50 -p 2 
  
Running this command will output results according to the keywords specified by -k

If you wish to specify a country, 
        
        search -k country:jp product:apache -l 50 -p 2

You can also search in this way.


## 3 : DATA STEP 

Details of the acquired data can be checked with the 
        
      data         
command.

The command control is designed to be more unix  for ease of use.

          

#


## Application Menu 
>>>
    
    # Menu > shomap

>>>



            ▄▄▄▄▄    ▄  █ ████▄ ██▄   ██      ▄
      █     ▀▄ █   █ █   █ █  █  █ █      █
    ▄  ▀▀▀▀▄   ██▀▀█ █   █ █   █ █▄▄█ ██   █
     ▀▄▄▄▄▀    █   █ ▀████ █  █  █  █ █ █  █
                  █        ███▀     █ █  █ █
                 ▀                 █  █   ██
                                  ▀
                                                    v1.0

                ##  search  ##
    -k --keys  [keywords]       To specify search keywords
    -l --limit [n]              To specify a limit, use
    -s --save                   To save the acquired data
    -f --file  [filenames]      To specify a filename, use
    -p -print  [1 or 2 or 3]

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


# 
## Contact Us
This is a demo, and if you need a higher quality tool or want more features, 

please contact us at this e-mail address.

e-mail: takenojob54@gmail.com

## Donation
If you can help us in any way, your donation will encourage us in our future activities!

Bitcoin : 14pTUJDExVn8Dz6y51w6DY3eXLoM83q1nv

Ethernet : 0xcde39cc1fc851b3fdc8a6ca308b41d8f291c2dd1

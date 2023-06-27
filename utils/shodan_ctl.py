import shodan
import json
import sys
import time

try:
    from . import args as args
    from . import ctl_dict as dctl
except:
    import args as args
    import ctl_dict as dctl
 

color0 = "\033[0m"
color1 = "\033[31m"
color2 = "\033[32m"
color3 = "\033[32m"
color4 = "\033[34m"


def search_rsolve_format(dict_data:dict, dict_pach:list, opt:int, line_n:int)->dict:
    
    print_format = "\033[33m[{line_n}]\033[0m \033[34m{port}\033[0m \033[32m{transport}\033[0m \
\033[0m\033[31m{ip_address}\033[0m \033[34m{domain}\033[0m\033[32m {hostname}\033[0m"
    
    dict_flat = dctl.dict_flatting(dict_data, dict_pach) 

    IP_ADDRESS  = dict_flat["ip_str"]
    PORT        = dict_flat["port"]
    TRANSPORT   = dict_flat["transport"]
    DOMAIN      = " ,".join(dict_flat["domains"])
    HOSTNAME    = " ,".join(dict_flat["hostnames"])
    DATA        = dict_flat["data"]

    city            = dict_flat["city"]
    region_code     = dict_flat["region_code"]
    country_name    = dict_flat["country_name"]
    country_code    = dict_flat["country_code"]
    longitude       = dict_flat["longitude"]
    latitude        = dict_flat["latitude"]

    # CONSOLE PRINT 
    if opt == 1 or opt == 2 or opt == 3:
        print(print_format.format(
            line_n      = line_n,
            port        = PORT,
            transport   = TRANSPORT,
            ip_address  = IP_ADDRESS,  
            domain      = DOMAIN,
            hostname    = HOSTNAME ))
    
        if opt == 2 or opt == 3:
            print("  country        : {country_name}".format(country_name = country_name))
            print("  country code   : {country_code}".format(country_code = country_code))
            print("  city           : {city}".format(city = city))
            print("  region code    : {region}".format(region = region_code))
            print("  longitude      : {longitude}.".format(longitude= longitude))
            print("  latitude       : {latitude}".format(latitude= latitude)) 
        
        
        if opt == 3:
            print("\033[38;2;0;255;0m  \n{data}\033[0m".format(data = DATA))

    else:
        pass
    
    return {IP_ADDRESS:dict_data} 

def search_resolve_save(dict_data:dict, filename:str):
    filename = str(filename) + ".json"
    print(f"\n{color3}[+]{color0} save filename is {filename}")
    with open(filename, "wt", encoding="utf-8") as f:
        json.dump(dict_data, f, ensure_ascii=False, indent=2)
        f.close()


class SHODAN_CTL:
    def __init__(self, api_auth):
        
        self.api_auth = api_auth
        self.data_dict = {}
        
        self.location_keynames = [
                "location/city",
                "location/region_code",
                "location/country_name",
                "location/country_code",
                "location/longitude",
                "location/latitude"
                ]
        self.serverinfo_keynames = ['ip_str','port','org',"transport","domains","hostnames","data"] 
        self.index_keynames = self.location_keynames + self.serverinfo_keynames
     
    def search(self, search_keywords:str)->dict:
        self.data_dict.clear()
        
        paser_keywords = args.args_paser(search_keywords)
        
        save_opt        = args.args_search(paser_keywords, ["-s", "--save"])
        file_opt        = args.args_search(paser_keywords, ["-f", "--file"])
        keywords_opt    = args.args_search(paser_keywords, ["-k", "--keys"]) 
        print_opt       = args.args_search(paser_keywords, ["-p", "--print"]) 
        limit_opt       = args.args_search(paser_keywords, ["-l", "--limit"])
        
        if keywords_opt == None:
            print(f"{color1}[!]{color0}-k : please enter search keywords")
            
        if save_opt != None:
            save_opt = True
            
        if limit_opt == None:
            limit_opt = -1
        else:
                
            if len(limit_opt) != 0 and limit_opt[0].isdecimal():
                limit_opt = int(limit_opt[0])
            else:
                limit_opt = -1
        
        if print_opt == None:
            print_opt = 1
        else:
            if print_opt[0].isdecimal():
                print_opt = int(print_opt[0])
            else:
                print_opt = 2

        if file_opt == None:
            file_opt = "".join(keywords_opt)
        else:
            file_opt = file_opt[0]

        
        keywords = " ".join(keywords_opt)
        self.data_dict.update({keywords:{}})
       
        searcha_query = self.api_auth.search_cursor(str(keywords))
        
        print(keywords)
        """ DEBUG 
        open_dict_file = open("search_raw.json", "r")
            searcha_query = json.load(open_dict_file)

        print(f"save_opt is {save_opt}\nfile_ope is {file_opt}\nkeywords_opt is \
{keywords_opt}\nprint_opt is {print_opt}\nlimit_opt is {limit_opt}\nkeywords is {keywords}") # debug 
        
        try:
            line_n =0
            for i in range(2<<1000):
                search_resolve = search_rsolve_format(searcha_query, opt=print_opt, dict_pach=self.index_keynames, line_n=line_n)
                self.data_dict[keywords].update(search_resolve)
                
                if line_n == limit_opt:
                    break
                
                time.sleep(1e-2)
                line_n += 1
                pass 
            
        except:
            print("finish")
            pass 
        """ 
        try:
            line_n =0
            for i in searcha_query:
                search_resolve = search_rsolve_format(i, opt=print_opt, dict_pach=self.index_keynames, line_n=line_n)
                self.data_dict[keywords].update(search_resolve)
                
                if line_n == limit_opt:
                    break
                
                time.sleep(1e-2)
                line_n += 1
                pass 
            
        except:
            print(f"search results : {line_n}")
            pass 
         
        if save_opt != None:
            search_resolve_save(dict_data=self.data_dict, filename=file_opt)

        return self.data_dict

if __name__ == "__main__":
    # TESTs

    api_auth = shodan.Shodan("mdJK40LYOaS1OVYs3BNxfPCrLmz6KN4P")
    
    try:
        api_auth.search("xyz")
        print("Accept")
    except:
        print("api error")
        sys.exit()        

    search_keywords = "-k country:ru ssh -l 10 -p 2"
    
    res = SHODAN_CTL(api_auth)
    res = res.search(search_keywords)
    
    pass


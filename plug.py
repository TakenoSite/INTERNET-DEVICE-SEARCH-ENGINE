import utils.ctl_dict as dctl
import utils.args as args
import addon.python_nmap.src.Nmap as netmap


color0 = "\033[0m"
color1 = "\033[31m"
color2 = "\033[32m"
color3 = "\033[33m"
color4 = "\033[34m"


class ADDON_CMD_PROCESS(dctl.CMD_PROCESS):
    def __init__(self, dict_data:dict, cmd:list):
        self.cmd = cmd
        self.dict_data = dict_data
        super.__init__()
        
        
    def addon_cmd_process(self):
        if self.cmd[0] == "nmap":
            self.nmap(nmap_cmd_value=self.cmd[1])
        pass 

    def nmap(self, nmap_cmd_value):
        nmap_cmd_paser = args.args_paser(" ".join(nmap_cmd_value[1:])) 
        target_host = args.args_search(nmap_cmd_paser, ["-h", "--host"])
        thread_opt  = args.args_search(nmap_cmd_paser, ["-t", "--thread"])
        
        if target_host == None and len(target_host) == 0:
            print(f"{color1}[!]{color0}Enter target host -h")
            return 0
        else:
            nmap_cmd_paser = args.args_deletes(nmap_cmd_paser, ["-h", "--host"])
        
        if thread_opt == None and len(thread_opt) == 0 and not thread_opt[0].isdecimal():
            print(f"{color1}[!]{color0}Enter thread num -t [n]")
            return 0

        else:
            nmap_cmd_paser = args.args_deletes(nmap_cmd_paser, ["-t", "--thread"])
        
        
        #残りをnmap のオプションとする
        nmap_opt = args.args_to_str(nmap_cmd_paser)
        netmap.Thread(IP=target_host, ARGS=nmap_opt, ThreadNum=thread_opt) 
        pass

    


class ADDON_PLUGS:
    def __init__(self, dict_data:dict):
        self.dict_data = dict_data

        pass

    def nmap_plug(self, args:str):
        
        


        pass



if __init__ == "__main__":


    pass 
    








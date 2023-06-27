import os 
import json

try:
    from . import args
    from . import string_prop as strprop

except:
    import args
    import string_prop as strprop

 

color0 = "\033[0m"
color1 = "\033[31m"
color2 = "\033[32m"
color3 = "\033[33m"
color4 = "\033[34m"

## 
dict_pass           = []
dict_search_keys    = []
dict_search_value   = {}


# add 
dict_add_file_list = {}

##

def route_pass(dict_data:dict):
    x,y=0,1
    dict_a = dict_data
    for i in dict_pass:
        if x == 0:
            dict_b = dict_a[i]
            x += 1
        
        elif x == y:
            dict_b = dict_b[i]
            y += 1
        
        elif x != y:
            dict_b = dict_b[i]
            x += 1
    
    dict_keys  = list(dict_b.keys())
    dict_value = dict_b
    
    return dict_keys, dict_value



def dict_flatting(dict_data:dict, dict_pach:list)->dict:
    if type(dict_pach) == list:
        res_dict = {}
        for i in dict_pach:
            
            pach = i.split("/")
            dataname = pach[len(pach)-1]
            x,y = 0,1
            dict_a = dict_data
            try:
                for i in pach:
                    if x == 0:
                        dict_b = dict_a[i]
                        x += 1
                    
                    elif x == y:
                        dict_b = dict_b[i]
                        y += 1
                    
                    elif x != y:
                        dict_b = dict_b[i]
                        x += 1
                i = dict_b
                update_dict = {str(dataname):i}
                res_dict.update(update_dict)
            except:
                print(f"{color1}[!]{color0}Specified pach does not exist.")
        return res_dict


class OPEN_DICT:
    def __init__(self, dict_data:dict):
        if len(dict_pass) != 0:
            dict_data = route_pass(dict_data)[1]
        
        self.dict_keys = dict_data.keys()
        self.dict_data = dict_data
        
        self.dict_all_key_name  = []
        self.dict_key_pass = []
        self.dict_key_word = []

        self.line_couint = 0
   
    def all_keyname(self):
        self.dict_all_key_name.clear()
        
        for i in list(self.dict_keys):
            solve_dict = self.dict_data[i]
            self.dict_key_pass.append(i)

            self.dict_development(dict_data=solve_dict, keys=self.dict_keys, func_n=2)

        return self.dict_all_key_name

  
    def all_open(self):
         
        for i in list(self.dict_keys):
            solve_dict = self.dict_data[i]
            self.dict_key_pass.append(i)

            self.dict_development(dict_data=solve_dict, keys=self.dict_keys, func_n=1)
        pass 
    
    
    def search(self, search_format:dict)->dict:
        
        self.search_format = search_format
        
        self.hitdict_list   = []
        self.search_result  = {}

        
        #search_keys = list(self.search_format.keys())
        #for i in search_keys:
        #    search_words = self.search_format[i]
        #    for j in search_words:
        #        print(i, j)

        for i in list(self.dict_keys):
            point_dict      = self.dict_data[i]
            point_dict_keys = point_dict.keys()

            for j in point_dict_keys:
                search_dict = point_dict[j]
                self.line_couint = 0
                self.dict_key_pass.clear()
                self.dict_key_pass.append(j)
                
                #solve
                self.dict_development(search_dict, keys=self.dict_keys, 
                        func_n=3, search_dict=search_dict)
        
        print(f"result_len {len(self.hitdict_list)}") # debug
        
        if len(self.hitdict_list) != 0:
            search_register_value = []
            search_register_id = [search_register_value.append(str(i)+"_"+str("_".join(search_format[i]))) for i in list(search_format.keys())]
            search_register_id = " ".join(search_register_value)

            register_format     = {search_register_id:self.search_result}
            dict_search_value.update(register_format) 
        
        return self.hitdict_list, self.search_result


    def dict_development(self, dict_data:dict, keys:list, func_n=None, search_dict=None):
        self.line_couint += 1
        # core area
        if type(dict_data) is dict:
            dict_keys = dict_data.keys()
            for i in list(dict_keys):
                solve_dict = dict_data[i]
                self.dict_key_pass.append(i)
                
                self.dict_development(dict_data=solve_dict, 
                        keys=i, func_n=func_n, search_dict=search_dict)
         
        else:
        # application area
            if func_n == 1:   # PRINT 
                print(f"{'-'*80}+{self.line_couint}\n{color3}{keys} \n{dict_data}{color0}")
                pass 
            
            elif func_n == 2: # KEYNAMES
                n = True
                for i in self.dict_all_key_name:
                    if i == keys:
                        n = False
                        break
                    
                    n = True
                    
                if n:
                    self.dict_all_key_name.append(keys)
                pass  
            
            elif func_n == 3: # SEARCH 
                
                def search_solve(keynames:str, searchwords:str, s:list):
                    self.line_couint += 1 
                    if str(keys) == str(keynames) and str(dict_data) == str(searchwords):
                        # 上のパスで検索するとバグる
                        sdict = {list(self.dict_key_pass)[0]:search_dict}
                        self.search_result.update(sdict)
                        self.hitdict_list.append(list(self.dict_key_pass))
                
                search_keys = list(self.search_format.keys())
                for i in search_keys:
                    search_words = self.search_format[i]
                    for j in search_words:
                        search_solve(keynames=i, searchwords=j, s=search_words)


class CMD_PROCESS(object):
    def __init__(self, dict_data:dict, cmd:list):
        self.dict_data = dict_data
        self.cmd = cmd
        
        
    def process(self):
        if self.cmd[0] == "ls":
            self.ls(ls_cmd_value=self.cmd[1])
            pass 

        elif self.cmd[0] == "cd":
            self.cd(cd_value=self.cmd[1])
            pass 

        elif self.cmd[0] == "cat":
            self.cat(cat_value=self.cmd[1])
            pass 
        
        elif self.cmd[0] == "back":
            self.back()
            pass
        
        elif self.cmd[0] == "search":
            self.search(search_value=self.cmd[1])
            pass
        
        elif self.cmd[0] == "save":
            self.save(save_cmd_value=self.cmd[1])

        elif self.cmd[0] == "add":
            self.add(add_cmd_value=self.cmd[1])
         
    
    
    def ls(self, ls_cmd_value):
        
        if ls_cmd_value != None:
            del ls_cmd_value[0]
            
            paser = args.args_paser(" ".join(ls_cmd_value))
            value = args.args_search(paser, ["-s", "--save"])
            if value != None:
                if len(value) == 0:
                    filename = "ls_info.ls"
                else:
                    filename = value[0]
            else:
                print(f"{color1}[!]{color0}Value Error")    
                return 0 
        
        if len(dict_pass) == 0:
            dict_keys = list(self.dict_data.keys())
        else:
            print("pass")
            route = route_pass(dict_data=self.dict_data) 
            dict_keys = route[0]
            self.dict_data = route[1]

        dict_key_count= []
        for i in dict_keys:
            try:
                self.dict_data[i].keys()
                dict_key_count.append(i)
            except:
                dict_key_count.append(f"{color3}{i}{color0}")
        
        line_n = 0
        for i in dict_key_count:
            print(f"[{line_n}] {i}")
            line_n += 1

            if ls_cmd_value != None:
                with open(filename, "a", encoding="utf-8") as f:
                    print(i, file=f)
                    f.close()
    

    def cd(self, cd_value):
        if  cd_value.isdecimal():
             
            if len(dict_pass) == 0:
                if len(list(self.dict_data.keys())) <= int(cd_value):
                    print("[!] value error 1")
                    return 0

                cd_value = str(list(self.dict_data.keys())[int(cd_value)])
            
            else:
                dict_n = route_pass(self.dict_data)[1]
                if len(list(dict_n.keys())) <= int(cd_value):
                    print("[!] value error 2")
                    return 0

                if len(dict_n) != 0:
                    cd_value = str(list(dict_n.keys())[int(cd_value)])
             
        try:
            if len(dict_pass) == 0:
                cd_dict = self.dict_data[str(cd_value)]
            else:
                cd_dict = route_pass(self.dict_data)[1][str(cd_value)]
            
            cd_dict.keys() # if error is file else folder
            dict_pass.append(str(cd_value))
        
        except:
            print(f"{color1}[!]{color0} Not in data keys")
    
    
    def cat(self, cat_value):
        if cat_value.isdecimal():

            if len(dict_pass) == 0:
                if len(list(self.dict_data.keys()) <= int(cat_value)):
                    print(f"{color1}[!]{color0} value error")
                    return 0
                
                cat_value = str(list(self.dict_data.keys())[int(cat_value)])
            
            else:
                dict_n = route_pass(self.dict_data)[1]
                if len(list(dict_n.keys())) <= int(cat_value):
                    print(f"{color1}[!]{color0} value error")
                    return 0
                
                if len(dict_n) != 0:
                    cat_value = str(list(dict_n.keys())[int(cat_value)])
        try:
            if len(dict_pass) == 0:
                cat_dict = self.dict_data[str(cat_value)]
            else:
                cat_dict = route_pass(self.dict_data)[1][str(cat_value)]
                
            print(cat_dict)

        except Exception as e:
            print(f"{color1}[!]{color0} Not in data keys")
            print(e)


    def back(self):
        if 0 < len(dict_pass):
            del dict_pass[len(dict_pass) - 1]
    
    
    def search(self, search_value):
        if len(search_value)  >= 2:
            if strprop.str_comparison(search_value[1], ["key", "-k"]):
                line_n = 0
                for i in OPEN_DICT(self.dict_data).all_keyname():
                    print(f"{color3}[{line_n}] --{i}{color0}")
                    line_n += 1
             
            elif strprop.str_comparison(search_value[1], ["show", "-s"]):
                dict_pass.clear()
                USER_INTERFACE(dict_data=dict_search_value, Mode="SEARCH_RESULT").ctl()

            else:
                search_format = args.args_paser(" ".join(search_value[1:]), opt=True)
                if search_format == None:
                    print(f"{color1}[!]{color0}Value Error")
                    return 0
                
                OPEN_DICT(self.dict_data).search(search_format)
    
    
    def save(self, save_cmd_value):
        
        save_cmd_format = args.args_paser(" ".join(save_cmd_value[1:]))
        target_keys  = args.args_search(save_cmd_format, ["--target","-t"])  
        filenames    = args.args_search(save_cmd_format, ["--file", "-f"]) 
        
        if filenames == None:
            filenames = "_".join(list(dict_pass))
        else:
            filenames = filenames[0]

        if target_keys == None:
            if len(dict_pass) == 0:
                print(f"{color1}[!]{color0}Value Error")
                return 0
            target_keys = dict_pass[-1]
            
            try:
                if len(dict_pass) == 0:
                    target_dict = self.dict_data[target_keys]
                
                else:
                    target_dict = route_pass(self.dict_data)[1]
            except Exception as e:
                    print(f"{color1}[!]{color0}Value Error {e}")
                    return 0

        else:
            if target_keys[0].isdecimal():
                target_keys = (list(self.dict_data.keys())[int(target_keys[0])])
                try:
                    if len(dict_pass) == 0:
                        target_dict = self.dict_data[target_keys]
                    
                    else:
                        target_dict = route_pass(self.dict_data)[1][str(target_keys)]
                except Exception as e:
                        print(f"{color1}[!]{color0}Value Error {e}")
                        return 0
        
        
        filenames =  filenames.replace(" ","_") + ".json" 
        with open(filenames, mode="wt", encoding="utf-8") as f:
                    json.dump(target_dict, f, ensure_ascii=False, indent=2)
                    f.close()
                 
        print(f"{color4}[*]{color0} save to ./{filenames}")
    
    
    def add(self, add_cmd_value):
         
        add_cmd_value  = args.args_paser(" ".join(add_cmd_value[1:]))
        if add_cmd_value == None:
            print(f"{color3}[+]{color0}Enter filename -f")
            return 0
        
        addfile = args.args_search(add_cmd_value, ["--list", "-l"])
        if addfile != None:
            path = args.args_search(add_cmd_value, ["--dir", "-d"])
            
            if path == None:
                path = os.getcwd()
            else:
                if len(path) == 0:
                    print(f"{color1}[!]{color0}Please enter path: -d {path}") 
                    return 0
                path = path[0]
            
            try:
                dir_name = os.listdir(path)
            except Exception as e:
                print(f"{color1}[!]{color0}Error Value {e}") 
                return 0
            
            filename = [f for f in dir_name if os.path.isfile(os.path.join(path ,f))]
            if len(addfile) != 0:
                filename = [f for f in filename if f.endswith(str(addfile[0]))]
             
            dict_add_file_list.clear()
            for i,f in enumerate(filename):
                print(f"[{i}] {f}")
                dict_add_file_list.update({f:str(path)+"/"})
             
            print(f"\npath : {path}")
            return 0
        
        
        
        filenames  = args.args_search(add_cmd_value, ["--file", "-f"])
        if filenames == None:
            print(f"{color3}[+]{color0}Enter filename -f")
            return 0

        for i in filenames:
            try:
                if i.isdecimal():
                    fname = int(i)
                    add_file_keynames = list(dict_add_file_list.keys())
                    if len(add_file_keynames) == 0:
                        
                        print(f"{color1}[!]{color0} Value Error")
                        return 0
                    
                    fname = add_file_keynames[fname]
                    fname = dict_add_file_list[fname] + fname
                    print(fname) 
                else:
                    fname = str(i)
                
                with open(fname, "r", encoding="utf-8") as f:
                    load_josn_file = json.load(f)
                    self.dict_data.update({fname:load_josn_file})
                    f.close()
                
                print(f"{color4}[*]{color0}{fname} added")
            
            except Exception as e:
                print(f"{color1}[!]{color0}Value Error {e}")



class USER_INTERFACE:
    def __init__(self, dict_data:dict, Mode:str):
        self.mode = Mode
        self.dict_data = dict_data

        self.dict_ctl_help = f"""
        v.1.0
                                            
        ls      [line_n or keynames]                : List segments
        cd      [line_n or keynames]                : Chenge direcroty
        cat     [line_n or keynames]                : Open file data
        open    [line_n or keynames]                : Open all data in current pass
                    
    
                    --  add  -- 
                    Add file
        -f --file [filename or See file num]        : File name
        -l --list [file type]                       : See file
        



                    -- search --
                  Keyword search
             search [--keyname] [keyword]

        key                         : Show all keys
        show                        : Go to search results
         
        """

        pass

    def ctl(self):
        while 1:
            dict_path = "/".join(dict_pass)
            
            in_key = input(f"[$] {self.mode} (/{dict_path}) : ")
            in_key = in_key.split(" ")
            in_key = [i for i in in_key if " " != i]
            
            if in_key[0] == "ls":
                if len(in_key) > 1:
                    CMD_PROCESS(self.dict_data, cmd=["ls", in_key]).process()
                
                else:
                    CMD_PROCESS(self.dict_data, cmd=["ls", None]).process()
                pass 
            
            elif in_key[0]  == "cd":
                if len(in_key) ==  2: 
                    if strprop.str_comparison(in_key[1], ["../", ".."]):
                        CMD_PROCESS(self.dict_data, cmd=["back"]).process()
                        pass 

                    elif strprop.str_comparison(in_key[1], ["~", "~/"]):
                        route_pass.clear()
                        pass 
                    
                    else:
                        CMD_PROCESS(self.dict_data, cmd=["cd", in_key[1]]).process()
                        pass 

            elif in_key[0] == "cat":
                if len(in_key) == 2:
                    CMD_PROCESS(self.dict_data, cmd=["cat", in_key[1]]).process()
                pass 

            elif strprop.str_comparison(in_key[0], ["clear", "cls"]):
                os.system("clear")
            
            elif strprop.str_comparison(in_key[0], ["quit","exit","!","q!"]):
                dict_pass.clear()
                break
                pass 

            elif in_key[0] == "search":
                CMD_PROCESS(self.dict_data, cmd=["search", in_key]).process()
                              
            elif in_key[0] == "open":
                OPEN_DICT(self.dict_data).all_open()

            elif in_key[0] == "save":
                print("save")
                CMD_PROCESS(self.dict_data, cmd=["save", in_key]).process()
            
            elif in_key[0] == "add":
                CMD_PROCESS(self.dict_data, cmd=["add", in_key]).process()
            
            elif in_key[0] == "help":
                print(self.dict_ctl_help)

            


    



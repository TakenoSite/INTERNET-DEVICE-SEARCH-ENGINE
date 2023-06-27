
def args_paser(value:str, opt=False):
    data = value.split(" ")
    data = [i for i in data if "" != i] 
 
    result = {}
    current_option = None
    
    for item in data:
        if item.startswith('-'):
            if item.startswith("--"):
                if opt:
                    current_option = item[2:]    
                else:
                    current_option = item
            else:
                if opt:
                    current_option = item[1:]
                else:
                    current_option = item
                
            result[current_option] = []
        else:
            try:
                result[current_option].append(item)
            except:
                return None

    return result

def args_search(value:dict, search_name:list):
    for i in search_name:
        if i in value:
            return value[i]
    
    return None


def args_deletes(value:dict, delete_name:list):
    for i in delete_name:
        try:
            value.pop(delete_name)
            return value
        except:
            continue

    return None


def args_to_str(dict_data:dict)->str:
    return " ".join([(str(i)+" "+str( " ".join(res[i]))) for i in list(res.keys())])


if __name__ == "__main__":
    res = args_paser("-A -sS -sV -p 80 22 -h 1.1.1.1 2.2.2.2")
    host = args_search(res, ["-h"])
    
    res.pop("-h")
    nmap_cmd = " ".join([(str(i)+" "+str( " ".join(res[i]))) for i in list(res.keys())])
    

    print(host)    
    print(nmap_cmd)


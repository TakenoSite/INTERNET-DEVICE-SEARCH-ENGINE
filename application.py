import interface 
import sys


if __name__ == "__main__":
    api_keys_filename = "./conf/API_KEYs.txt"
    
    # ログイン処理
    auth = interface.AUTH(api_keyfilename=api_keys_filename)
    login = auth.login() 
    
    if not login:
        print("application exit") 
        sys.exit() 
    
    ctl_interface = interface.CLI_INTERFACE(api_auth=login,
            api_keys_fname=api_keys_filename)
    


    pass 


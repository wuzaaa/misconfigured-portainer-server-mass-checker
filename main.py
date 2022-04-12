import requests
from multiprocessing.pool import ThreadPool
from functools import partial
import time



print('''  _____           _        _                    _____ _               _
 |  __ \         | |      (_)                  / ____| |             | |
 | |__) |__  _ __| |_ __ _ _ _ __   ___ _ __  | |    | |__   ___  ___| | _____ _ __
 |  ___/ _ \| '__| __/ _` | | '_ \ / _ \ '__| | |    | '_ \ / _ \/ __| |/ / _ \ '__|
 | |  | (_) | |  | || (_| | | | | |  __/ |    | |____| | | |  __/ (__|   <  __/ |
 |_|   \___/|_|   \__\__,_|_|_| |_|\___|_|     \_____|_| |_|\___|\___|_|\_\___|_|



''')


# List of connections failed
Failed_Connections = []


with open('Servers.txt') as f:
    servers = [line.rstrip() for line in f]
    f.close()


def login(session, server):
    url = f'http://{server}/api/users/admin/check'
    try:
        response = requests.get(url)
    except:
        print('[~] Connection to '+server+' failed! Moving on.')
    if '404' in str(response):
        with open('Saved.txt', "a") as f:
                f.write(f'http://'+server+'/#!/init/admin\n')
        print('\n[!] Portainer server not setup yet, saved URL! '+url+'\n')
    else:
        Failed_Connections.append(server)
        print('[-] Portainer server is setup, moving on.  '+url)




if __name__ == "__main__":
    # creating a pool object
    with ThreadPool(min(len(servers), 5000)) as pool, \
    requests.Session() as session:
        # map will return list of None since `login` returns None implicitly:
        try:
            pool.map(partial(login, session), servers)
        except:
            print('\n\n[*] Job finished!')
            with open('Saved.txt', "a") as f:
                f.write('\n')
                f.close()

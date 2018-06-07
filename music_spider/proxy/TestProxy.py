import requests
import pandas as pd
import time

def fortmat_ip(df):
    return 'http://'+str(df['ip'])+':'+str(df['port'])



if __name__ == '__main__':
    url = 'https://music.163.com/'
    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
    }
    df = pd.read_excel('ip.xlsx', header=None, names=['ip', 'port'])
    ips = list(df.apply(fortmat_ip, axis=1))



    res = []
    for i in ips:
        start_time = time.clock()
        resp = requests.post(url, headers=header, proxies = {'http': i})
        end_time = time.clock()
        if resp.status_code == 200:
            _res = (i, end_time-start_time)
            res.append(_res)
    data = pd.DataFrame(res)
    print(len(data))
    data.to_csv('ips.csv')
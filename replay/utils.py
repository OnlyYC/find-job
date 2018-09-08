import time

def log(*args, **kwargs):
    # time.time() 返回 unix time
    # 如何把 unix time 转换为普通人类可以看懂的格式呢？
    format = '%H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


# 获取代理
def get_proxy():
    proxies = {'http': '118.190.95.35:9001', 'https': 'https://117.158.81.151:53281'}
    return proxies


# 设置代理不可用
# def setProxyUnavailable(url):

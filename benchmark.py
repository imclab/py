import sys
import csv
from random import choice
from datetime import datetime
from collections import defaultdict
from BeautifulSoup import BeautifulSoup

import eventlet
requests = eventlet.import_patched('requests')

NUM_REQUESTS = 10000
CONCURRENT_REQUESTS = 50
USER_AGENTS = [
    "Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/21.0",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11",
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11",
    "Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/11.10 Chromium/17.0.963.65 Chrome/17.0.963.65 Safari/535.11",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/11.04 Chromium/17.0.963.65 Chrome/17.0.963.65 Safari/535.11",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/10.10 Chromium/17.0.963.65 Chrome/17.0.963.65 Safari/535.11",
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/11.10 Chromium/17.0.963.65 Chrome/17.0.963.65 Safari/535.11",
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.65 Safari/535.11",
    "Mozilla/5.0 (X11; FreeBSD amd64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.65 Safari/535.11",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.65 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.65 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.65 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_4) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.65 Safari/535.11",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20130331 Firefox/21.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20100101 Firefox/21.0",
    "Mozilla/5.0 (X11; Linux i686; rv:21.0) Gecko/20100101 Firefox/21.0",
    "Mozilla/5.0 (Windows NT 6.2; rv:21.0) Gecko/20130326 Firefox/21.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130401 Firefox/21.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130331 Firefox/21.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130330 Firefox/21.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0",
    "Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20130401 Firefox/21.0",
    "Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20130328 Firefox/21.0",
    "Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20100101 Firefox/21.0",
    "Mozilla/5.0 (Windows NT 5.1; rv:21.0) Gecko/20130401 Firefox/21.0",
    "Mozilla/5.0 (Windows NT 5.1; rv:21.0) Gecko/20130331 Firefox/21.0",
    "Mozilla/5.0 (Windows NT 5.1; rv:21.0) Gecko/20100101 Firefox/21.0",
    "Mozilla/5.0 (Windows NT 5.0; rv:21.0) Gecko/20100101 Firefox/21.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0",
    "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
    "Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Googlebot/2.1 (+http://www.googlebot.com/bot.html)",
    "Googlebot/2.1 (+http://www.google.com/bot.html)",
]
IP_ADDRESSES = [
    "10.0.0.1",
    "10.0.0.2",
    "10.0.0.4",
    "10.0.0.8",
    "10.0.0.16",
    "222.42.1.226",
    "113.53.232.46",
    "180.250.129.184",
    "111.90.146.196",
    "217.13.118.93",
    "198.154.114.100",
    "190.95.199.243",
    "183.60.126.184",
    "123.103.23.106",
    "110.77.226.216",
    "118.99.126.162",
    "118.175.88.45",
    "159.255.166.29",
    "195.165.58.61",
    "118.196.121.17",
    "220.422.125.226",
    "116.131.232.246",
    "120.258.129.184",
    "191.905.146.196",
    "215.130.118.193",
    "198.154.114.100",
    "190.195.199.243",
    "183.160.126.184",
    "123.103.223.106",
    "110.177.226.216",
    "118.199.126.162",
    "118.175.188.245",
    "159.255.166.129",
    "195.165.158.161",
    "118.196.121.179",
]

PROXIES = [
    "http://222.42.1.226:80",
    "https://113.53.232.46:3128",
    "http://180.250.129.184:8080",
    "http://111.90.146.196:80",
    "https://217.13.118.93:80",
    "https://198.154.114.100:8089",
    "https://190.95.199.243:80",
    "http://183.60.126.184:1080",
    "https://123.103.23.106:29786",
    "https://110.77.226.216:3128",
    "https://118.99.126.162:8080",
    "https://118.175.88.45:8080",
    "https://159.255.166.29:8080",
    "https://95.65.58.61:443",
    "https://118.96.121.17:8080",
    "https://66.35.68.146:3128",
    "https://80.191.169.66:8080",
    "http://80.58.29.170:80",
    "https://124.126.126.7:80",
    "http://190.128.170.18:8080",
    "http://211.143.200.183:80",
    "http://36.32.20.222:8080",
    "https://58.252.56.149:9000",
    "https://200.6.121.105:80",
    "http://122.72.28.118:80",
    "https://221.13.79.20:80",
    "https://59.46.67.108:8080",
    "https://125.39.66.154:80",
    "http://113.12.83.157:80",
    "https://116.213.51.80:80",
    "https://182.48.191.83:8080",
    "https://117.211.91.147:808",
    "http://218.108.168.67:82",
    "https://124.237.92.2:8080",
    "https://186.103.143.210:8080",
    "http://200.62.231.218:3128",
    "https://122.72.0.145:80",
    "https://93.78.92.179:3128",
    "http://189.59.17.206:3128",
    "http://211.167.64.112:8080",
    "https://178.254.152.102:6666",
    "https://58.242.249.31:35010",
    "https://213.16.101.18:3128",
    "https://180.173.89.208:8080",
    "https://218.197.148.4:21",
    "https://2.133.93.178:9090",
    "https://180.250.144.231:8080",
    "https://111.67.78.34:80",
    "http://123.103.23.106:10064",
]


def fetch(url):
    try:
        headers = {
            "Connection": "close",
            "Cache-Control": "no-cache",
            "User-Agent": choice(USER_AGENTS),
            "Via": choice(IP_ADDRESSES),
            "X-Forwarded-For": choice(IP_ADDRESSES),
        }
        proxies = {
            "http": choice(PROXIES)
        }

        # make and time request
        start = datetime.now()
        r = requests.get(url, headers=headers)
        end = datetime.now()

        # soup = BeautifulSoup(r.text)
        # print soup.find("title")

        # how long did it take?
        diff = end - start
        seconds = diff.total_seconds()

        # round to nearest second
        decimal = seconds % 1
        if decimal >= 0.5:
            return int(seconds) +1
        else:
            return int(seconds)

    except:
        return None


def main(site):

    pool = eventlet.GreenPool(CONCURRENT_REQUESTS)
    pile = eventlet.GreenPile(pool)

    for x in xrange(NUM_REQUESTS):
        # eventlet.spawn(fetch, [site])
        pile.spawn(fetch, site)

    distribution = defaultdict(int)
    for time in pile:
        distribution[time] += 1

    ticks = sorted([x for x in distribution.keys()])
    values = [distribution[tick] for tick in ticks]

    with open("results.csv", "a") as f:
        w = csv.writer(f)
        w.writerow(["", "", "", "", "", "", "", "",])
        w.writerow([site, datetime.now().isoformat(), NUM_REQUESTS, CONCURRENT_REQUESTS])
        w.writerow(["num_seconds", "num_requests"])
        for t, v in zip(ticks, values):
            w.writerow([t, v])

    print zip(ticks, values)

if __name__ == "__main__":
    site = sys.argv[1]
    main(site)

import platform
import random
import os
import time

linux_countries = ['al', 'ar', 'au', 'at', 'br', 'bg', 'ca', 'cl', 'cr', 'hr', 'cy', 'cz', 'dk', 'ee', 'fi',
                   'fr', 'ge', 'de', 'gr', 'hk', 'hu', 'is', 'in', 'id', 'ie', 'il', 'it', 'jp', 'lv', 'lu', 'my',
                   'mx', 'md', 'nl', 'nz', 'mk', 'no', 'pl', 'pt', 'ro', 'rs', 'sg', '', 'si', 'za', 'kr', 'es',
                   'se', 'ch', 'tw', 'th', 'tr', 'ua', 'So', 'uk', 'us']
windows_countries = ['United States', 'Canada', 'Argentina', 'Brazil', 'Mexico', 'Costa Rica', 'Chile',
                     'United Kingdom', 'Germany', 'France', 'Netherlands', 'Sweden', 'Switzerland',
                     'Denmark', 'Poland', 'Italy', 'Spain', 'Norway', 'Belgium', 'Ireland', 'Czech Republic',
                     'Austria', 'Portugal', 'Finland', 'Ukraine', 'Romania', 'Serbia', 'Hungary', 'Luxembourg',
                     'Slovakia', 'Bulgaria', 'Latvia', 'Greece', 'Iceland', 'Estonia', 'Albania', 'Croatia',
                     'Cyprus', 'Slovenia', 'Moldova', 'Bosnia and Herzegovina', 'Georgia', 'North Macedonia',
                     'Turkey', 'South Africa', 'India', 'Israel', 'Turkey', 'United Arab Emirates', 'Australia',
                     'Taiwan', 'Singapore', 'Japan', 'Hong Kong', 'New Zealand', 'Malaysia', 'Vietnam', 'Indonesia',
                     'South Korea', 'Thailand']


def nordvpn():
    version = platform.system()
    tt=os.system("cd C:\\Program Files\\NordVPN\\")
    print(tt)
    if version == "Linux" or version == "Darwin":
        ser = "nordvpn connect " + random.choice(linux_countries) + " > /dev/null 2>&1"
        os.system(ser)
    elif version == "Windows":
        server = "nordvpn -c -g \'" + random.choice(windows_countries) + "\'" + " > /dev/null 2>&1"
        os.system('nordvpn -c')
    time.sleep(60)


# Before using NordVpn
import requests
import urllib3
http = urllib3.PoolManager()
resp = http.request("GET", "https://api.ipify.org")
ip = resp.data.decode("UTF-8")
print(f"\nWith Urllib3\nIp:\t{ip}")
nordvpn()
# Requests Example
ip = requests.get('https://api.ipify.org').text
print(f"\nWith Requests\nIp:\t{ip}")

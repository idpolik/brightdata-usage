import requests
import json
from termcolor import colored
import colorama
import math

def truncate(number, digits) -> float:
    nbDecimals = len(str(number).split('.')[1]) 
    if nbDecimals <= digits:
        return number
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper
def loadConfig():
    with open('brightdata.json', 'r') as configfile:
        return json.loads(configfile.read())


headers = {'Authorization': loadConfig()['api-key']}
api = "https://brightdata.com/api/zone/bw?zone=" + loadConfig()["api-zone"]

colorama.init()
r = requests.get(api, headers=headers, timeout=10).text
mbusage = (0.000001 * json.loads(r)[loadConfig()['user-id']]["sums"][loadConfig()['api_zone']]["back_m0"]["bw_sum"])
date = str(json.loads(r)[loadConfig()['user-id']]["last_update_ts"])
valdate = str(json.loads(r)[loadConfig()['user-id']]["last_value_ts"])
gb = mbusage / 1000
print(colored("----------------------------------", 'grey', attrs=['bold']))
print(colored(date.split("Z")[0].split("T")[0] + " @ " + date.split("Z")[0].split("T")[1].split(".")[0], 'magenta', attrs=['bold']))
print(colored("----------------------------------", 'grey', attrs=['bold']))
if(mbusage < 1000):
    print(colored("{} Usage: ".format(loadConfig()['api-zone']), 'white', attrs=['bold']) + colored(str(truncate(mbusage, 2)) + ' MB', 'blue'))
else:
    print(colored("{} Usage: ".format(loadConfig()['api-zone']), 'white', attrs=['bold']) + colored(str(truncate(gb, 2)) + ' GB', 'blue'))
print(colored("Cost:", 'white', attrs=['bold']), colored("$"+str(truncate((gb * .6), 3)), 'blue'))
print(colored("Value TS:", 'white', attrs=['bold']), colored(valdate.split("Z")[0].split("T")[1].split(".")[0], 'blue'))
print(colored("----------------------------------", 'grey', attrs=['bold']))
        

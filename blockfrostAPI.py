import requests
from requests.exceptions import HTTPError, Timeout
import json
import time

from config import HEADER, VERSION, URL_BASE, ADDRESS

def main():
    # stakeAddr = getStakeAddr()
    # addr_amt = getAddrAmt(stakeAddr)
    # print("ADA available:", addr_amt) 

    epochTxCount = getTransactionVol()
    print(epochTxCount)

    # StaKePoolList = getStakePoolList()
    # print(StaKePoolList)

def getStakeAddr():
    call_type = 'addresses' 
    payload = {
        } # pass parameters as a dictionary; example=> {'order' : 'desc'}

    url = f'{URL_BASE}/{VERSION}/{call_type}/{ADDRESS}'
    data = httpGetRequest(url, payload, viewResults=False)
    return data['stake_address']


def getAddrAmt(stakeAddr):
    call_type = 'accounts' 
    url = f'{URL_BASE}/{VERSION}/{call_type}/{stakeAddr}'
    payload = {
        } # example=> {'order' : 'desc'}
    data = httpGetRequest(url, payload, viewResults=False)
    return (int(data['controlled_amount']) // 1000000) # amount coverted to ada


def getStakePoolList():
    call_type = 'pools' 
    url = f'{URL_BASE}/{VERSION}/{call_type}'
    poolList = []
    emptyData, i = False, 0
    while not emptyData:
        payload = {
            'count' : '100',
            'page' : str(i+1)
            } # Default: {'order' : 'asc'}
        data = httpGetRequest(url, payload, viewResults=False)
        poolList += data
        i += 1 
        if not data: 
            emptyData = True
    return poolList


def getTransactionVol():
    call_type1 = 'epochs' 
    call_type2 = 'next'
    epochNumber = 0
    url = f'{URL_BASE}/{VERSION}/{call_type1}/{epochNumber}/{call_type2}'
    totalTxVol = []
    emptyData, i = False, 0
    while not emptyData:
        payload = {
            'count' : '100',
            'page' : str(i+1)
            }
        data = httpGetRequest(url, payload, viewResults=False)
        totalTxVol += data
        i += 1
        if not data: 
            emptyData = True

    epochTxCount = dict()
    for i in range(len(totalTxVol)): 
        epochTxCount.update({ totalTxVol[i]['epoch'] : [totalTxVol[i]['tx_count'], posixToDate(totalTxVol[i]['start_time'])] })
    return epochTxCount    


def httpGetRequest(urlStr, payload={}, viewResults=False):
    result = requests.get(url=urlStr , headers=HEADER, params=payload)
    print("Status: {0}".format(result))
    # print(result.url)
    result_jsonStr = json.loads(result.text) # could be wrapped in a list depending on the api call
    if viewResults == True:
        print(json.dumps(result_jsonStr, indent=4)) # view results in a pretty format
    return result_jsonStr


def posixToDate(POSIXTime):
    date = time.strftime('%Y-%m-%d', time.localtime(POSIXTime)) # For exact time include> %H:%M:%S
    # from datetime import datetime
    # datetime.strptime("2012-may-31 19:00", "%Y-%b-%d %H:%M")
    # datetime.datetime(2012, 5, 31, 19, 0)
    return date


if __name__ == '__main__':
    main()
    
import requests
from requests.exceptions import HTTPError, Timeout
import json

from config import HEADER, VERSION, URL_BASE, ADDRESS


def httpGetRequest(urlStr, payload={}, viewResults=False):
    result = requests.get(url=urlStr , headers=HEADER, params=payload)
    print("Status: {0}".format(result))
    # print(result.url)
    result_jsonStr = json.loads(result.text) # could be wrapped in a list depending on the api call
    if viewResults == True:
        print(json.dumps(result_jsonStr, indent=4)) # view results in a pretty format
    return result_jsonStr


def getStakeAddr():
    call_type = 'addresses' 
    payload = {
        } # pass parameters as a dictionary; example=> {'order' : 'desc'}

    url = f'{URL_BASE}/{VERSION}/{call_type}/{ADDRESS}'
    data = httpGetRequest(url, payload, viewResults=False)
    return data['stake_address']


def getAddrAmt(stakeAddress):
    call_type = 'accounts' 
    payload = {
        } # example=> {'order' : 'desc'}

    url = f'{URL_BASE}/{VERSION}/{call_type}/{stakeAddress}'
    data = httpGetRequest(url, payload, viewResults=True)

    return (int(data['controlled_amount']) // 1000000) # amount coverted to ada


def getTransactionVolume():
    call_type1 = 'epochs' 
    call_type2 = 'next'
    epochNumber = 0
    url = f'{URL_BASE}/{VERSION}/{call_type1}/{epochNumber}/{call_type2}'

    totalData = []
    pageNum = 4
    for i in range(pageNum):
        payload = {
            'count' : '100',
            'page' : str(i+1)
            }
        data = httpGetRequest(url, payload, viewResults=False)
        totalData += data

    epochTxCount = dict()
    for i in range(len(totalData)): 
        epochTxCount.update({totalData[i]['epoch'] : totalData[i]['tx_count']})
    return epochTxCount    


def main():
    # stakeAddr = getStakeAddr()
    # addr_amt = getAddrAmt(stakeAddr)
    # print("ADA available:", addr_amt) 

    epochTxCount = getTransactionVolume()
    print(epochTxCount)


if __name__ == '__main__':
    main()
    
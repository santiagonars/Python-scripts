import os
import json
import time
import requests
from requests.exceptions import HTTPError, Timeout

from config import HEADER, VERSION, URL_BASE, ADDRESS # config contains api key
from matplotlib.ticker import FormatStrFormatter, StrMethodFormatter
import matplotlib.pyplot as plt
import numpy as np

def main():
    # stakeAddr = getStakeAddr()
    # addr_amt = getAddrAmt(stakeAddr)
    # print("ADA available:", addr_amt)

    # StaKePoolList = getStakePoolList()
    # print(StaKePoolList)

    epochTxCount = getTransactionCount(createChart=True)
    for key, value in epochTxCount.items():
        print(key, ':', value)


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


def getTransactionCount(createChart=False):
    call_type1 = 'epochs' 
    call_type2 = 'next'
    epochNumber = 0
    url = f'{URL_BASE}/{VERSION}/{call_type1}/{epochNumber}/{call_type2}'
    nextEpochsData = []
    emptyData, i = False, 0
    while not emptyData:
        payload = {
            'count' : '100',
            'page' : str(i+1)
            }
        data = httpGetRequest(url, payload, viewResults=False)
        nextEpochsData += data
        i += 1
        if not data: 
            emptyData = True
    epochTxCount = {}
    for i in range(len(nextEpochsData)): 
        epochTxCount.update({ nextEpochsData[i]['epoch'] : nextEpochsData[i]['tx_count'] })
        # epochTxCount.update({ nextEpochsData[i]['epoch'] : [nextEpochsData[i]['tx_count'], posixToDate(nextEpochsData[i]['start_time'])] })
    
    if createChart == True:
        chart_TxCount(epochTxCount)
        
    return epochTxCount # returns dict


def chart_TxCount(epochTxCount):
    x = np.array(list(epochTxCount.keys())) # epochs
    y = np.array(list(epochTxCount.values())) # transaction count
    
    font1 = {'family':'serif','color':'blue','size':30}
    font2 = {'family':'serif','color':'darkred','size':25}
    plt.rcParams["figure.figsize"] = (20,12)

    fig, ax = plt.subplots()
    plt.plot(x, y)
    
    plt.xticks(np.arange(min(x)-1, max(x)+9, 10.0))
    plt.xticks(fontsize=15, rotation=45)
    plt.yticks(fontsize=15)
    ax.yaxis.set_major_formatter(StrMethodFormatter('{x:,}'))
    
    plt.title("Cardano Transaction Count", fontdict = font1)
    plt.xlabel("Epoch", fontdict = font2)
    plt.ylabel("Number of Transactions", fontdict = font2)
    plt.grid(axis = 'x', linestyle = 'dashed')

    dir_path = os.path.dirname(os.path.realpath(__file__))
    plt.savefig(dir_path + '/charts/CardanoTxCount.png')
    # plt.show()


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


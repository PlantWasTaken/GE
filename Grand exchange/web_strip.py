import requests
import json
import linecache
import time as t
import sys, os
import datetime
from operator import itemgetter


sys.setrecursionlimit(10000)

index = open("index.txt", "r")
bankmanagment = open("bank.json", "r")
log = open("log.txt", "r+")

data = ''
line_count = 0

headers = {

    'User-Agent' : 'Plant',
    'From' : 'Plant#6356'
}

temp = ''
#p_change = 0 #current price omcpared to yesterday price ot detrmine

def l_count():
    global line_count
    for line in index:
        if line != "\n":
            line_count = line_count + 1

l_count()
index = open("index.txt", "r")

def eval(data, p_change): #evaulates all items in list, manages purchaes etc...
    #print(p_change)
    if(p_change >= -9):
        if(p_change <= 0):
            #print(data['item']['name'], data['item']['current']['price'])
            bought_items.append([data['item']['id'], data['item']['current']['price'], p_change, data['item']['name']])
        else:
            pass
    else:
        pass


def sell_items():
    i = 0
    current_prices = []

    with open("bank.json", "r") as jsonFile:
        json_data_sell = json.load(jsonFile)
                  
    def main_sell(i):
        print("Waiting for API\nDo not close!\n")
        t.sleep(20)

        while(i != 3):
            url = 'http://services.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item=' + str(json_data_sell['items']['slot' + str(i+1)]['Id'])
            try:
                r = requests.get(url, headers=headers)                    
                sell_data = r.json()
                i = i + 1
            except ValueError:
                main_sell(i)
            
            current_prices.append(int(sell_data['item']['current']['price']))
                
            t.sleep(3) #pauses for api to catch up
        i = 0
    main_sell(i)

    with open("bank.json", "w") as jsonFile: 
        for i in range(len(current_prices)):
            json_data_sell['items']['slot' + str(i+1)]['Current price'] = current_prices[i]

        json.dump(json_data_sell, jsonFile, indent=4)

    with open("bank.json", "r") as jsonFile: #opens new instance of json file after appending prices
        json_data_sell = json.load(jsonFile)

    with open("bank.json", "w") as jsonFile:   #compares prices and decides to sell or hold
        for i in range(3):
            if(json_data_sell['items']['slot' + str(i+1)]['Price'] < ((json_data_sell['items']['slot' + str(i+1)]['Current price'])-(json_data_sell['items']['slot' + str(i+1)]['Current price']*0.01))):
                #print(json_data_sell['items']['slot' + str(i+1)]['Amount'], "AMOUNT")
                if(json_data_sell['items']['slot' + str(i+1)]['Amount'] > 0):
            
                    #print((json_data_sell['items']['gp'] + (json_data_sell['items']['slot' + str(i+1)]['Current price'])-int(json_data_sell['items']['slot' + str(i+1)]['Current price']*0.01))*json_data_sell['items']['slot' + str(i+1)]['Amount'])

                    json_data_sell['items']['gp'] = ((json_data_sell['items']['gp'] + (json_data_sell['items']['slot' + str(i+1)]['Current price'])-int(json_data_sell['items']['slot' + str(i+1)]['Current price']*0.01))*json_data_sell['items']['slot' + str(i+1)]['Amount'])
                    json_data_sell['items']['slot' + str(i+1)]['Amount'] = 0 #changes amount after item has been sold
                    json_data_sell['items']['portfolio'] = (json_data_sell['items']['portfolio'])+(json_data_sell['items']['slot' + str(i+1)]['Price'])*(json_data_sell['items']['slot' + str(i+1)]['Amount']) #sets portfolio

                    now = datetime.datetime.now() #writing to log file
                    log.write("Sold at : " + str(now.strftime("%Y-%m-%d %H:%M:%S" + "\n")))
                
                else:
                    #print("NO0", i)
                    pass
            else:
                #print("NO", i)
                pass

        json_data_sell['items']['net'] = (json_data_sell['items']['gp']) + (json_data_sell['items']['portfolio']) #sets net value
        #print(json_data_sell)
        json.dump(json_data_sell, jsonFile, indent=4)  


bought_items = [] #list of all bought items n=[[[id0],[price0],[change0],[name0], [[id1],[price1],[change1], [name1]]]

def buy_items(): #writes to json file
    global bought_items #= ["2"][340][-3.24][cannon ball] | [id][price][change][name]
    items_to_buy = [] #index of json file with 0 amount

    bought_items = sorted(bought_items, key=itemgetter(2), reverse=True) #sorts and picks out 3 biggest price falls

    with open("bank.json", "r") as jsonFile:
        json_data_buy = json.load(jsonFile)

        for i in range(3): #checks what slots are available
            if(json_data_buy['items']['slot' + str(i+1)]['Amount'] == 0):
                items_to_buy.append(i)
            else:
                pass

    del bought_items[0:len(bought_items)-3] #list filtering with respect to amount of avaiable slots

    with open("bank.json", "w") as jsonFile: #appends to jsonfile, buying items, current price, change
        j = 0
        for i in items_to_buy:  #filter thourhgt available items to decide what to append ot json
            json_data_buy["items"]['slot' + str(i+1)]['Item'] = bought_items[j][3]     #item name, i = slot+i in json, j = what item to buy | bought_items
            json_data_buy['items']['slot' + str(i+1)]['Price'] = bought_items[j][1]    #item price, bought at price
            json_data_buy['items']['slot' + str(i+1)]['Change'] = bought_items[j][2]   #item change
            json_data_buy['items']['slot' + str(i+1)]['Id'] = bought_items[j][0]

            json_data_buy['items']['slot' + str(i+1)]['Amount'] = int((json_data_buy['items']['gp'])/(len(items_to_buy))/bought_items[j][1]) #buys items
            j = j + 1


        
        if(len(items_to_buy) != 0): #moves money from a to b simulating purcahse
            for i in range(len(items_to_buy)):
                json_data_buy['items']['portfolio'] = (json_data_buy['items']['portfolio'])+(json_data_buy['items']['slot' + str(i+1)]['Price'])*(json_data_buy['items']['slot' + str(i+1)]['Amount'])
                json_data_buy['items']['gp'] = (json_data_buy['items']['gp'])-((json_data_buy['items']['slot' + str(items_to_buy[i]+1)]['Price'])*(json_data_buy['items']['slot' + str(items_to_buy[i]+1)]['Amount']))

                now = datetime.datetime.now() #writing to log file
                log.write("Bought at : " + str(now.strftime("%Y-%m-%d %H:%M:%S") + "\n"))
                    

                
            json_data_buy['items']['net'] = (json_data_buy['items']['gp']) + (json_data_buy['items']['portfolio'])            
        else:
            pass

        json.dump(json_data_buy, jsonFile, indent=4)
    
    bought_items = []

def findItemPrice(): #finds all item prices from index.txt
    Done = False
    i = 0
    print("Working...")
    while(Done == False):
        while(i != line_count):
            temp = linecache.getline('index.txt', i+1)
            if(temp[-1] == '\n'):
                url = 'http://services.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item=' + str(temp[:-1])
            else:
                url = 'http://services.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item=' + str(temp)
            try:
                r = requests.get(url, headers=headers)
                
                data = r.json()
                item_price = data['item']['current']['price']
                item_change = data['item']['today']['price']
            except ValueError:
                break
            n = []
            p = []
            p_1 = '' #foramtted item price
            n_1 = '' #formatted item change
            suf_c = 1 #change
            suf_p = 1 #price
            for j in str(item_change):  #filtering out and formatting data correctly
                if(j == ','): #MID
                    pass
                elif(j == 'k'): #SUF
                    suf_c = 1000
                    pass
                else:
                    n.append(j) #PRE
            for h in str(item_price):
                if(h == ','): #MID
                    pass
                elif(h == 'k'): #SUF
                    suf_p = 1000
                    pass
                elif(h == 'm'): #suf
                    suf_p = 10**6
                else:
                    p.append(h) #PRE
            if(n[0] == '-'):
                n.pop(1)
                n_1 = ''.join(map(str, n))
                p_1 = ''.join(map(str, p))
                p_change = ((float(n_1)*suf_c)/(float(p_1)*suf_p))*100
                eval(data, p_change)
            else:
                n.pop(0)
                n_1 = ''.join(map(str, n))
                p_1 = ''.join(map(str, p))
                if(n_1 == ''):
                    #prices.write(str(data['item']['name']) + " : " + str(data['item']['current']['price']) + " | " + str('Change') + " : " + "0.00" + " | " + str('Trend') + " : " + str(data['item']['today']['trend']) + "\n")
                    p_change = 0
                    eval(data, p_change)
                else:
                    p_change = ((float(n_1)*suf_c)/(float(p_1)*suf_p))*100
                    eval(data, p_change)
            t.sleep(0)
            if(i+1 == line_count):
                Done = True
                break
            else:
                i = i + 1
    index.close()

for i in range(2):
    print("Safe to close!")
    findItemPrice()
    os.system('clear')      
    buy_items()
    sell_items()
    print("Waiting for API...\nSafe to close")
    t.sleep(60)

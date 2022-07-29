import requests
import json
import time as t
import linecache
from alive_progress import alive_bar

index = open(r"C:\Users\Max\Desktop\Osrs bot\Grand exchange\Scraped f2p id.txt", "r")
tempe = open('tempid.txt', "w")

headers = {

    'User-Agent' : 'Plant',
    'From' : 'Plant#6356'
}

line_count = 0
Done = False

def l_count():
    global line_count
    for line in index:
        if line != "\n":
            line_count = line_count + 1
l_count()
index = open(r"C:\Users\Max\Desktop\Osrs bot\Grand exchange\Scraped f2p id.txt", "r")


i = 0
with alive_bar(line_count, title='Prosecessing', length=20) as bar:
    while(Done == False):
        while(i != line_count):
            temp = linecache.getline('Scraped f2p id.txt', i+1)
            if(temp[-1] == '\n'):
                url = 'http://services.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item=' + str(temp[:-1])
            else:
                url = 'http://services.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item=' + str(temp)

            try:
                r = requests.get(url, headers=headers)
                        
                data = r.json()
            except ValueError:
                break
            
            price = 0
            suf = 1
            n = []
            n_1 = 0
            itemprice = data['item']['current']['price']

            for j in str(itemprice):
                if(j == ','):
                    pass
                elif(j == 'k'):
                    suf = 1000
                elif(j == 'm'):
                    suf = 10**6
                else:
                    n.append(j)

            if(n[0] == '-'):
                n.pop(1)
                n_1 = ''.join(map(str, n))

                price = float(n_1)*suf

            else:
                n_1 = ''.join(map(str, n))

                if(n_1 == ''):
                    price = float(n_1)*suf

                else:
                    price = float(n_1)*suf

            if(data['item']['members'] == 'false'):
                if(price < 1000):
                    if(price > 100):
                        tempe.write(linecache.getline('Scraped f2p id.txt', i+1))
                    else:
                        pass
                else:
                    pass


            if(i+1 == line_count):
                bar()
                Done = 1
                break
            else:
                i = i + 1
                bar()
    

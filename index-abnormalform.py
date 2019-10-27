import urllib2
from bs4 import BeautifulSoup
import csv 

myBigData = []

link = 'http://en.dinus.ac.id/mahasiswa/A11.2017.{}'

start = 10055
stop = 11000
data = []

for idx in range(start, stop):

    page = urllib2.urlopen(link.format(idx))
    soup = BeautifulSoup(page, 'html.parser')
    tables = soup.find_all('table')

    if len(tables) > 0:

        biodata = tables[0].find_all('tr')
        mhsStat = biodata[3].find_all('td')[2].text

        if mhsStat == "Aktif":
            mhname = biodata[0].find_all('td')[2].text
            nim = biodata[1].find_all('td')[2].text
            ipk = float(biodata[4].find_all('td')[2].text.split(' ')[0])
            #mahasiswa = { "nim": nim, "name": mhname, "ipk": ipk}
            #print(nim, mhname, ipk)
            #print('------------------------------------------------')

            makul = tables[1].find_all('tr')
            foo = makul[0]
            for item in makul:
                if item != foo:
                    code = item.find_all('td')[1].text
                    name = item.find_all('td')[3].text
                    status = item.find_all('td')[5].text
                    makul = {"code": code, "name": name}
                    print(nim, mhname, ipk, code, name, status)
                    
                    mySmallData = {}
                    mySmallData['nim'] = nim
                    mySmallData['mhname'] = mhname
                    mySmallData['ipk'] = ipk
                    mySmallData['code'] = code
                    mySmallData['name'] = name
                    mySmallData['status'] = status
                    
                    myBigData.append(mySmallData)
            print("")
            
# simpan data ke csv
filename = 'myBigData.csv'
with open(filename, 'wb') as f: 
    w = csv.DictWriter(f,['nim','mhname','ipk','code','name','status']) 
    w.writeheader() 
    for mySmallData in myBigData: 
        w.writerow(mySmallData) 


import pymongo
import urllib2
from bs4 import BeautifulSoup

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient['ambil-data']

myMahasiswa = mydb['mahasiswas']
myMakul = mydb['makuls']
myKuliah = mydb['kuliahs']

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
            name = biodata[0].find_all('td')[2].text
            nim = biodata[1].find_all('td')[2].text
            ipk = float(biodata[4].find_all('td')[2].text.split(' ')[0])
            mahasiswa = { "nim": nim, "name": name, "ipk": ipk}
            hslMahasiswa = myMahasiswa.insert_one(mahasiswa)
            print(nim, name, ipk)
            print('------------------------------------------------')

            makul = tables[1].find_all('tr')
            foo = makul[0]
            for item in makul:
                if item != foo:
                    code = item.find_all('td')[1].text
                    name = item.find_all('td')[3].text
                    status = item.find_all('td')[5].text
                    makul = {"code": code, "name": name}
                    print(id, code, name, status)
                    temp = myMakul.find_one(makul)
                    if temp != None:
                        kuliah = {
                            "mahasiswa": hslMahasiswa.inserted_id,
                            "makul": temp['_id'],
                            "status": status
                        }
                        myKuliah.insert_one(kuliah)
                    else:
                        hslMakul = myMakul.insert_one(makul)
                        kuliah = {
                            "mahasiswa": hslMahasiswa.inserted_id,
                            "makul": hslMakul.inserted_id,
                            "status": status
                        }
                        myKuliah.insert_one(kuliah)
            print("")

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

myclient = MongoClient('localhost', port=27017, username='mongoadmin', password='admin123')
mydb = myclient['scrapping2']

myMahasiswa = mydb['mahasiswas']
myMakul = mydb['makuls']
myKuliah = mydb['kuliahs']

link = 'http://en.dinus.ac.id/mahasiswa/A11.{0}.{1:0=5d}'
data = []

for thn in range(2016, 2018):

    start = 9346 if thn == 2016 else 10054
    stop = 10043 if thn == 2016 else 11000

    for idx in range(start, stop):
        
        url = link.format(thn, idx)
        print(url, 'link start')
        resp = requests.get(url, timeout=(1,5))
        r_text = resp.text
        soup = BeautifulSoup(r_text, 'html.parser')
        tables = soup.find_all('table')

        if len(tables) > 0:

            biodata = tables[0].find_all('tr')
            mhsStat = biodata[3].find_all('td')[2].text

            if mhsStat == "Aktif":
                name = biodata[0].find_all('td')[2].text
                nim = biodata[1].find_all('td')[2].text
                ipk = float(biodata[4].find_all('td')[2].text.split(' ')[0])
                mahasiswa = { "nim": nim, "name": name, "ipk": ipk}
                print(nim, name, ipk)
                hslMahasiswa = myMahasiswa.insert_one(mahasiswa)
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

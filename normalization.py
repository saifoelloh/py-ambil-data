import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

myclient = MongoClient('localhost', port=27017, username='mongoadmin', password='admin123')
mydb = myclient['scrapping2']

myMahasiswa = mydb['mahasiswas']
myMakul = mydb['makuls']
myKuliah = mydb['kuliahs']
myClasses = mydb['classes']

kuliahs = myKuliah.find()

for kuliah in kuliahs:
    print(kuliah['mahasiswa'])
    mahasiswa = myMahasiswa.find_one({"_id": kuliah['mahasiswa']})
    makul = myMakul.find_one({"_id": kuliah['makul']})
    kelas = {
        "name": mahasiswa['name'],
        "nim": mahasiswa['nim'],
        "ipk": mahasiswa['ipk'],
        "makul": makul['name'],
        "code": makul['code'],
        "status": kuliah['status'],
    }
    print(kelas)
    myClasses.insert_one(kelas)

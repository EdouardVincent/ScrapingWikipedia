import requests
from bs4 import BeautifulSoup
import sqlite3

conn = sqlite3.connect('database.sqlite')
cur = conn.cursor()

cur.execute ('''DROP TABLE IF EXISTS classement''')
cur.execute('''CREATE TABLE classement (rang  INTEGER AUTOINCREMENT UNIQUE, country TEXT, link TEXT)''')

url = 'https://fr.wikipedia.org/wiki/Liste_des_pays_par_population'

reponse = requests.get(url)

if reponse.ok: #Response[200]
    
    links = []
    soup = BeautifulSoup(reponse.text)
    title = soup.find('title')

    x=0
    tds = soup.findAll('td')
    for td in tds :

        a = td.find('a')
        if a != None :
            x+=1
            if x < 237 :
                a = td.find('a')
                link = a['href']
            
            c = link.split('/wiki/Fichier:Flag_of_')
            
            if c[0] == '' :
                link = c[1]

                d = link.split('.svg')

                link = d[0]

                
 
            country = link
            whole_link = ('https://fr.wikipedia.org/wiki/' + link)

            cur.execute('''INSERT INTO classement(country, link) VALUES (?,?)''',(country, whole_link))

            
        
    for row in cur.execute('''SELECT rang, country, link FROM classement'''):
        print(row)

cur.close()
        


        

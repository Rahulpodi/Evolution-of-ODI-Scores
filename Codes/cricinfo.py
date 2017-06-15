# -*- coding: utf-8 -*-
"""
"""

from bs4 import BeautifulSoup
from urllib import FancyURLopener
import pandas as pd
import re


class MyOpener(FancyURLopener):
        version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'

myopener = MyOpener()

# find all player ids

d = {1: "England",
   2: "Australia",
   3: "South Africa",
   4: "West Indies",
   5: "New Zealand",
   6: "India",
   7: "Pakistan",
   8: "Sri Lanka"}

player = pd.DataFrame(index = [], columns = ["Player Name", "Player ID"])
for i in range(1,9):
    page = myopener.open("http://www.espncricinfo.com/ci/content/player/caps.html?country="+str(i) +";class=2")
    soup = BeautifulSoup(page, "lxml")
    
    for row in soup.findAll("div", {"class": "ciPlayerbycapstable"})[0].findAll("ul"):
        if len(row.text.split('\n')) > 4:
            p = {}
            p["Country"] = d[i]
            p["Player Name"] = row.text.split('\n')[2]
            p['Player ID'] = re.findall(r'[0-9]+', row.find('a').get('href'))[0]
            player = player.append(p, ignore_index = True)


cols = {0 : "Team",
        1 : "Score",
        2 : "Overs",
        3 : "RPO",
        4 : "Inns",
        5 : "Result",
        6 : "Blank",
        7 : "Blank1",
        8 : "Opposition",
        9 : "Ground",
        10 : "Start Date"}

df = pd.DataFrame()
for n in range(157): 
    print n
    if n == 1:        
        link = "http://stats.espncricinfo.com/ci/engine/stats/index.html?class=2;template=results;type=team;view=innings"
        page = myopener.open(link)
        soup = BeautifulSoup(page, "lxml")
        
        for row in soup.findAll("table", { "class" : "engineTable" })[2].findAll("tr"):        
           tds = {}
           for j,col in enumerate(row.find_all('td')):
              tds[cols[j]] = col.text
           df = df.append(tds, ignore_index = True)
           
    elif n>1:
        link = "http://stats.espncricinfo.com/ci/engine/stats/index.html?class=2;page="+str(n)+";template=results;type=team;view=innings"
        page = myopener.open(link)
        soup = BeautifulSoup(page, "lxml")
        
        for row in soup.findAll("table", { "class" : "engineTable" })[2].findAll("tr"):        
           tds = {}
           for j,col in enumerate(row.find_all('td')):
              tds[cols[j]] = col.text
           df = df.append(tds, ignore_index = True)
           
df.to_csv("E:/Cricinfo/Data/Team_totals.csv",sep=",")

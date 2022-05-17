# Import libraries
from asyncio.windows_events import NULL
from genericpath import exists
from turtle import clear
from bs4 import BeautifulSoup
import requests
import re
import json
import pandas as pd, numpy as np
import xlwt
from xlwt import Workbook
import openpyxl
from openpyxl import load_workbook
from openpyxl.styles import Font
import os
import validators
import time
import sys


def getLast50(URL, URL2=''): #URL to site ; lenght of for loop ; both hubs for search ; cells list of given elements
    
    cells2= []
    #print('\n URL : ' + URL2 + '\n')
    #print(cells2)
    if(len(URL2) != 0):
    # print('recursion' + '\n')    
        cells2 = getLast50(URL2)
    #request website
    page = requests.get(URL)    
    # load the page content
    website = page.content   
    soup = BeautifulSoup(website, "html.parser")
    stable = soup.find('table')
    if(stable == None): #If player didnt play a hub the programm will return a empty list
        return []
    cells = [ ]
    rows = stable.findAll('tr')  

    for tr in rows[1:51]:
        # Process the body of the table
        row = []
        td = tr.findAll('td')
        #Datum
        row.append( td[1].text)   
        #Map  
        csmap = re.sub(r"[^a-zA-Z0-9_]","",td[3].text) #unnotige sachen weg machen
        row.append(csmap)
    

        #HLTV
        row.append( td[10].text)
        #Win or Lose

        if((td[11].text[(td[11].text).find('(')+1] == '+') or ('positive' in td[11]['class']) == True): #Check if Elo is + or td[11] has the attr 'positiv' which means it was a win
            row.append('Win')
        else : row.append('Lose')  

        #Score
        score = td[4].text
        ct = ''
        t = ''
        score=  re.sub(r"[^0-9/]","",score)
        slash = False
        for x in score:
            if (x != '/' and slash == False):
                ct += x
            elif (x == '/'):
                slash = True
            elif (x != '/' and slash == True):
                t += x

        totalScore = int(t) + int(ct)
        row.append(totalScore)   

        row.append(td[5].text)    
        

        cells.append( row )
    #[Datum, Map Name , HLTV, Win or Lose, TotalScore, Kills] cell format 
    if(len(cells2) != 0):
        cells = cells + cells2
        print('Multiple hubs where analyzed')
    #print('\n')
    #print(cells2)  
    #print(json.dumps(cells, indent = 4))            
    return cells




def getFinal(URL) :
    all_maps= ['de_mirage', 'de_inferno', 'de_overpass', 'de_dust2', 'de_ancient', 'de_vertigo', 'de_nuke']
    final = {
        'de_mirage' : {
            'TotalMaps' : 0,
            'WinRate' : 0,
            'HLTV' : 0,
            'KillsPerRound' : 0,
            'HLTVTotal' : 0,
            'TotalRounds' : 0  
        }, 
        'de_inferno' :  {
            'TotalMaps' : 0,
            'WinRate' : 0,
            'HLTV' : 0,
            'KillsPerRound' : 0,
            'HLTVTotal' : 0,
            'TotalRounds' : 0 
        },
        'de_overpass' :  {
            'TotalMaps' : 0,
            'WinRate' : 0,
            'HLTV' : 0,
            'KillsPerRound' : 0,
            'HLTVTotal' : 0,
            'TotalRounds' : 0
        },
        'de_dust2' : {
            'TotalMaps' : 0,
            'WinRate' : 0,
            'HLTV' : 0,
            'KillsPerRound' : 0,
            'HLTVTotal' : 0,
            'TotalRounds' : 0  
        },
        'de_ancient' :  {
            'TotalMaps' : 0,
            'WinRate' : 0,
            'HLTV' : 0,
            'KillsPerRound' : 0,
            'HLTVTotal' : 0,
            'TotalRounds' : 0  
        },
        'de_vertigo' :  {
            'TotalMaps' : 0,
            'WinRate' : 0,
            'HLTV' : 0,
            'KillsPerRound' : 0,
            'HLTVTotal' : 0,
            'TotalRounds' : 0 
        },
        'de_nuke' :  {
            'TotalMaps' : 0,
            'WinRate' : 0,
            'HLTV' : 0,
            'KillsPerRound' : 0,
            'HLTVTotal' : 0,
            'TotalRounds' : 0  
        },
    }

    for x in URL:
        for maps in all_maps:
            if(x[1] == maps):            
                tmp_old = final[maps]
                tmp_old['TotalMaps'] = tmp_old['TotalMaps'] + 1
                if(x[3] == 'Win'):
                    tmp_old['WinRate'] = tmp_old['WinRate'] + 1

                tmp_old['HLTVTotal']  =   tmp_old['HLTVTotal'] + float(x[2])
                tmp_old['TotalRounds'] = tmp_old['TotalRounds'] + int(x[4]) 
                tmp_old['KillsPerRound'] =  tmp_old['KillsPerRound'] + float(x[5])
                #print (tmp_old)
                final[maps] = tmp_old

    for x in final.values():  
        #print(x)
        if( int(x['TotalMaps']) !=  0  and int(x['TotalRounds']) !=  0 ): 
            x['HLTV'] = round (float(x['HLTVTotal'])  / int(x['TotalMaps']), 2)
            x['WinRate'] = round( x['WinRate'] / x['TotalMaps'] , 2)
            x['KillsPerRound'] = round(x['KillsPerRound'] / x['TotalRounds'] , 2)
            x.pop('HLTVTotal')

    return final
    
def toExcle(file_name, data, player_name = '',):
    #Data 5vs5
    data = pd.DataFrame(data) 
    data = data.dropna() #Drop rows with NaN  
    print(data)

   
    if(exists(os.path.abspath(os.getcwd()) + "/" + file_name + ".xlsx")):
        with pd.ExcelWriter(file_name + ".xlsx",mode="a",engine="openpyxl",if_sheet_exists="overlay") as writer:
         data.to_excel(writer, sheet_name=file_name, startrow=writer.sheets[file_name].max_row+2, index_label = player_name )
     
   
    else:
        data.to_excel(file_name+".xlsx", sheet_name=file_name,  index_label = player_name )             
    
def stripHubLink(hub):
    cleanURl= ''
    if(len(hub) != 0):
        for x in range(hub.find("?hub="), len(hub)): #strip string
            cleanURl += hub[x]
    return cleanURl     

#test cases : 
'''''
URL2 = 'https://faceitanalyser.com/matches/itsWuyu?hub=Liga%201%20SS%202022'
URL = 'https://faceitanalyser.com/matches/itsWuyu?hub=CS:GO%205v5%20EU'

last_5v5 = getLast50(URL, URL2) 
getFinal(last_5v5)
#toExcle('AXIS', getFinal(last_5v5), 'itsWuyu')

'''''
#user input: 
loop = True
while loop == True:
    print("Welcome the stats analyzer")
    try:
        players = int( input("How many players ? :"))
        hub = input("Optional : Add different hub to search (enter hub link): ")
        if(len(hub) == 0 or validators.url(hub) == True):
            hub_stip = stripHubLink(hub)
            nickname = []
            team = "Analzye1"
            if(players > 1):
                team = str(input("Please enter a team name (optional)"))
                if(len(team) == 0):
                    team = "Analzye1"
            for i in range(int(players)) :
                username = input("Faceit Username " + str(i+1) + " :")
                nickname.append(username)
            for i in nickname:
                print('\n'+i + '\n')
                URL = 'https://faceitanalyser.com/matches/' + i + '?hub=CS:GO%205v5%20EU'
                if(len(hub_stip) != 0):
                    URL2 = 'https://faceitanalyser.com/matches/' + i + hub_stip
                    last_5v5 = getLast50(URL, URL2)          
                    print(URL + '\n' + URL2)
                    toExcle(team, getFinal(last_5v5), i)
                 
                else :
                    print(URL + '\n')
                    last_5v5 = getLast50(URL)    
                    toExcle(team, getFinal(last_5v5), i)
            loop = False
            print('This window will close automaticly in 3 seconds')
            time.sleep(3)        
            sys.exit()


        else:
            print("Please enter a correct hub url")
            continue    
    except ValueError:
        print("Please enter a number.")
        continue

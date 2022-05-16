# Import libraries
from asyncio.windows_events import NULL
from turtle import clear
from bs4 import BeautifulSoup
import requests
import re
import json
import pandas as pd
import xlwt
from xlwt import Workbook
import openpyxl
from openpyxl import load_workbook
from openpyxl.styles import Font



def getMaps(URL):
     #request website

    page = requests.get(URL)
    
    # load the page content
    website = page.content
    

    soup = BeautifulSoup(website, "html.parser")

    div = soup.find("div", {"id": "view2_stats"})
    stable = div.find('table')
    cells = [ ]
    rows = stable.findAll('tr')
    for tr in rows[1:10]:
        # Process the body of the table
        row = []
        td = tr.findAll('td')
        #Map
        csmap = re.sub(r"[^a-zA-Z0-9_]","",td[0].text) #unnotige sachen weg machen
        row.append(csmap)  
        #Winrate
        row.append( td[4].text)
        #HS%
        row.append( td[8].text) 
        #KPR    
        row.append( td[9].text)
        #HLTV
        row.append( td[11].text)    
        cells.append( row )
     #[Map Name, Winrate , HS%, KPR, HLTV ] cell format   
    return cells

def getLast50(URL): #URL to site ; lenght of for loop ; both hubs for search ; cells list of given elements

    #request website
    page = requests.get(URL)    
    # load the page content
    website = page.content   
    soup = BeautifulSoup(website, "html.parser")
    stable = soup.find('table')
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
        (td[11].text).find('(')
        if(td[11].text[(td[11].text).find('(')+1] == '+'):
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
        
        #print(ct  +  " & "  + t)

        cells.append( row )
    #[Datum, Map Name , HLTV, Win or Lose, TotalScore, Kills] cell format      
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
    
def toExcle(file_name, data):
    
    data = pd.DataFrame(data) 
    data = data.dropna() #Drop rows with NaN

    print(data)
    data.to_excel((file_name+".xlsx"),sheet_name=file_name)    
    wb = load_workbook((file_name+'.xlsx'))    
    ws = wb[file_name]
    ws['A1'] = file_name
    ws['A1'].font = Font(bold = True)
    ws['A7'] = 'https://faceitanalyser.com/matches/' + file_name + '?hub=CS:GO%205v5%20EU'
    ws['A7'].font = Font(bold = True)
    wb.save((file_name+'.xlsx'))          
 
players = input("How many Players ? :")
nickname = []
for i in range(int(players)) :
    username = input("Faceit Username " + str(i+1) + " :")
    nickname.append(username)


for i in nickname:
    print('\n'+i + '\n')
    URL = 'https://faceitanalyser.com/matches/' + i + '?hub=CS:GO%205v5%20EU'
    print(URL)
    last50 = getLast50(URL)   
    toExcle(i, getFinal(last50))
   








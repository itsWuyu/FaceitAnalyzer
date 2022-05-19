
# FaceitAnalyzer

Just a little project to get better in CS:GO

The Programm helps you to see where your strengths and weaknesses are by scanning your last matches.


## Run Locally

Install auto-py-to-exe

```bash
pip install auto-py-to-exe
```

Run auto-py-to-exe

```bash
auto-py-to-exe -nu .\main.py
```

Follow auto-py-to-exe instructions





## Usage/Examples

```
"How many players ? : " -> enter how many people you want to analyze

"Optional : Add different hub to search (enter hub link): " -> enter a second faceit hub link (full link) to scan for example : https://faceitanalyser.com/matches/itsWuyu?hub=Red%20Bull%20Flick%20Community%20Hub

"Please enter a team name (optional): " -> enter a team name if you want to analzye a hole team. By default it is "Analzye1". This is also the Excel file name

"Faceit Username X : " -> enter faceit username

```


## FAQ

#### Where do you get the stats from ?

I am using https://faceitanalyser.com/ to get the relevant infos.

#### Whats the difference between this programm and faceitanalyser.com ?

faceitanalyser shows every game played even the custom hubs.  
This programm shows only the relevant matches and creats the statistics from these. 

#### What will happen if I add a second hub and one of the players did not play this hub ?

Nothing, the programm will skip this player for the additional hub

#### What default hub is used ?
The CS:GO 5v5 EU is the default hub. You can change the default hub by editing the end of the URL variable
to your desired hub.  
For example : 
```pyhton
URL = 'https://faceitanalyser.com/matches/' + i + '?hub=CSGO%205v5'
``` 

## Have a nice day

![CS:GO -  Flashbang dance baby by n0thing](https://i.makeagif.com/media/7-13-2017/y_b8YO.gif)


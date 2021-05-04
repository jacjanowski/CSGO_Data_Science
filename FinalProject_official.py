#!/usr/bin/env python
# coding: utf-8

# In[530]:


from time import sleep
import csv
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup


# driver = webdriver.Chrome(ChromeDriverManager().install())


url = "https://www.hltv.org/stats"
players = []
teams = []
teamRanks = []

fields1 = ['Player', 'Team', 'Maps', 'K-D_Diff', 'K/D', 'Rating(1.0)'] 
fields2 = ['Teams' ,'Maps', 'Won-Lost', 'Pistol_Win_%', 'Round_2_Conversion', 'Round_2_Break'] 
fields3 = ['Team', 'Maps', 'K-D_Diff', 'K/D', 'Rating(2.0)']

    
def writeToCSV(file, header, data):
    filename = file

    # writing to csv file 
    with open(filename, 'w') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 

        # writing the fields 
        csvwriter.writerow(header) 

        # writing the data rows 
        csvwriter.writerows(data)
        
        
def get_parsed_page(url):
    # This fixes a blocked by cloudflare error i've encountered
    headers = {
        "referer": "https://www.hltv.org/stats",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    return BeautifulSoup(requests.get(url, headers=headers).text, "lxml")

def get_parsed_page2(url):
    # This fixes a blocked by cloudflare error i've encountered
    headers = {
        "referer": "https://ggscore.com/en/csgo",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    return BeautifulSoup(requests.get(url, headers=headers).text, "lxml")


        
def playerPerformanceByDate():
    startDate = input("Start date (yyyy-mm-dd, leave blank for 'All-time' results): ")
    endDate = input("End date (yyyy-mm-dd, leave blank for 'All-time' results): ")
    print("Map Selection. Choose one from the following: all, vertigo, dust2, mirage, overpass, nuke, inferno, cobblestone, cache, train.")
    mapName = input("Choose the map: ")
    
    dateConversion = url + "/players?startDate=" + startDate + "&endDate=" + endDate + "&maps=de_"+mapName.lower() + "&rankingFilter=Top50";
    print(dateConversion)
    soup = get_parsed_page(dateConversion)
    statTable = soup.tbody;
    for tr in statTable.find_all("tr"):
        newArray = []
        for td in tr.find_all('td'):
            newArray.append(td.get_text())
        players.append(newArray)
    writeToCSV("data.csv", fields1, players)
   

def pistolRoundByDate():
    startDate = input("Start date (yyyy-mm-dd, leave blank for 'All-time' results): ")
    endDate = input("End date (yyyy-mm-dd, leave blank if you want 'All-time' results): ")
    print("Map Selection. Choose one from the following: all, vertigo, dust2, mirage, overpass, nuke, inferno, cobblestone, cache, train.")
    mapName = input("Choose the map: ")
    teamSide = input("Enter team ('TERRORIST or COUNTER_TERRORIST'):")
    pistol = url + "/teams/pistols?startDate=" + startDate + "&endDate=" + endDate + "&maps=de_"+mapName.lower()+"&side=" + teamSide.upper() + "&rankingFilter=Top50"; 
    print(pistol)
    soup = get_parsed_page(pistol)
    pistolTable = soup.tbody;

    for tr in pistolTable.find_all("tr"):
        newArray = []
        for td in tr.find_all('td'):
            newArray.append(td.get_text())
        teams.append(newArray)
    writeToCSV("data2.csv", fields2, teams)

def teamRank():
    startDate = input("Start date (yyyy-mm-dd, leave blank for 'All-time' results): ")
    endDate = input("End date (yyyy-mm-dd, leave blank if you want 'All-time' results): ")
    print("Map Selection. Choose one from the following: all, vertigo, dust2, mirage, overpass, nuke, inferno, cobblestone, cache, train.")
    mapName = input("Choose the map: ")
    teamURL = url + "/teams?startDate="+startDate+"&endDate=" + endDate + "&maps=de_"+ mapName.lower() + "&rankingFilter=Top50"; 
    print(teamURL)
    soup = get_parsed_page(teamURL)
    teamRankTable = soup.tbody;
    
    for tr in teamRankTable.find_all("tr"):
        newArray = []
        for td in tr.find_all("td"):
            newArray.append(td.get_text())
        teamRanks.append(newArray)
    writeToCSV("data3.csv", fields3, teamRanks)
    
    
    
# Calling functions and creating our csv files dynamically    
playerPerformanceByDate()
pistolRoundByDate()
teamRank()
print('-----------------------------------------------------------------------------------------------------------')
print('RUN THE 3 CELLS BELOW TO SEE THE "PLAYER DATAFRAME" AND "TEAM PISTOL DATAFRAME" AND "TEAM RANKS DATAFRAME"')
print('-----------------------------------------------------------------------------------------------------------')


# In[531]:


import matplotlib
print('matplotlib: {}'.format(matplotlib.__version__))


# In[ ]:





# In[532]:


#Player Performance dataframe
print("-------------------------------")
print('Player Dataframe')
print("-------------------------------")
player_df = pd.read_csv('data.csv')
player_df = player_df.dropna(axis='columns', how ='all')
player_df.head(20)


# In[533]:


# Team Pistol dataframe
print("-------------------------------")
print('Team Pistol Dataframe')
print("-------------------------------")
team_pistol_df = pd.read_csv('data2.csv')
team_pistol_df.head(20)


# In[534]:


# Team Ranks dataframe
print("-------------------------------")
print('Team Overall Rank Dataframe')
print("-------------------------------")
team_rank_df = pd.read_csv('data3.csv')
team_rank_df.head(20)


# In[540]:


# Get the names of the players in each team depending what team the user chooses.
team_and_player_ratings = 'https://ggscore.com/en/csgo/team/';
teamName = input("Choose a team to view the players on that team: ")
url = team_and_player_ratings + teamName
teammates = []

soup = get_parsed_page2(url);
teamTable = soup.find("div", "teamP")
players = teamTable.find("div", "row")
for name in players.find_all(attrs={"class": "pllink"}):
    teammates.append(name.text)
print(teammates)


# In[541]:


player_rating = 'https://ggscore.com/en/csgo/player/'
# playerName = input('Enter a player\'s name: ')
strength =  []
form = []

for i in range(len(teammates)):
    print(teammates[i].lower())
    url = player_rating + teammates[i].lower()
    soup = get_parsed_page2(url)
    playerTable = soup.find_all("span", class_="counter")
    form.append(playerTable[0].text)
    strength.append(playerTable[1].text)
#     print(teammates[i] + "'s' Form level is " + playerTable[0].text + " with a Strength level of " + playerTable[1].text) 
print("Team players:",teammates)
print("Form level:",form)
print("Strength level:",strength)


# In[542]:


import matplotlib
import matplotlib.pyplot as plt
import numpy as np
x = np.arange(len(teammates))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, form, width, label='Form')
rects2 = ax.bar(x + width/2, strength, width, label='Strength')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Scores')
ax.set_title('Scores by Form and Strength Levels')
ax.set_xticks(x)
ax.set_xticklabels(teammates)
ax.legend()


ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)

fig.tight_layout()

plt.show()


# In[543]:


soup = get_parsed_page('https://www.hltv.org/events/5728/dreamhack-masters-spring-2021%27')
teams_in_tournament = soup.find_all("div", "text")

print("---------------------------------------------------------------------------------------------------------")
print("These teams will be in the upcoming tournament known as DreamHack Master Spring 2021 (Apr 29th - May 9th)\nFrom this, we can use these teams and the data provided to predict which team has the overhand on the other.")
print("---------------------------------------------------------------------------------------------------------")
for team in teams_in_tournament:
    print("-" + team.text)
    


# In[ ]:





# In[545]:


faze = 'https://www.hltv.org/stats/teams/maps/6667/faze'
g2 = 'https://www.hltv.org/stats/teams/maps/5995/g2'
gambit = 'https://www.hltv.org/stats/teams/maps/6651/gambit'
astralis = 'https://www.hltv.org/stats/teams/maps/6665/astralis'
heroic = 'https://www.hltv.org/stats/teams/maps/7175/heroic'
natus_vincere = 'https://www.hltv.org/stats/teams/maps/4608/natus-vincere'
virtus_pro = 'https://www.hltv.org/stats/teams/maps/5378/virtuspro'
furia = 'https://www.hltv.org/stats/teams/maps/8297/furia'
complexity = 'https://www.hltv.org/stats/teams/maps/5005/complexity'
BIG = 'https://www.hltv.org/stats/teams/maps/7532/big'
spirit = 'https://www.hltv.org/stats/teams/maps/7020/spirit'
vitality = 'https://www.hltv.org/stats/teams/maps/9565/vitality'
mousesports = 'https://www.hltv.org/stats/teams/maps/4494/mousesports'
extra_salt = 'https://www.hltv.org/stats/teams/maps/10948/extra-salt'
pain = 'https://www.hltv.org/stats/teams/maps/4773/pain'
fiend = 'https://www.hltv.org/stats/teams/maps/11066/fiend'

soup = get_parsed_page(heroic)
two_grid = soup.find("div", "two-grid")
map_pool = two_grid.find_all(attrs={"class": "map-pool"})
stats_for_maps = two_grid.find_all("div",'stats-rows standard-box')
maps = []
data = []

def divide_chunks(lst, n):
      
    # looping till length l
    for i in range(0, len(lst), n): 
        yield lst[i:i + n]  
        
for map_name in map_pool:
    
    maps.append(map_name.text)

    
divs = soup.find_all('div', {'class': 'stats-row'})
for div in divs:
    # want the second span in the div
    newArray = []
    span = div.find_next('span').find_next('span')
    data.append(span.text)

x = list(divide_chunks(data, 5))


res = {maps[i].strip(): x[i] for i in range(len(maps))}
win_tie_loss = []

dict2 = res.copy()

for key in res:
    result = res[key][0].split(" / ")
    win_tie_loss.append(result)
    print(key, '->',result )


      
print ("\nResultant dictionary is : " +  str(res))


# In[ ]:





# In[546]:


map_table = pd.DataFrame.from_dict(res, orient='index',
                       columns=['Win/Tie/Loss', 'Win_Rate', 'Total_Rounds', 'Round_Win_%_First_Kill', 'Round_Win_%_First_Death'])
map_table


# In[547]:


dict2 = dict(res)
arr = []
for item in dict2.values():
    item.remove(item[0])
    item.remove(item[1])
    r = [sub[ : -1] for sub in item]    
    arr.append(r)

arr = [list(map(float, sublist)) for sublist in arr]
# print(arr)
ress = {maps[i].strip(): arr[i] for i in range(len(maps))}
print(ress)


# In[548]:


map_table = pd.DataFrame.from_dict(ress, orient='index',
                       columns=['Win_Rate','Round_Win_%_First_Kill', 'Round_Win_%_First_Death'])
map_table.plot(kind="bar")
plt.title("Likelyhood of Winning Round")
plt.xlabel("Map")
plt.ylabel("Percentage of Winning")


# In[ ]:





# In[ ]:





# In[549]:


df = pd.read_csv("data.csv", index_col = 0)
df1 = df[['K/D', 'Rating(1.0)']]

plt.rcParams["figure.figsize"] = [16,9]
plt.figure(figsize=(8, 8))
df1.head(30).plot(kind="bar")
plt.show()


# In[550]:


df2 = pd.read_csv('data2.csv',index_col=0).head(30)
df3 = df2[['Pistol_Win_%', 'Round_2_Conversion', 'Round_2_Break']]
df3 = df3.replace('%','', regex=True)
plt.rcParams["figure.figsize"] = [16,9]
df3=df3.astype(float)
df3.plot(kind="bar")
plt.show()


# In[ ]:





# In[ ]:





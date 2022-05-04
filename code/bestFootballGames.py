#   API KEY
#	88c9c6c677874894b40c8d72629e1f63
# Bundesliga ID=2002, Serie A ID=2019, "Primeira Liga ID=2017", "Premier League ID=2021", "Ligue 1 ID=2015", "Primera Division ID=2014"
import requests
import json
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from io import BytesIO
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from datetime import datetime as dt
from threading import Thread

competition_list=["Bundesliga", "Serie A", "Primeira Liga", "Premier League", "Ligue 1", "Primera Division"]
competition_ids=[2002,2019,2017,2021,2015,2014]

def make_competitions_request():
    headers={'X-Auth-Token': '88c9c6c677874894b40c8d72629e1f63'}
    url = 'https://api.football-data.org/v2/competitions'
    x = requests.get(url,headers=headers)
    return x

def write_file(data,name):
    with open('D:\Programmierprojekte\Fussball/'+name+".json", 'w') as outfile:
        json.dump(data,outfile,indent=4)

def make_matches_request(von,bis):
    headers={'X-Auth-Token': '88c9c6c677874894b40c8d72629e1f63'}
    url = 'https://api.football-data.org/v2/matches?dateFrom='+von+'&dateTo='+bis
    response = requests.get(url,headers=headers)
    return response

def make_standings_request(competition_id):
    headers={'X-Auth-Token': '88c9c6c677874894b40c8d72629e1f63'}
    url = 'https://api.football-data.org/v2/competitions/'+str(competition_id)+'/standings'
    response = requests.get(url,headers=headers)
    return response

def get_all_standings():
    all_standings=[]
    for id in competition_ids:
        x=json.loads(make_standings_request(id).text)
        all_standings.append(x)
    return all_standings

def find_matches(data):
    top_six_matches=[]
    for match in data['matches']:
        y=match['competition']['id']
        status=match['status']
        for competition_id in competition_ids:
            if competition_id==y and status!= "FINISHED":
                top_six_matches.append(match)
    return top_six_matches

def make_special_match_format(matches):
    full_match_data=[]
    for i,match in enumerate(matches):
        x={
            "matchID":i,
            "competitionID":match['competition']['id'],
            "infos": {
                "time":match['utcDate'],
                "homeTeam":match['homeTeam']['name'],
                "homeTeamID":match['homeTeam']['id'],
                "homeTeamLogo":"",
                "homeTeamPosition":1,
                "awayTeam":match['awayTeam']['name'],
                "awayTeamID":match['awayTeam']['id'],
                "awayTeamLogo":"",
                "awayTeamPosition":1
            },
            "importance":20
        }
        full_match_data.append(x)
    return full_match_data

def fillout_matches(matches,standings):
    for match in matches:
        competition=match['competitionID']
        index=get_index(competition)
        #homeTeamHandling
        homeTeamID=match['infos']['homeTeamID']
        homeInfo=get_standing(json.dumps(standings[index]),homeTeamID)
        match['infos']['homeTeamPosition']=homeInfo[0]
        match['infos']['homeTeamLogo']=homeInfo[1]
        #awayTeam handling
        awayTeamID=match['infos']['awayTeamID']
        awayInfo=get_standing(json.dumps(standings[index]),awayTeamID)
        match['infos']['awayTeamPosition']=awayInfo[0]
        match['infos']['awayTeamLogo']=awayInfo[1]
    return matches

def get_index(value):
    if(value==2002):
        return 0
    elif(value==2019):
        return 1
    elif(value==2017):
        return 2
    elif(value==2021):
        return 3
    elif(value==2015):
        return 4
    elif(value==2014):
        return 5
    
def get_standing(tabelle,id):
    x=json.loads(tabelle)
    for team in x["standings"][0]['table']:
        if team["team"]['id']==id:
            return team["position"],team['team']["crestUrl"]

def calculate_importance(match):
    if match['infos']['homeTeamPosition']>match['infos']['awayTeamPosition']:
        importance=match['infos']['homeTeamPosition']-match['infos']['awayTeamPosition']
        return importance
    else:
        importance=match['infos']['awayTeamPosition']-match['infos']['homeTeamPosition']
        return importance

def bubblesort_importance(matches):
    go=True
    while go==True:
        changed=False
        for i in range(0,len(matches)-1):
            if matches[i+1]['importance']<matches[i]['importance']:
                changed=True
                temp=matches[i]
                matches[i]=matches[i+1]
                matches[i+1]=temp
        if changed==False:
            go=False
    return matches

def bubblesort_standings(matches):
    #print("Länge matches ", matches)
    matches_neu=[]
    i=0
    while i<len(matches):
        equal_importance=[]
        count=1
        #print("i ", i," count",count)
        while count+i<len(matches) and matches[i]['importance']==matches[i+count]['importance']:
            equal_importance.append(matches[i+count])
            count=count+1
        if count!=1:
            temp=bubblesort(equal_importance)
            for k in range(0,count-1):
                matches_neu.append(temp[k])
        else:
            matches_neu.append(matches[i])
        i=i+count
    return matches_neu

def bubblesort(matches):
    go=True
    while go==True:
        changed=False
        for i in range(0,len(matches)-1):
            value_one=0
            if matches[i]['infos']['awayTeamPosition']<matches[i]['infos']['homeTeamPosition']:
                value_one='awayTeamPosition'
            else:
                value_one='homeTeamPosition'
            if matches[i+1]['infos']['awayTeamPosition']<matches[i+1]['infos']['awayTeamPosition']:
                value_two='awayTeamPosition'
            else:
                value_two='homeTeamPosition'
            if matches[i+1]['infos'][value_two]<matches[i]['infos'][value_one]:
                changed=True
                temp=matches[i]
                matches[i]=matches[i+1]
                matches[i+1]=temp
        if changed==False:
            go=False
    return matches

def sort_by_day(matches):
    games_weekdays=[[],[],[],[],[],[],[]]
    for match in matches:
        date=match['infos']['time']
        date=get_datetime(date)
        weekday=date.weekday()
        games_weekdays[weekday].append(match)
    #pprint(games_weekdays)
    for i,x in enumerate (games_weekdays):
        if len(x)==0:
            games_weekdays.pop(i)
    return games_weekdays

def formate_time(input):
    date_time=get_datetime(input)
    final=str(date_time.hour)+":"+str(date_time.minute)
    final=final.replace(" ","")
    final=get_weekday(date_time.weekday())+" "+final
    return final

def get_datetime(input):
    input=input.replace("T","")
    input=input.replace("Z","")
    date_time = dt.strptime(input,"%Y-%m-%d%H:%M:%S")
    return date_time

def get_weekday(day):
    if day==0:
        return "Mon"
    elif day==1:
        return "Tud"
    elif day==2:
        return "Wen"
    elif day==3:
        return "Thu"
    elif day==4:
        return "Fri"
    elif day==5:
        return "Sat"
    else:
        return "Sun" 

def get_Data():
    f = open("D:\Programmierprojekte\Fussball\InteressantesDikument.json", "r")
    t=json.loads(f.read())
    return t

def convert_input_to_format(von,bis):
    new_von=von[6:]+"-"+von[3:5]+"-"+von[0:2]
    new_bis=bis[6:]+"-"+bis[3:5]+"-"+bis[0:2]
    return [new_von,new_bis]

def start(von,bis):
    standings=get_all_standings()
    von_bis=convert_input_to_format(von,bis)
    data=make_matches_request(von_bis[0],von_bis[1])
    data=json.loads(data.text)
    matches=find_matches(data)
    matches=make_special_match_format(matches)
    matches=fillout_matches(matches,standings)
    #matches=get_Data()
    for match in matches:
        match['importance']=calculate_importance(match)
    matches=bubblesort_importance(matches)
    weekdays=sort_by_day(matches)
    new_weekdays=[]
    for i in range(0,len(weekdays)):
        #write_file(weekdays[i],str(i))
        if len(weekdays[i])>2:
            weekdays[i]=bubblesort_standings(weekdays[i])
        if len(weekdays[i])!=0:
            new_weekdays.append(weekdays[i])
    return new_weekdays

class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.geometry("1900x1000")
        self.make_frms()
        self.fill_frm1()
        self.stop_garbage=[]

    def fill_frm1(self):
        self.date_from = tk.StringVar()
        self.date_from.set("dd.mm.yyyy")
        ttk.Entry(self.frm1, textvariable= self.date_from).grid(column=1, row=0)
        self.date_to = tk.StringVar()
        self.date_to.set("dd.mm.yyyy")
        ttk.Entry(self.frm1, textvariable= self.date_to).grid(column=1, row=1)
        date_from_label=ttk.Label(self.frm1,text="Datum-Von").grid(column=0, row=0)
        date_to_label=ttk.Label(self.frm1,text="Datum-Bis").grid(column=0, row=1) 
        ttk.Button(self.frm1, text = "Absenden", command=lambda:self.start_thread()).grid(column=1, row=3, sticky=tk.NSEW) 

    def fill_frm2(self):
        self.pb = ttk.Progressbar(self.frm2,orient='horizontal',mode='indeterminate',length=280)
        self.pb.grid(column=1,row=1)

    def make_frms(self):
        self.frm1=ttk.Frame(self)
        self.frm2=ttk.Frame(self)
        self.frm3=ttk.Frame(self)
        self.frm1.grid(column=0,row=0,sticky=tk.NSEW)
        self.frm2.grid(column=0,row=0,sticky=tk.NSEW)
        self.frm3.grid(column=0,row=0,sticky=tk.NSEW)
        self.change_frame(self.frm1)

    def start_thread(self):
        self.fill_frm2()
        self.change_frame(self.frm2)
        self.pb.start()
        self.p2= Thread(target=lambda:self.get_data())
        self.p2.start()
        self.monitor()
        print("Thread started")

    def change_frame(self,frame):
        frame.tkraise()

    def monitor(self):
        if self.p2.is_alive()== True:
            self.after(1000,lambda:self.monitor())
        else:
            self.change_frame(self.frm3)

    def get_data(self):
        self.get_frame()
        self.pb.stop()

    def load_logo(self,url):
        if url[len(url)-3:len(url)]!="png":
            response = requests.get(url)
            drawing = svg2rlg(BytesIO(response.content))
            x=renderPM.drawToPIL(drawing)
            logo_eins = ImageTk.PhotoImage(x.resize((50, 50)))
            return logo_eins
        else: 
            response = requests.get(url)
            logo_eins = ImageTk.PhotoImage(Image.open(BytesIO(response.content)).resize((50, 50)))
            return logo_eins
    
    def get_frame(self):
        #i=0,1,2,3... match=values
        #Damit die Bilder geladen werden muss der Speicher irgendwie "reverenziert" werden um nicht weggeworfen zu werden. 
        #Deswegen speichern in der Liste. Keine Ahnung was das mit der Memory macht. Aber anders will es nicht...
        matches=start(self.date_from.get(),self.date_to.get())
        for y in range (0,len(matches)):
            tk.Label(self.frm3,text=get_weekday(get_datetime(matches[y][0]['infos']['time']).weekday()),borderwidth=2, relief="groove").grid(column=y,row=0,sticky=tk.NSEW)
            for i,match in enumerate (matches[y][0:9]):
                #Fenster für ein Spiel
                match_frame=ttk.Frame(self.frm3,padding=0,borderwidth=2, relief="groove")
                match_frame.grid(column=y, row=i+1, sticky=tk.NSEW)
                #Hinzufügen der Zeit
                tk.Label(match_frame,text=formate_time(match['infos']['time'])).grid(column=1, row=1, sticky=tk.NSEW)
                #Hinzufügen Ränge
                tk.Label(match_frame,text=str(match['infos']['homeTeamPosition'])+". vs "+str(match['infos']['awayTeamPosition'])+".").grid(column=1, row=0, sticky=tk.NSEW)
                #Hinzufügen Logo 1
                try:
                    url=match['infos']['homeTeamLogo']
                    logo_eins=self.load_logo(url)
                    tk.Label(match_frame,image=logo_eins).grid(column=0,row=0,sticky=tk.W)
                    self.stop_garbage.append(logo_eins)
                except:
                    tk.Label(match_frame).grid(column=0,row=0)
                #Hinzufügen Logo 2
                try:
                    url=match['infos']['awayTeamLogo']
                    logo_zwei = self.load_logo(url) 
                    tk.Label(match_frame,image=logo_zwei).grid(column=3,row=0,sticky=tk.W)
                    self.stop_garbage.append(logo_zwei)
                except:
                    tk.Label(match_frame).grid(column=0,row=0)
                #Hinzufügen TeamName 1
                tk.Label(match_frame,text=match['infos']['homeTeam'],wraplength=60).grid(column=0, row=1)
                #Hinzufügen TeamName 2
                tk.Label(match_frame,text=match['infos']['awayTeam'],wraplength=60).grid(column=3, row=1, sticky=tk.N) 
    
app=App()
app.mainloop()


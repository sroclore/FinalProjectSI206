from unicodedata import name
import requests
from bs4 import BeautifulSoup
import os
import sqlite3

#Step 1a: Get attendance numbers for 2012-2021
def getAttendanceMLB(year):
    baseURL = 'https://www.espn.com/mlb/attendance/_/year/'

    try:
        year = str(year)
        r = requests.get(f'{baseURL}{year}')
        soup = BeautifulSoup(r.text, 'html.parser')
        rows = soup.find_all('tr')
    except:
        print('Exception')

    info = []
    for row in rows[2:]:
        try:
            data = row.find_all('td')
            team = data[1].find('a').text
            avgAttendance = data[4].text
            totAttendance = data[3].text
        except:
            team = 'NO ATTENDANCE - COVID19'
            avgAttendance = 'NO ATTENDANCE - COVID19'
            totAttendance = 'NO ATTENDANCE - COVID19'
        info.append((team, avgAttendance, totAttendance))
    return info
db_name = 'AttendanceDatabase'
path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path+'/'+db_name)
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS AttendanceMLB')
conn.commit()
#Step 2: Add attendance numbers and teams to SQL
def createDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    
    cur.execute('CREATE TABLE IF NOT EXISTS AttendanceMLB (year INTEGER, team_id INTEGER, avgAttendance INTEGER, totAttendance INTEGER)')
    conn.commit()
    return cur, conn

def getTeamID(db_name):
    data = getAttendanceMLB(2021)
    idDic = {}
    team_id = 0
    for team in data:
        team_id += 1
        idDic[team[0]] = team_id
    return idDic

def addTeamTable(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS MLBteams (team_id INTEGER PRIMARY KEY, teamName TEXT)')
    conn.commit()
    return cur, conn
    
def addData(year, db_name):
    cur, conn = createDatabase(db_name)
    data = getAttendanceMLB(year)
    idDic = getTeamID(db_name)

    for tup in data:
        try:
            team_id = idDic[tup[0]]
            avgAttendance = tup[1]
            totAttendance = tup[2]
        except:
            team_id = 0
            avgAttendance = 0
            totAttendance = 0
        cur.execute('INSERT OR IGNORE INTO AttendanceMLB (year, team_id, avgAttendance, totAttendance) VALUES (?, ?, ?, ?)', (year, team_id, avgAttendance, totAttendance))
    conn.commit()

    cur, conn = addTeamTable(db_name)

    for team, id in idDic.items():
        cur.execute('INSERT OR IGNORE INTO MLBteams (team_id, teamName) VALUES (?, ?)', (id, team))
    conn.commit()

def main():
    year = 2012
    db_name = 'AttendanceDatabase'
    while year != 2022:
       getAttendanceMLB(year)
       getTeamID(db_name)
       createDatabase(db_name)
       addTeamTable(db_name)
       addData(year, db_name)
       year += 1

main()




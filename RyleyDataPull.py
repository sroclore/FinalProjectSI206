import requests
from bs4 import BeautifulSoup
import os
import sqlite3

#Step 1a: Get attendance numbers for 2021-2012
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
        data = row.find_all('td')
        team = data[1].find('a').text
        avgAttendance = data[4].text
        totAttendance = data[3].text
        info.append((team, avgAttendance, totAttendance))

    return info

#Step 2: Add attendance numbers and teams to SQL
def createDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    
    cur.execute('CREATE TABLE IF NOT EXISTS AttendanceMLB (team_id INTEGER PRIMARY KEY, teamName TEXT, avgAttendance INTEGER, totAttendance INTEGER')
    conn.commit()
    return cur, conn

def addData(year, db_name):
    cur, conn = createDatabase(db_name)
    data = getAttendanceMLB(year)
    
    

#Step 3: Create visualizations and such




import requests
from bs4 import BeautifulSoup

#Step 1a: Get attendance numbers for 2021-2012
def getAttendanceMLB():
    baseURL = 'https://www.espn.com/mlb/attendance/_/year/'

    years = ['2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012']
    for year in years:
        r = requests.get(f'{baseURL}{year}')
        soup = BeautifulSoup(r.text, 'html.parser')
        rows = soup.find_all('tr')

    info = []
    for row in rows[2:]:
        data = row.find_all('td')
        team = data[1].find('a').text
        avgAttendance = data[4].text
        totAttendance = data[3].text
        info.append((team, avgAttendance, totAttendance))

    return info

print(len(getAttendanceMLB()))

#Step 1b: Get teams from ESPN api

#Step 2: Add attendance numbers and teams to SQL (team table and attendance table, shared team id)

#Step 3: Create visualizations and such




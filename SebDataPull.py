import unittest
import sqlite3
import json
import os
from bs4 import BeautifulSoup
import requests


# Name: Sebastian Roclore
# Who did you work with: Ryley Larson

def getAttendancePrem(year):
    baseURL = 'https://www.footballwebpages.co.uk/premier-league/attendances/'
    
    try:
        year = str(year)
        r = requests.get(f'{baseURL}{year}')
        soup = BeautifulSoup(r.text, 'html.parser')
        rows = soup.find_all('table')
        print(rows)
    except:
        print('Exception')

    info = []
    # for row in rows.contents:
    #     data = row.find_all('td')
        # print(data)
        # team = data[1].find('a').text
        # avgAttendance = data[4].text
        # totAttendance = data[3].text
        # info.append((team, avgAttendance, totAttendance))

    return info


# def get_teams_by_season(season):
#     url = "https://football-web-pages1.p.rapidapi.com/league-table.json"

#     querystring = {"comp":"1", "year":{season}}

#     headers = { 
# 	    "X-RapidAPI-Host": "football-web-pages1.p.rapidapi.com",
# 	    "X-RapidAPI-Key": "e34cfc2358mshb0d0a32b739f2e0p1fa103jsnf9f3985beab7"
#     }
#     response = requests.request("GET", url, headers=headers, params=querystring)
#     year_table = json.loads(response.text)
#     L = []
#     for x,y in year_table.items():
#         for teams in y.items():
#             t = teams[1]
#             for team in t:
#                 try:
#                     val = team['name']
#                     L.append(val)
#                 except:
#                     break   
#     return L

# def get_team_ids():
#     L = [] 



def prem_data_grab(season):
    # L = get_teams_by_season(season)

    url = "https://football-web-pages1.p.rapidapi.com/attendances.json"

    headers = {
        "X-RapidAPI-Host": "football-web-pages1.p.rapidapi.com",
        "X-RapidAPI-Key": "e34cfc2358mshb0d0a32b739f2e0p1fa103jsnf9f3985beab7"
    }

    data_dict = {}
    
    for i in range(1, 21):
        querystring = {"comp":"1","team":{i},"sort":"average","type":"home"}
        response = requests.request("GET", url, headers=headers, params=querystring)
        json_data = json.loads(response.text)
        for x,y in json_data["attendances"].items():
            if x == 'team':
                # if y['name'] in L:
                    team = y['name']
                    data_dict[team] = []
            elif x == 'matches':
                for match in y:
                    if match["attendance"] != 0:
                        data_dict[team].append(match["attendance"])
    
    for x,y in data_dict.items():
        sum = 0
        tot = 0
        for num in y:
            sum += num
            tot += 1
        data_dict[x] = sum / tot
    
    print(data_dict)
    print(len(data_dict))
    return data_dict



# class TestAllMethods(unittest.TestCase):
#     def test_data_grab():
#         data_grab()
#         return




def main():
    prem_data_grab("2021-2022")
    # print(get_teams_by_season("2013-2014"))
    print(getAttendancePrem("2021-2022"))
    return 1





if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)

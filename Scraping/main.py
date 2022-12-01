# Python script to scrape player data
import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads"

response = requests.get(url)
source = response.text
src_soup = BeautifulSoup(source, "html.parser")
players = src_soup.find_all("tr", {"class": "nat-fs-player"})
# player_lst = []
player_number = 0
players_dict = {}

for player in players:
    player_dets = player.find_all("td")
    player_position = player_dets[1].find("a").text
    player_dob = player_dets[2].text
    pdob = player_dob[13:]
    player_dob = pdob[:len(pdob) - 11]
    # print(player_dob)
    dob_split = player_dob.split(" ")
    date = dob_split[0]
    mob = dob_split[1]
    yob = dob_split[2]
    player_caps = player_dets[3].text.strip()
    print(player_caps)
    player_goals = player_dets[4].text.strip()
    print(player_goals)
    club_team_country = player_dets[5].find("img").get("alt")
    player_club = player_dets[5].find_all("a")[1].text
    player_name = player.find("th", {"scope": "row"}).get("data-sort-value")
    if ", " in player_name:
        first_name = player_name.split(", ")[1]
        other_names = player_name.split(", ")[0]
    else:
        first_name = player_name
        other_names = "N/A"
    player_number += 1
    players_dict[player_number] = [first_name, other_names, player_name, player_dob, date,
                                   mob, yob, player_position, player_caps, player_goals, player_club, club_team_country]
    # print("Name: " + player_name + "\nFirst name: " + first_name + "\nOther names: " + other_names + "\nPosition: " + player_position + "\nDOB: " + player_dob +
    #       "\nNational Caps: " + player_caps + "\nNational Goals: " + player_goals + "\nClub: " + player_club + "\nClub Country: " + club_team_country + "\n-------")

# print(player_lst[0])
wc_players_dict = pd.DataFrame.from_dict(players_dict, orient="index", columns=[
                                         "First Name", "Other Names", "Full Name", "DOB", "Day of Birth", "Month of Birth", "Year of Birth", "Position", "International Caps", "International Goals", "Club", "Club Country"])

# print(wc_players_dict.head)
wc_players_dict.to_csv("WorldCup2022Players.csv")

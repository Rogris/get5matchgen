import argparse
import json
import os
from dataclasses import asdict

from tools import Defaultsettings, Matchinfo, Teaminfo, maps


def showteams() -> list:  # shows available teams
    teamfiles = os.path.abspath(os.path.dirname(__file__)) + "\\teams"
    teams = os.listdir(teamfiles)
    teams = [os.path.splitext(x)[0] for x in teams]  # strip extension
    print("Avaliable teams:")
    print(*teams, sep="\n")  # prints 1 team per line
    return teams  # returns the list for future use in other functions


def deleteteam() -> None:  # delete a team
    showteams()
    teamfiles = os.path.abspath(os.path.dirname(__file__)) + "\\teams"
    removeteam = input("Enter name of team to remove: ")
    if removeteam in showteams():
        os.remove(teamfiles + f"\\{removeteam}.json")  # removes team json file
    else:
        print("Invalid team name. Aborting")
        quit()


def addteam() -> None:  # Add a team json file and save it in the teams folder
    try:
        file_path = os.path.abspath(os.path.dirname(__file__))  # Get default file path
        os.mkdir(f"{file_path}/teams")  # Create folder teams
    except FileExistsError:  # If it exists, ignore error
        pass
    teamname = input("Enter team name: ")
    tag = input("Enter team tag: ")
    player = []  # Initialize empty player list
    data = Teaminfo(name=teamname, tag=tag, players=player)  # get relevant data
    filename = teamname + ".json"
    playerno = 1
    try:
        with open("teams\\" + filename, "x") as teamjson:
            for _ in range(5):  # Add first five players
                steamid = input(f"Enter SteamID for player {playerno}: ")
                player.append(steamid)
                playerno = playerno + 1
            else:  # Add sub if required
                subcheck = input("Type 'yes' if you wish to add a sub: ")
                if "yes" in subcheck.lower():  # checks if yes was entered
                    steamid = input("Enter SteamID for substitute: ")
                    player.append(steamid)
                else:
                    pass
            teamjson.write(json.dumps(asdict(data), indent=4))  # Writes json data
    except FileExistsError:
        print("Team already exists. Aborting")
        quit()


def writematchfile():
    specs = {
        "players": input("Insert spectator SteamID: ")
    }  # players that can join GOTV
    showteams()
    teamno = 1
    filename = str(Defaultsettings.matchid) + ".json"
    data1 = asdict(Defaultsettings(spectators=specs))
    teamdata = []
    for _ in range(2):  # To select two teams
        selection = input(f"Enter name of team number {teamno}: ")
        while selection not in showteams():
            print("Team name does not exist. Aborting")
            quit()
        print(
            f"Selected as team {teamno}: {selection}"
        )  # prints which team was selected as which
        teamno = teamno + 1
        teamfile = "teams\\" + selection + ".json"  # get the team file
        with open(teamfile, "r") as teamjson:
            teamdata.append(json.loads(teamjson.read()))  # append the data to list
    teamdata1 = teamdata[0]
    teamdata2 = teamdata[1]
    defhostname = {"hostname": f"{teamdata1['name']} vs {teamdata2['name']}"}
    data2 = asdict(
        Matchinfo(
            maplist=maps,
            team1=dict(teamdata1),
            team2=dict(teamdata2),
            cvars=defhostname,
        )
    )  # Sets map, teams and hostname parameters
    data = [data1, data2]  # create list from both two separate dicts
    with open(filename, "x") as matchjson:
        matchjson.write(json.dumps(data, indent=4))  # create json from list of dicts
    print(f"Match file {filename} generated")


def main(args: dict) -> None:
    if args["create"] is True:
        writematchfile()
    elif args["add"] is True:
        addteam()
    elif args["show"] is True:
        showteams()
    elif args["delete"] is True:
        deleteteam()
    else:
        print("Something went wrong. Aborting")
        quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Get5 match generator",
        description="Creates a match file for get5 without manual editing",
        epilog="Enjoy",
    )
    parser.add_argument(
        "-c", "--create", help="Create a match file", action="store_true"
    )
    parser.add_argument("-a", "--add", help="Add a team", action="store_true")
    parser.add_argument("-s", "--show", help="Show created teams", action="store_true")
    parser.add_argument("-d", "--delete", help="Delete a team", action="store_true")
    args = vars(parser.parse_args())
    main(args)

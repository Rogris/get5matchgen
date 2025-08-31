import json
from argparse import ArgumentParser
from subprocess import run

MAPS=[
    "de_mirage",
    "de_dust2",
    "de_inferno",
    "de_train",
    "de_nuke",
    "de_ancient",
    "de_overpass"
    ]

class Match():
    def __init__(self):
        pass


    def getmatchid(self):
        with open("cfg/data", "r") as f:
            return int(f.read().strip())
        

    def getteams(self, team1, team2):
        with open(f"teams/{team1}.json") as f:
            data=f.read()
            team1=json.loads(data)
        with open(f"teams/{team2}.json") as f:
            data=f.read()
            team2=json.loads(data)
        return team1, team2
    

    def getspectators(self, specid):
        return {"players": {f"{specid}": "EPICENTER 2025 Observer"}}
    

    def getformat(self, setformat):
        return int(setformat)
    
    
    def generatematch(self, team1, team2, nummaps, spec):
        print(f"Generating match: {team1} vs {team2}")
        id=self.getmatchid()
        teams=self.getteams(team1=team1, team2=team2)
        nummaps=self.getformat(nummaps)
        spectators=self.getspectators(spec)
        matchfilename=f"matches/match_{id}_{team1}_{team2}.json"
        with open(matchfilename, "w+") as f:
            matchdata={
                "matchid": id,
                "team1": teams[0],
                "team2": teams[1],
                "num_maps": nummaps,
                "maplist": MAPS,
                "spectators": spectators,
                "clinch_series": "true",
                "players_per_team": 5,
                "cvars": {
                    "hostname": f"EPICENTER Lan 2025: {team1} vs {team2}"
                }
            }
            f.write(json.dumps(matchdata, indent=4))
        with open("cfg/data", "w") as f:
            id += 1
            f.write(str(id))
        print(matchfilename)
        run(["bash", "transferfile.sh", f"{matchfilename}"])
        print("File copied to server")

if __name__ == "__main__":
    parser=ArgumentParser(
        prog="MatchZy team generator",
        description="Generater MatchZy match configs"
    )
    parser.add_argument("team1", help="Team 1 name")
    parser.add_argument("team2", help="Team 2 name")
    parser.add_argument("--nummaps, -n", dest="nummaps", help="Number of maps. Default is 1", default=1, required=False)
    parser.add_argument("--spectator, -s", dest="spectator", help="Spectator. Only set if needed", default="76561198015560450", required=False)
    args=parser.parse_args()
    Match().generatematch(args.team1, args.team2, args.nummaps, args.spectator)


import json
from dataclasses import asdict, dataclass, field, is_dataclass
from random import randint

maps = [
    "de_anubis",
    "de_inferno",
    "de_ancient",
    "de_mirage",
    "de_nuke",
    "de_overpass",
    "de_vertigo",
]


class JsonDataclass(json.JSONEncoder):
    def default(self, o):
        if is_dataclass(o):
            return asdict(o)
        return super().default(o)


@dataclass
class Defaultsettings:
    """Sets basic match information. You can override the number of maps, first veto and knife round."""

    matchid: int = field(
        default=randint(10000000, 999999999), init=False
    )  # generates 8 digit match ID
    num_maps: int = field(default=3)  # number of maps to play
    players_per_team: int = field(default=5, init=False)  # number of players per team
    coaches_per_team: int = field(default=1, init=False)  # number of coaches per team
    min_players_to_ready: int = field(
        default=8, init=False
    )  # minimum number of players to enabley !forceready
    min_spectators_to_ready: int = field(
        default=0, init=False
    )  # minimum number of spectators to ready
    skip_veto: bool = field(default=False)  # skip map veto if True
    veto_first: str = field(default="team1")  # which team vetoes first (1=CT, 2=T)
    side_type: str = field(
        default="standard"
    )  # standard is valve BO3, always/never knife for knife rounds


# @dataclass
# class Matchinfo:
#     """arrays of teams, spectators, maps"""

#     spectators: dict = field
#     maplist: list = field(default=maps)
#     team1: dict = field
#     team2: dict = field
#     cvars: dict = field(default={"hostname": f"{team1} vs {team2}"})


@dataclass
class Teaminfo:
    pass


@dataclass
class Playerinfo:
    pass


if __name__ == "__main__":
    print("You're running the wrong file. Aborting")
    quit()

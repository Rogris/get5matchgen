import json
from dataclasses import asdict

from tools import Defaultsettings


def writefile():
    filename = str(Defaultsettings.matchid) + ".json"
    data = Defaultsettings()
    with open(filename, "x") as matchjson:
        matchjson.write(json.dumps(asdict(data), indent=4))


def main() -> None:
    writefile()


if __name__ == "__main__":
    main()

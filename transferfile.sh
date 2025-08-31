#!/bin/bash
echo "Copying $1 to server"
scp $1 cs2server1@10.100.0.15:~/serverfiles/game/csgo
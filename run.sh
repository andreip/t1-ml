#!/bin/bash

# Copyright (C) 2014 Tudor Berariu
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

if [[ $# -eq 2 ]]; then
  PORT_SERVER=$1
  GAMES_NO=$2
elif [[ $# -eq 1 ]]; then
  PORT_SERVER=$1
  GAMES_NO=200
else
  PORT_SERVER=35000
  GAMES_NO=200
fi

echo $GAMES_NO

get_free_port()
{
    Port=35000
    while netstat -atwn | grep "^.*:${Port}.*:\*\s*LISTEN\s*$"
    do
    Port=$(( ${Port} + 1 ))
    done
    eval "$1='${Port}'"
}

launch_round()
{
    eval "./bricks_server --port $1 --height $2 --length $3 --output-file $4 --games-no=$GAMES_NO &"
    sleep 1
    eval "./brickmaker --port $1 --in-file $5 &"
    eval "./bricklayer.py $1 &"
}

make -f Makefile.compile_d build
launch_round $PORT_SERVER 4 4 score1 distributions/dist1

#launch_round $PORT_SERVER 8 5 score2 distributions/dist2

#launch_round $PORT_SERVER 8 6 score3 distributions/dist3

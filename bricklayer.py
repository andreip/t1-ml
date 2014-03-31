#!/usr/bin/env python
# -*- coding: utf-8 -*-

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


import socket
from bricklayer_sarsa import BricklayerSarsa

class BrickLayer:
    """Demo BrickLayer
    """

    def __init__(self, port=9923):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((socket.gethostname(), port))
        self.mysend("BRICKLAYER\n")
        self.buffer = b''
        firstLine = self.myreceive()
        [height, length] = map(lambda x: int(x), firstLine.split(','))
        self.sarsa = BricklayerSarsa(height, length)

    def loop(self):
        line = self.myreceive()
        action = self.sarsa.get_action(line)
        while line:
            if "GAME OVER" not in line:
                (rot, offset) = action
                msg = str(rot) + "," + str(offset) + "\n"
                self.mysend(msg)

            # Get next action and its reward for s -> s'.
            next_line = self.myreceive()

            # Update utilities and update (s,a) <- (s', a').
            if next_line and "GAME OVER" not in next_line:
                next_action = self.sarsa.get_action(next_line)
                self.sarsa.update_utilities(line, action, next_line, next_action)
                action = next_action
            line = next_line

    def mysend(self, msg):
        totalsent = 0
        while totalsent < len(msg):
            sent = self.socket.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("S-A BUSIT SOCKETUL")
            totalsent = totalsent + sent

    def myreceive(self):
        while '\n' not in self.buffer:
            chunk = self.socket.recv(1024)
            if chunk == b'':
                return False
            self.buffer = self.buffer + chunk
        line = self.buffer[0:self.buffer.index('\n')]
        self.buffer = self.buffer[self.buffer.index('\n')+1:]
        return line

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        port = int(sys.argv[1])
    else:
        port = 9923
    bricklayer = BrickLayer(port)
    bricklayer.loop()
    bricklayer.socket.close()
    print 'bye (bricklayer)'

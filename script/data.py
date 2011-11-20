##-----------------------------------------------------------------------------
##This source file is part of Con Sonar!
##For the latest info, see http://exequor.com/
##
##Copyright (c) 2011 Exequor Studios Inc.
##
##Permission is hereby granted, free of charge, to any person obtaining a copy
##of this software and associated documentation files (the "Software"), to deal
##in the Software without restriction, including without limitation the rights
##to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
##copies of the Software, and to permit persons to whom the Software is
##furnished to do so, subject to the following conditions:
##
##The above copyright notice and this permission notice shall be included in
##all copies or substantial portions of the Software.
##
##THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
##IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
##FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
##AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
##LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
##OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
##THE SOFTWARE.
##-----------------------------------------------------------------------------

attacker = ["destroyer", "carrier", "pt", "frigate", "sub", "transport"]
colours = ["b","g","o","p","r","y"]
values = ["m1","p2","m3","p4","m5","p6"]
avalues = [-1, +2, -3, +4, -5, +6]
dbFleetCards = []
dbTorpedoCards = []

start_attacker_index = 2
for c in colours:
    attacker_index = start_attacker_index
    for t in range(0,3):
        attacker_index = attacker_index%6
        dbTorpedoCard = [c, t, attacker[attacker_index]]
        dbTorpedoCards += [dbTorpedoCard]
        attacker_index -= 1
    start_attacker_index += 1

print dbTorpedoCards

#Rules
# Regular red torpedo should be usable when you just +2d a red sub
# Advanced red torpedo should be usable when you just -1d a red sub
# Experimental red torpedo should be usable when you just -3d a red sub


start_attacker_index = 0
for c in colours:
    attacker_index = start_attacker_index-1
    lead_index = start_attacker_index
    for t in range(0,6):
        attacker_index = attacker_index%6
        lead_index = lead_index%6
        print c,t,lead_index,attacker_index
        dbFleetCard = [c,values[t],attacker[attacker_index],attacker[lead_index],avalues[t]]
        dbFleetCards += [dbFleetCard]
        lead_index += 1
        attacker_index += 1
    start_attacker_index += 1

print dbFleetCards

        
        
    



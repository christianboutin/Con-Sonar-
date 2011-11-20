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

import time
import data
import random
import datetime

reload(data)


verbose = False
currentLog = None

game = None

notes = {}

dotspacer = 0

def log(s):
    global dotspacer
    
    if (verbose):
        print s#+"\n"
    else:
        dotspacer +=1
        dotspacer = dotspacer %100
        if (dotspacer == 0):
            print ".",

    if (currentLog):
        currentLog.write(str(s)+"\n")

def note(n):
    global notes
    if (notes.has_key(n)):
        notes[n] += 1
    else:
        notes[n] = 1
    
    

class Position:
    index=None
    
    def __init__(self, index):
        self.index = index

    def __repr__(self):
        rv = str(self.index);
        return rv

class Sub:
    colour=None
    pos=None

    def __init__(self, colour, mFiringSolution):
        self.colour = colour
        self.pos = Position(mFiringSolution)

    def __repr__(self):
        rv = "Sub:"+self.colour+"["+str(self.pos)+"]";
        return rv
        

class Game:
    subs = []
    players = []
    fleetdiscard = []
    fleetdraw = []
    torpdraw = []
    torp = []
    turn = 0

    def __init__(self):
        self.subs = []
        self.players = []
        self.fleetdiscard = []
        self.fleetdraw = []
        self.torpdraw = []
        self.torp = []
        self.turn = 0

        self.torpdraw = data.dbTorpedoCards[:]
        random.shuffle(self.torpdraw)

        self.fleetdraw = data.dbFleetCards[:]
        random.shuffle(self.fleetdraw)
##        log "---"
##        log self.torpdraw
##        log "---"
##        log self.fleetdraw
##        print "---"

        for i in data.colours:
            if (i == "o"):
                p = RandomPlayer(i, self);
##            elif (i == "p"):
##                p = WeightedPlayer(i, self);
            else:
                p = DefaultPlayer(i, self);

            for j in range(0,3):
                p.addCard(self.fleetdraw.pop())

            self.players += [p]

            sub = Sub(i, 1)
            self.subs +=  [sub]
            sub = Sub(i, 2)
            self.subs +=  [sub]
#        print self.subs
            

        for j in range(0,3):
            self.torp += [self.torpdraw.pop()]
#        print self.torp
                

    def isGameOver(self):
        if (len(self.torpdraw) == 0 and len(self.torp) < 4):
            note("GameOverNoTorp");
            return True
        if (len(self.subs) == 0):
            note("GameOverNoSub");
            return True
        return False

    def showBoard(self):
        strlog = "BOARD:"
        for index in range(1,9):
            strlog+="["+str(index)+":"
            for i in self.subs:
                if (i.pos.index == index):
                    strlog+=i.colour
            strlog+="]"
        log (strlog)                        

    def showTorp(self):
        log("Opened Torpedo Cards : "+str(self.torp))
        
    
    def showPlayers(self):
        for i in self.players:
            log(i)

    def play(self):
        gameover = False
        while (not gameover):
            self.turn += 1
            log("----------------------------------------------- TURN "+str(self.turn))
            self.showBoard()
            self.showTorp()
            self.showPlayers()

            for j in self.players:
                j.play()
                if (len(j.hand) == 3):
                    raise("Player still has a full hand")
                    
                while (len(j.hand) < 3):
                    self.giveCardToPlayer(j)
                if (self.isGameOver()):
                    gameover = True
                    break

        log("----------------------------------------------- GAME OVER IN "+str(self.turn)+" TURNS")
        note("Over in "+str(self.turn))
        self.showPlayers()
        sortedPlayers = sorted(self.players, key=lambda p:p.getScore(), reverse=True)
        if (sortedPlayers[0].getScore() == sortedPlayers[1].getScore()):
            return "draw"
        return sortedPlayers[0].colour
                

    def giveCardToPlayer(self, player):
        if (len(self.fleetdraw)==0):
            while (len(self.fleetdiscard) > 0):
                self.fleetdraw += [self.fleetdiscard.pop()]
            random.shuffle(self.fleetdraw)
            
        player.hand+=[self.fleetdraw.pop()]
        
    def playCard(self, card,sub):## Must play a card and a sub
        if (card[0] != sub.colour and self.getSubs(card[0])):
            raise ("Playing a card on a sub of a different colour")
        
        self.fleetdiscard+= [card]

        #validate the card is the right colour OR no remaining sub

        if (card[1] == "p2"):
            diff = 2
        elif (card[1] == "m1"):
            diff = -1
        elif (card[1] == "m3"):
            diff = -3
        elif (card[1] == "p4"):
            diff = 4
        elif (card[1] == "m5"):
            diff = -5
        elif (card[1] == "p6"):
            diff = +6
            
        #print str(sub.pos.index)+" >",
        sub.pos.index += diff
        if (sub.pos.index < 1):
            sub.pos.index = 1
        elif (sub.pos.index > 8):
            sub.pos.index = 8
        #print str(sub.pos.index)
            

    def rollToDestroy(self, card, sub):
        for i in range(card[1]):
            result = random.randrange(0,8)+1
            log("Dice Roll :"+str(result))
            if (result < sub.pos.index):
                return True
        return False

    def playTorp(self, player, card, sub): ## Torp should attempt to destroy sub
        #validate the card is the right colour OR no remaining sub
        rv = False
        for h in self.torp:
            if (h == card):
                if (self.rollToDestroy(card, sub)):
                    note("Sub Destroyed")
                    player.subs+=[sub]
                    self.subs.remove(sub)
                    rv = True
                else:
                    player.miss +=1
                    
                self.torp.remove(h)

        while (len(self.torp) < 3):
            if (len(self.torpdraw) == 0):
                break
            else:
                self.torp += [self.torpdraw.pop()]
        return rv

    def getSubs(self, colour=None):
        rv = []
        if (colour == None):
            return self.subs
        else:
            for h in self.subs:
                if (h.colour == colour):
                    rv += [h]

        return rv;

    def getTopSub(self, colour=None):
        targets = self.getSubs(colour)
        if (len(targets) == 0):
            targets = self.getSubs(None)

        rv = sorted(targets, key=lambda sub:sub.pos.index, reverse=True)[0]
        return rv
        
            
class Player:
    colour = None
    hand=[]
    subs=[]
    game = None
    miss = 0

    def __init__(self, colour,game):
        self.colour = colour
        self.hand=[]
        self.subs = []
        self.game = game

    def getScore(self):
        return (len(self.subs))+len(game.getSubs(self.colour))-self.miss
    
    def addCard(self, card):
        self.hand += [card]

    def __repr__(self):
        rv="Player : "+self.colour+" sc:"+str(self.getScore())+" -> "+str(self.hand)+" w/ +"+str(self.subs)
        return rv

    def randomPlay(self):
        strlog = "RNDPlr "+self.colour+" plays "
        # plays a random card
        random.shuffle(self.hand)

        targetSub = None
        playing = self.hand.pop()
        targets = self.game.getSubs(playing[0])
        if (len(targets) > 0):
            targetSub = targets[0]
        else:  # No target sub of wanted colour, plays on another sub
            targets = self.game.getSubs()
            random.shuffle(targets)
            targetSub = targets[0]

        strlog += playing[0]+playing[1] + " on "+str(targetSub)
        
        self.game.playCard(playing,targetSub)

        for h in self.game.torp:
            if (h[0] != self.colour):
                targets = self.game.getSubs(h[0])
                if (len(targets) == 0):
                    targets = self.game.getSubs()
                if (len(targets) == 0):
                    break
                
                target = targets[0]
                strlog+= " then attacks "+str(target)+" with "+h[0]+str(h[1]+1)
                if (self.game.playTorp(self,h, target)):
                    strlog+=" HIT!"
                break
                    
                        
        log (strlog)

    def getRandomTarget(self, colour):
        possibletargets = self.game.getSubs(colour);
        if not possibletargets:
            possibletargets = self.game.getSubs();
            
        random.shuffle(possibletargets)
        return possibletargets[0]

class RandomPlayer(Player):
       
    def play(self):
        self.randomPlay()



class DefaultPlayer(Player):

    def playCards(self):
        pass
       
    def play(self):
        targets = self.game.getSubs()
        sortedTargets = sorted(targets, key=lambda sub:sub.pos.index, reverse=True)
        sortedTorpCards = sorted(self.game.torp, key=lambda c:c[1], reverse = True)
        sortedFleetCards = sorted(self.hand, key=lambda v:v[4], reverse = True)

        for t in sortedTargets:
            #is there a torpedo card for it?
            for c in sortedTorpCards:
                if (c[0] == t.colour):
                    #do I have a card that can lead to THAT card
                    for f in sortedFleetCards:
                        if (f[3] == c[2] and f[0] != self.colour):
                            fleetTarget = self.getRandomTarget(f[0])
                            
                            strlog = "DEFPlr "+self.colour+" plays "
                            playing = self.hand.pop(self.hand.index(f))
                            strlog += playing[0]+playing[1] + " on "+str(t)
                            
                            self.game.playCard(playing,fleetTarget)
                            strlog+= " then attacks "+str(t)+" with "+c[0]+str(c[1]+1)

                            if (self.game.playTorp(self,c, t)):
                                strlog+=" HIT!"
                            log (strlog)
                            return
        note("DefaultPlayerRevertsToRandom");
        self.randomPlay()
                            

class FleetCard:
    @staticmethod
    def getColour(card):
        return card[0]
    
    @staticmethod
    def getValue(card):
        return card[4]

    @staticmethod
    def getAttacker(card):
        return card[2]

    @staticmethod
    def getLead(card):
        return card[3]
    

class TorpCard:
    @staticmethod
    def getColour(card):
        return card[0]

    @staticmethod
    def getStrength(card):
        return card[1]

    @staticmethod
    def getAttacker(card):
        return card[2]

class WeightedPlayer(Player):

    def playCards(self):
        pass

    def getCardWeight(self, card):
        # score modifier is the base weight.
        # If the card is of the player's colour, it is reversed
        weight = 0

        if (FleetCard.getColour(card) == self.colour):
            weight -= FleetCard.getValue(card)*5
        else:
            weight += FleetCard.getValue(card)*5
            
        # If a card leads to a torpedo of an opposing colour, the position of that sub on the track is added to the weight

        tw = 0
        for h in self.game.torp:
            if (TorpCard.getAttacker(h) == FleetCard.getLead(card)):
                ntw = 3 + TorpCard.getStrength(h) + self.game.getTopSub(TorpCard.getColour(h)).pos.index
                tw = max(tw, ntw)

        weight += tw
        return weight

    def getTorpWeight(self, torp):
        rv = 0
        rv += TorpCard.getStrength(torp)
        rv += self.game.getTopSub(TorpCard.getColour(torp)).pos.index
        return rv
       
    def play(self):
        sortedTorpCards = sorted(self.game.torp, key=lambda v:self.getTorpWeight(v), reverse = True)
        sortedFleetCards = sorted(self.hand, key=lambda v:self.getCardWeight(v), reverse = True)

        
        choice = sortedFleetCards[0]
        playing = self.hand.pop(self.hand.index(choice))
        #print playing
        if (playing != choice):
            raise ("Ahem")

        t = self.game.getTopSub(FleetCard.getColour(playing))

        self.game.playCard(playing,t)

        strlog = "WGTPlr "+self.colour+" plays "
        strlog += playing[0]+playing[1] + " on "+str(t)


        for i in sortedTorpCards:
            if (TorpCard.getColour(i) != self.colour):
                if (TorpCard.getAttacker(i) == FleetCard.getLead(playing)):
                    target = self.game.getTopSub(TorpCard.getColour(i))
                    if (target.pos.index < 5):
                        strlog+= " then attacks "+str(t)+" with "+i[0]+str(i[1]+1)
                        if (self.game.playTorp(self,i,target)):
                            strlog+=" HIT!"
                        break
        log(strlog)
        
results = {"r":0,"g":0,"b":0,"y":0,"o":0,"p":0,"draw":0}
        
for i in range(0,10000):
    currentLog = file("simlog/"+datetime.datetime.now().strftime("%Y%m%d_%H%M%S_")+str(datetime.datetime.now().time().microsecond)+".txt","wt+")
    game = Game()
    results[game.play()]+=1
    currentLog.close()
    print i,

print ""
print results
print notes

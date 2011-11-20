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

##Requires PIL: http://www.pythonware.com/products/pil/

import Image as PIL
import ImageEnhance as PILEnhance
import ImageChops as PILChops
import ImageDraw as PILImageDraw
import ImageFont as PILImageFont
import os
import math
import shutil
import xml.dom.minidom
import data
import random

reload(data)

def BoxFromXml(tag):
    doc = xml.dom.minidom.parse("../source-media/cards/cards_coord.xml")
    for node in doc.getElementsByTagName("coord"):
        if (node.getAttribute("id") == tag):
            x = int(node.getAttribute("x"))
            y = int(node.getAttribute("y"))
            w = int(node.getAttribute("w"))
            h = int(node.getAttribute("h"))
            return (x,y,x+w,y+h)
    print "TAG:"+tag;
    raise(Exception)

def BlitImage(imgname, canvas):
    img = PIL.open("../source-media/cards/"+imgname)
    box = BoxFromXml(imgname)
    canvas.paste(img, box, img)

def BlitMirror(imgname, canvas):
    img = PIL.open("../source-media/cards/"+imgname).rotate(180)
    box = BoxFromXml(imgname)
    newbox = (825-box[2],1125-box[3],825-box[0],1125-box[1])
    canvas.paste(img, newbox, img)

ICON_WIDTH = 147
ARROW_WIDTH = 64
    
def BlitLead(imgname, canvas):
    img = PIL.open("../source-media/cards/"+imgname)
    box = BoxFromXml(imgname)
    newbox = (box[0]+ICON_WIDTH+ARROW_WIDTH,box[1],box[2]+ICON_WIDTH+ARROW_WIDTH,box[3])
    canvas.paste(img, newbox, img)

def BlitLeadMirror(imgname, canvas):
    img = PIL.open("../source-media/cards/"+imgname).rotate(180)
    box = BoxFromXml(imgname)
    newbox = (box[0]+ICON_WIDTH+ARROW_WIDTH,box[1],box[2]+ICON_WIDTH+ARROW_WIDTH,box[3])
    newnewbox = (825-newbox[2],1125-newbox[3],825-newbox[0],1125-newbox[1])
    canvas.paste(img, newnewbox, img)
    
for i in data.dbFleetCards:
    print i
    card = PIL.new("RGBA", (825,1125))
    print i[1]
    bkg = PIL.open("../source-media/cards/card_"+i[1]+".png")
    card.paste(bkg)
    card = card.convert("RGB")
    
    for j in ["borders_"+i[0]+".png",i[1]+".png",i[1]+"e.png","icon_"+i[2]+".png","icon_arrow.png"]:
        BlitImage(j,card)
        BlitMirror(j,card)

    BlitLead("icon_"+i[3]+".png", card)
    BlitLeadMirror("icon_"+i[3]+".png", card)

    outname = "../prod/fleet_"+i[0]+"_"+i[1]+".png"
    card.save(outname)
    print "."
    

for i in data.dbTorpedoCards:
    print i
    card = PIL.new("RGBA", (825,1125))
    bkg = PIL.open("../source-media/cards/card_t"+str(i[1]+1)+".png")
    card.paste(bkg)
    card = card.convert("RGB")
    
    for j in ["borders_"+i[0]+".png","icon_"+i[2]+".png","t"+str(i[1])+"x.png","t"+str(i[1])+".png"]:
        BlitImage(j,card)
        BlitMirror(j,card)
##
##    BlitLead("icon_"+i[3]+".png", card)
##    BlitLeadMirror("icon_"+i[3]+".png", card)

    outname = "../prod/torp_"+i[0]+"_"+str(i[1])+".png"
    card.save(outname)
    print "."
    

    

    


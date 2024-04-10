# Imports PIL module
from PIL import Image
import random
import numpy as np
import math
from perlin_noise import PerlinNoise

noise = PerlinNoise(octaves=10, seed=1)







grassColourOne=(52,140,49)#(0,51,20)
grassColourTwo=(0,900,0)#(229,372,150)#(154,247,100)#(11, 102, 35)

rockColourOne=(100,100,100)#(73,49,37)#(79,57,48)#(152, 154, 152)
rockColourTwo=(255,255,255)#(60,40,13)
Gradientfactor=1

im = Image.new(mode="RGB", size=(600, 600),color = (40, 40, 40))#heightmap
texturemap=Image.new(mode="RGB", size=(600, 600))

# noise1 = PerlinNoise(octaves=3)
# noise2 = PerlinNoise(octaves=6)
# noise3 = PerlinNoise(octaves=12)
# noise4 = PerlinNoise(octaves=24)

# xpix, ypix = texturemap.width, texturemap.height
# pic = []
# for i in range(xpix):
#     for j in range(ypix):
#         noise_val = noise1([i/xpix, j/ypix])
#         noise_val += 0.5 * noise2([i/xpix, j/ypix])
#         noise_val += 0.25 * noise3([i/xpix, j/ypix])
#         noise_val += 0.125 * noise4([i/xpix, j/ypix])
#         noise_val *=255
#         noise_val=int(noise_val)
#         texturemap.putpixel((i,j),(noise_val,noise_val,noise_val))
# texturemap.show()

def getGrassColour():
    # judge=random.random()
    # if(judge<0.1):
    #     return grassColourOne
    return grassColourTwo

def getRockColour():
    # judge=random.random()
    # if(judge<0.05):
    #     return rockColourTwo
    return rockColourOne

def createBasicTerrainFlow():
    hillbrush = Image.open('./threejsFold/Heightmaps/softDotGradientThree.png').convert("RGB")
    hillbrush = hillbrush.resize((int(hillbrush.width/1), int(hillbrush.height/1)), Image.Resampling.LANCZOS)
    clampRGB=hillbrush.getpixel((int(hillbrush.width/2),int(hillbrush.height/2)))
    brightnessclampRGB=(0.2126*clampRGB[0] + 0.7152*clampRGB[1]  + 0.0722*clampRGB[2] )
    scaleFactor=1
    created=0
    riverpoints= pointsOnLineBetweenTwoPoints(riverStart,riverEnd)
    while created<20:#im.size[0]*im.size[1]/5) ):
        adjustX=random.randint(0, im.size[0]-1)
        adjustY=random.randint(0, im.size[1]-1)
        cornersOfBrush=getCornersOfAdjustedImage((adjustX,adjustY),hillbrush)
        print(cornersOfBrush)
        within=None
        for RP in riverpoints:
            PPX=RP[0]
            PPY=RP[1]
            topLeftCorner=(PPX-32,PPY-32)
            topRightCorner=(PPX+32,PPY-32)
            BottomLeftCorner=(PPX-32,PPY+32)
            BottomRightCorner=(PPX+32,PPY+32)
            corners=[topLeftCorner,topRightCorner,BottomLeftCorner,BottomRightCorner]
            for corn in corners:
                within=DetectIfPointWithinBox(cornersOfBrush,corn)
                if(within==True):
                    break
            if(within==True):
                break
        if(within==False):
            created+=1

            for yy in range( hillbrush.height):
                for xx in range( hillbrush.width):
                    #im.size[0]*im.size[1]/5) ):
                    rr, gg, bb = hillbrush.getpixel((xx, yy))
                    # print(r,g,b)
                    overEqZx=(adjustX -int(hillbrush.width/2)+ xx)>=0
                    overEqZy=(adjustY-int(hillbrush.height/2) + yy)>=0
                    underEqZmaxX=(adjustX-int(hillbrush.width/2) + xx)<=im.size[0]-1
                    underEqZmaxY=(adjustY-int(hillbrush.height/2) + yy)<=im.size[1]-1

                    if((rr,gg,bb)>=(1,1,1) and overEqZx and overEqZy and underEqZmaxX and underEqZmaxY):
                        R,G,B=im.getpixel((adjustX -int(hillbrush.width/2)+ xx, adjustY-int(hillbrush.height/2) + yy))
                        # print(curCol)
                        brightnessOne=(0.2126*R + 0.7152*G + 0.0722*B)
                        brightnessTwo=(0.2126*rr + 0.7152*gg + 0.0722*bb)
                        # if(brightnessOne<=brightnessTwo):
                            # im.putpixel((adjustX -int(hillbrush.width/2)+ xx, adjustY-int(hillbrush.height/2) + yy), (rr,gg,bb))
                        factor=2
                        added=(int((rr+R)/factor),int((gg+G)/factor),int((bb+B)/factor))
                        subtracted=((R-int(rr/6),G-int(gg/6),B-int(bb/6)))
                        brightnessAdded=(0.2126*added[0] + 0.7152*added[1]  + 0.0722*added[2] )
                        brightnesssubbed=(0.2126*subtracted[0] + 0.7152*subtracted[1]  + 0.0722*subtracted[2] )
                        # im.putpixel((adjustX -int(hillbrush.width/2)+ xx, adjustY-int(hillbrush.height/2) + yy), added)
                        if(brightnessTwo>brightnessOne):
                            im.putpixel((adjustX -int(hillbrush.width/2)+ xx, adjustY-int(hillbrush.height/2) + yy), added)
                        # else:
                        #     im.putpixel((adjustX -int(hillbrush.width/2)+ xx, adjustY-int(hillbrush.height/2) + yy), (40,40,40))#clampRGB

                        # if(brightnesssubbed<brightnessOne):#brightnesssubbed<brightnessclampRGB):
                        #     im.putpixel((adjustX -int(hillbrush.width/2)+ xx, adjustY-int(hillbrush.height/2) + yy), subtracted)
                        # else:
                        #     im.putpixel((adjustX -int(hillbrush.width/2)+ xx, adjustY-int(hillbrush.height/2) + yy), clampRGB)

riverStart=(0,300)
riverEnd=(600,300) 

TownCenterCoords=[(290,290),(290,310),(310,290),(310,310)]#top left, bottom left, top right, bottom right

obstacleBounds=[]
obstacles=[]
def DrawImageOnCenter(center,ImageUsed,scale,rotation):
    ImageUsed=ImageUsed.resize((int(ImageUsed.width/scale), int(ImageUsed.height/scale)), Image.Resampling.LANCZOS)
    ImageUsed=ImageUsed.rotate(rotation)
    adjustX=center[0]
    adjustY=center[1]
    for yy in range( ImageUsed.height):
        for xx in range( ImageUsed.width):
            #im.size[0]*im.size[1]/5) ):
            rr, gg, bb = ImageUsed.getpixel((xx, yy))
            # print(r,g,b)
            
            overEqZx=(adjustX -int(ImageUsed.width/2)+ xx)>=0
            overEqZy=(adjustY-int(ImageUsed.height/2) + yy)>=0
            underEqZmaxX=(adjustX-int(ImageUsed.width/2) + xx)<=im.size[0]-1
            underEqZmaxY=(adjustY-int(ImageUsed.height/2) + yy)<=im.size[1]-1

            if((rr,gg,bb)>=(1,1,1) and overEqZx and overEqZy and underEqZmaxX and underEqZmaxY):
                R,G,B=im.getpixel((adjustX -int(ImageUsed.width/2)+ xx, adjustY-int(ImageUsed.height/2) + yy))
                # # print(curCol)
                brightnessCanvas=(0.2126*R + 0.7152*G + 0.0722*B)
                brightnessImageUsed=(0.2126*rr + 0.7152*gg + 0.0722*bb)
                if(brightnessCanvas<brightnessImageUsed):#so there will always be some kind of rockcolour now 
                    im.putpixel((adjustX -int(ImageUsed.width/2)+ xx, adjustY-int(ImageUsed.height/2) + yy), (rr,gg,bb))
                    # R,G,B=im.getpixel((adjustX -int(ImageUsed.width/2)+ xx, adjustY-int(ImageUsed.height/2) + yy))
                    # brightnessCanvas=(0.2126*R + 0.7152*G + 0.0722*B)

                    # ratio=(brightnessCanvas/brightnessImageUsed)*1 #so on the edge its basically 0, aproaching and after ratio becomes 1, more rock colour
                    # print("RATIO",ratio)
                    # NCR=int(grassColour[0]*ratio+rockColour[0]*(1-ratio))
                    # NCG=int(grassColour[1]*ratio+rockColour[1]*(1-ratio))
                    # NCB=int(grassColour[2]*ratio+rockColour[2]*(1-ratio))
                    # newColour=(NCR,NCG,NCB)
                    # texturemap.putpixel((adjustX -int(ImageUsed.width/2)+ xx, adjustY-int(ImageUsed.height/2) + yy), newColour)
                    # if(ratio>1):
                    #     NCR=int(grassColour[0]*(1-ratio)+rockColour[0]*ratio)
                    #     NCG=int(grassColour[1]*(1-ratio)+rockColour[1]*ratio)
                    #     NCB=int(grassColour[2]*(1-ratio)+rockColour[2]*ratio)
                    #     newColour=(NCR,NCG,NCB)
                    #     texturemap.putpixel((adjustX -int(ImageUsed.width/2)+ xx, adjustY-int(ImageUsed.height/2) + yy), newColour)
                    # else:
                    #     texturemap.putpixel((adjustX -int(ImageUsed.width/2)+ xx, adjustY-int(ImageUsed.height/2) + yy), rockColour)



                
                # if((rr,gg,bb)>(R,G,B)):
                #     im.putpixel((adjustX -int(ImageUsed.width/2)+ xx, adjustY-int(ImageUsed.height/2) + yy), (rr,gg,bb))
    return 0

def getCornersOfAdjustedImage(center,ImageUsed):
    adjustX=center[0]
    adjustY=center[1]
    topLeftCorner=(adjustX-int(ImageUsed.width/2),adjustY-int(ImageUsed.height/2))
    topRightCorner=(adjustX+int(ImageUsed.width/2),adjustY-int(ImageUsed.height/2))
    BottomLeftCorner=(adjustX-int(ImageUsed.width/2),adjustY+int(ImageUsed.height/2))
    BottomRightCorner=(adjustX+int(ImageUsed.width/2),adjustY+int(ImageUsed.height/2))

    return [topLeftCorner,topRightCorner,BottomLeftCorner,BottomRightCorner]

#create the spawn location, a square that is centered on canvas (im) +- 0.1* width or height of canvas
#all other obstacles spawn  centered at the edge +- 0.8* width or height of canvas - /2 the width or height of the spawn location
#basically, obstacles can spawn anywhere outiside the spawn patch

def createObstacles():
    terrainOne = Image.open('./threejsFold/Heightmaps/mountains/1.jpg').convert("RGB")
    adjustX=300+random.randint(-int(0.25*im.width),int(0.25*im.width))
    adjustY=300+random.randint(-int(0.25*im.height),int(0.25*im.height))
    angle=50

    obstacles.append([terrainOne,(adjustX,adjustY),angle,2])
    corners=getCornersOfAdjustedImage((adjustX,adjustY),terrainOne)
    obstacleBounds.append(corners)
    # terrainOne=terrainOne.resize((int(terrainOne.width/2), int(terrainOne.height/2)), Image.Resampling.LANCZOS)
    # im.paste(terrainOne, (adjustX-int(terrainOne.width/2),adjustY-int(terrainOne.height/2))) 
    
    adjustX=500
    adjustY=500
    angle=0
    # terrainOne=terrainOne.resize((int(terrainOne.width/0.5), int(terrainOne.height/0.5)), Image.Resampling.LANCZOS)
    obstacles.append([terrainOne,(adjustX,adjustY),angle,1])
    corners=getCornersOfAdjustedImage((adjustX,adjustY),terrainOne)
    obstacleBounds.append(corners)

    
    adjustX=0
    adjustY=500
    angle=0

    obstacles.append([terrainOne,(adjustX,adjustY),angle,1])
    corners=getCornersOfAdjustedImage((adjustX,adjustY),terrainOne)
    obstacleBounds.append(corners)
    
    adjustX=100
    adjustY=430
    angle=50

    obstacles.append([terrainOne,(adjustX,adjustY),angle,1])
    corners=getCornersOfAdjustedImage((adjustX,adjustY),terrainOne)
    obstacleBounds.append(corners)

    adjustX=0
    adjustY=200
    angle=50

    obstacles.append([terrainOne,(adjustX,adjustY),angle,1])
    corners=getCornersOfAdjustedImage((adjustX,adjustY),terrainOne)
    obstacleBounds.append(corners)




def DetectIfPointWithinBox(pointArray,point):
    #pointArray should be the four points of an obstacle, topleft, topright, bottomleft,bottomright
    if(point[0]>pointArray[0][0] and point[0]<pointArray[1][0]):#if within Xrange of box
        if(point[1]>pointArray[0][1] and point[1]<pointArray[2][1]):
            # print("HIT IN")
            return True
        else:
            return False
    else:
        return False

def GetArrayOfValidRiverEdgePoints():
    ValidPoints=[]
    for obstacle in obstacleBounds:
        # print(obstacle)
        for point in obstacle:
            within=False#assume point is valid and out the bounds of some other obstacle
            if(point[0]<=im.width and point[0]>=0 and point[1]>=0 and point[1]<=im.height):
                for traverseObst in obstacleBounds:
                    if(traverseObst!=obstacle):#so it doesnt go over itself
                        within=DetectIfPointWithinBox(traverseObst,point)
                        if(within==True):#if point isnt within the 
                            break
                if(within==False):
                    ValidPoints.append(point)
    return ValidPoints

#the path the river takes is the start will go to the closest valid point
def pointPath():
    pathArray=[riverStart]
    validPoints=GetArrayOfValidRiverEdgePoints()
    validPoints.append(riverEnd)
    currPoint=riverStart
    while currPoint!=riverEnd :
        closest=None
        closestmag=None
        #find magnitude between current point and all other points saving the closest
        for validPoint in validPoints:
            addedSquared=(validPoint[0]-currPoint[0])**2+(validPoint[1]-currPoint[1])**2
            mag=math.sqrt(addedSquared)
            if(closestmag!=None and closestmag>mag):
                closestmag=mag
                closest=validPoint
            elif(closestmag==None):
                closestmag=mag
                closest=validPoint
        # print(currPoint,closest)
        currPoint=closest
        pathArray.append(closest)
        validPoints.remove(closest)
        
    return pathArray
# print(pointPath())


def pointsOnLineBetweenTwoPoints(pointOne, pointTwo):#returns a set of points along the line, the number based on the magnitude 
    OutputArray=[]
    for num in range(41):
        partX=int(pointOne[0]+num*((pointTwo[0]-pointOne[0])/40))
        partY=int(pointOne[1]+num*((pointTwo[1]-pointOne[1])/40))
        OutputArray.append((partX,partY))
    # print(OutputArray)
    return OutputArray

def drawDot(center,scale):
    hillbrush = Image.open('./threejsFold/Heightmaps/softDotGradientTwo.png').convert("RGB")
    hillbrush = hillbrush.resize((int(hillbrush.width/scale), int(hillbrush.height/scale)), Image.Resampling.LANCZOS)
    clampRGB=hillbrush.getpixel((int(hillbrush.width/2),int(hillbrush.height/2)))
    brightnessclampRGB=(0.2126*clampRGB[0] + 0.7152*clampRGB[1]  + 0.0722*clampRGB[2] )
    adjustX=center[0]
    adjustY=center[1]
    tudorBrown=(79,57,48)
    for yy in range( hillbrush.height):
        for xx in range( hillbrush.width):
            #im.size[0]*im.size[1]/5) ):
            rr, gg, bb = hillbrush.getpixel((xx, yy))
            # print(r,g,b)
            overEqZx=(adjustX -int(hillbrush.width/2)+ xx)>=0
            overEqZy=(adjustY-int(hillbrush.height/2) + yy)>=0
            underEqZmaxX=(adjustX-int(hillbrush.width/2) + xx)<=im.size[0]-1
            underEqZmaxY=(adjustY-int(hillbrush.height/2) + yy)<=im.size[1]-1

            if((rr,gg,bb)>=(1,1,1) and overEqZx and overEqZy and underEqZmaxX and underEqZmaxY):
                R,G,B=im.getpixel((adjustX -int(hillbrush.width/2)+ xx, adjustY-int(hillbrush.height/2) + yy))
                texRGB=texturemap.getpixel((adjustX -int(hillbrush.width/2)+ xx, adjustY-int(hillbrush.height/2) + yy))
                
                #gets brighter on the brush towards the center, in practice this is subtracted so its black in the texture
                #if you get the brightness of the brush, divide it by the brightest, ie the center of the brush (clampRGB) 
                brightnessBrush=(0.2126*rr + 0.7152*gg + 0.0722*bb)
                ratio= brightnessBrush/brightnessclampRGB

                newColourX=int(texRGB[0]*(1-ratio))+int(tudorBrown[0]*(ratio))
                newColourY=int(texRGB[1]*(1-ratio))+int(tudorBrown[1]*(ratio))
                newColourZ=int(texRGB[2]*(1-ratio))+int(tudorBrown[2]*(ratio))
                newColour=(newColourX,newColourY,newColourZ)

                brightnessOne=(0.2126*R + 0.7152*G + 0.0722*B)
                
                # if(brightnessOne<brightnessTwo):
                #     im.putpixel((adjustX -int(hillbrush.width/2)+ xx, adjustY-int(hillbrush.height/2) + yy), (rr,gg,bb))
                added=(int((rr+R)/1),int((gg+G)/1),int((bb+B)/1))
                subtracted=((R-rr,G-gg,B-bb))
                brightnessAdded=(0.2126*added[0] + 0.7152*added[1]  + 0.0722*added[2] )
                brightnesssubbed=(0.2126*subtracted[0] + 0.7152*subtracted[1]  + 0.0722*subtracted[2] )
                
                if(brightnesssubbed<brightnessclampRGB):
                    im.putpixel((adjustX -int(hillbrush.width/2)+ xx, adjustY-int(hillbrush.height/2) + yy), subtracted)
                    texturemap.putpixel((adjustX -int(hillbrush.width/2)+ xx, adjustY-int(hillbrush.height/2) + yy), newColour)
                else:
                    im.putpixel((adjustX -int(hillbrush.width/2)+ xx, adjustY-int(hillbrush.height/2) + yy), clampRGB)

def drawLinesFromPath():
    PathPoints=pointPath()
    # print(len(PathPoints))
    for step in range(len(PathPoints)-1):
        # print(PathPoints[step],PathPoints[step+1])
        for coord in pointsOnLineBetweenTwoPoints(PathPoints[step],PathPoints[step+1]):
            drawDot(coord,8)
    # arrayOne=pointsOnLineBetweenTwoPoints((0,300),(300,300))

    return 0




#generate 

# createBasicTerrainFlow()

# createObstacles()
# drawLinesFromPath()

# for obst in obstacles:
#     center=obst[0]
#     ImageUsed=obst[1]
#     scale=obst[2]
#     angle=obst[3]
#     DrawImageOnCenter(ImageUsed,center,angle,scale)

brushWidthHalf=int(236/2)
brushHeightHalf=int(236/2)
gendObstacleCentersAndRot=[]
PythTriangleDistFromCenter=167 #at least for 236, around 167

PathPoints=pointPath()
PathPoints=pointsOnLineBetweenTwoPoints(PathPoints[0],PathPoints[1])
# print("pathpoints",PathPoints)
while len(gendObstacleCentersAndRot)!=15:#generates centers for obstacles on the edges
    randomX=random.randint(0,im.width)
    randomY=random.randint(0,im.height)        
    if(randomX<=int(im.width/4)-brushWidthHalf or randomY<=int(im.height/4)-brushWidthHalf or randomX>=int(im.width*0.75)+brushWidthHalf or randomY>=int(im.height*0.75)+brushWidthHalf):
        # im.putpixel((randomX,y),(255,255,255))
        centeringPoint=(randomX,randomY)#check if the point is too close to river entry or exit
        IMGtopLeftCorner=(randomX-brushWidthHalf,randomY-brushHeightHalf)
        IMGtopRightCorner=(randomX+brushWidthHalf,randomY-brushHeightHalf)
        IMGBottomLeftCorner=(randomX-brushWidthHalf,randomY+brushHeightHalf)
        IMGBottomRightCorner=(randomX+brushWidthHalf,randomY+brushHeightHalf)
        BrushCorners=[IMGtopLeftCorner,IMGtopRightCorner,IMGBottomLeftCorner,IMGBottomRightCorner]

        withinTF=False
        for PP in PathPoints:
            PPX=PP[0]
            PPY=PP[1]
            topLeftCorner=(PPX-32,PPY-32)
            topRightCorner=(PPX+32,PPY-32)
            BottomLeftCorner=(PPX-32,PPY+32)
            BottomRightCorner=(PPX+32,PPY+32)
            corners=[topLeftCorner,topRightCorner,BottomLeftCorner,BottomRightCorner]
            for corn in corners:
                withinTF=DetectIfPointWithinBox(BrushCorners,corn)
                
                if(withinTF==True):#if there is a point within spawn area bounds, no point checking the other corners
                    break
            if(withinTF==True):#if there is a point within spawn area bounds, no point continuing down the riverpath
                break
        if(withinTF==False):
            gendObstacleCentersAndRot.append((randomX,randomY,random.randint(0,360)))

        # addedSquaredExit=(centeringPoint[0]-riverEnd[0])**2+(centeringPoint[1]-riverEnd[1])**2
        # addedSquaredEntry=(centeringPoint[0]-riverStart[0])**2+(centeringPoint[1]-riverStart[1])**2
        # magToExit=math.sqrt(addedSquaredExit)
        # magToEntry=math.sqrt(addedSquaredEntry)
        # if(magToExit>PythTriangleDistFromCenter and magToEntry>PythTriangleDistFromCenter and withinTF==False):
        #     gendObstacleCentersAndRot.append((randomX,randomY,random.randint(0,360)))

ImageUsed=Image.open('./threejsFold/Heightmaps/mountains/1.jpg').convert("RGB")
for hehe in gendObstacleCentersAndRot:
    # print(hehe)
    center=(hehe[0],hehe[1])
    DrawImageOnCenter(center,ImageUsed,1,hehe[2])
    # corners=getCornersOfAdjustedImage(center,ImageUsed)
    # obstacleBounds.append(corners)
# corners=getCornersOfAdjustedImage((300,300),ImageUsed)


for CanvasY in range( im.height):
    for CanvasX in range( im.width):
        R,G,B=im.getpixel((CanvasX,CanvasY))
        # print(curCol)
        brightnessCanvas=(0.2126*R + 0.7152*G + 0.0722*B)
        brightnessmax=(0.2126*255 + 0.7152*255 + 0.0722*255)

        ratio=brightnessCanvas/brightnessmax #so on the edge its basically 0, aproaching and after ratio becomes 1, more rock colour
        grassColour=getGrassColour()
        rockColour=getRockColour()
        # rockColourTwo[0]*(ratio -0.4) 
        NCR=int(grassColour[0]*(1-ratio)**8+ rockColour[0]*(ratio))
        NCG=int(grassColour[1]*(1-ratio)**8+ rockColour[1]*(ratio))
        NCB=int(grassColour[2]*(1-ratio)**8+ rockColour[2]*(ratio))
        newColour=(NCR,NCG,NCB)

        texturemap.putpixel((CanvasX,CanvasY), newColour)

createBasicTerrainFlow()
drawLinesFromPath()#draws the river

(
#you have the start and endpoint of the river, you know that the obstacles will never step into int(im.width/4) etc...
#a spawn area is a square, so this spawn area needs to be within that inner area of the canvas away from the obstacles
#but the spawn area also needs to not touch the river which is 
#    riverbrush = Image.open('./threejsFold/Heightmaps/softDotGradientTwo.png').convert("RGB")
#    riverbrush = riverbrush.resize((int(riverbrush.width/8), int(riverbrush.height/8)), Image.Resampling.LANCZOS)
#the height and width of the riverbrush should be 64, 512/8, so, from anypoint along the riverline, 32 left or right is invalid for any
    #point of the spawn to be in, making the spawn location invalid
)

spawnHeight=50
spawnWidth=50
#so the spawn center cant be closer than 100 to the edge of the inner area
validSpawnCoord=None
while validSpawnCoord==None:#generates centers for obstacles on the edges
    randomX=random.randint(0,im.width)
    randomY=random.randint(0,im.height)        
    if(randomX<=int(im.width/4)+spawnWidth/2 or randomY<=int(im.height/4)+spawnHeight/2 or randomX>=int(im.width*0.75)-spawnWidth/2 or randomY>=int(im.height*0.75)-spawnHeight/2):
        pass
    else:#point is within the valid area a spawn can be created, check for river conflict
        PathPoints=pointPath()
        PathPoints=pointsOnLineBetweenTwoPoints(PathPoints[0],PathPoints[1])

        SPAWNtopLeftCorner=(randomX-int(spawnWidth/2),randomY-int(spawnHeight/2))
        SPAWNtopRightCorner=(randomX+int(spawnWidth/2),randomY-int(spawnHeight/2))
        SPAWNBottomLeftCorner=(randomX-int(spawnWidth/2),randomY+int(spawnHeight/2))
        SPAWNBottomRightCorner=(randomX+int(spawnWidth/2),randomY+int(spawnHeight/2))
        cornersSpawn=[SPAWNtopLeftCorner,SPAWNtopRightCorner,SPAWNBottomLeftCorner,SPAWNBottomRightCorner]
        withinTF=False
        for PP in PathPoints:
            PPX=PP[0]
            PPY=PP[1]
            topLeftCorner=(PPX-32,PPY-32)
            topRightCorner=(PPX+32,PPY-32)
            BottomLeftCorner=(PPX-32,PPY+32)
            BottomRightCorner=(PPX+32,PPY+32)
            corners=[topLeftCorner,topRightCorner,BottomLeftCorner,BottomRightCorner]
            for corn in cornersSpawn:
                withinTF=DetectIfPointWithinBox(corners,corn)
                # print(withinTF)
                if(withinTF==True):#if there is a point within spawn area bounds, no point checking the other corners
                    break
            if(withinTF==True):#if there is a point within spawn area bounds, no point continuing down the riverpath
                break
        if(withinTF==False):
            validSpawnCoord=(randomX,randomY)
        

        # im.putpixel((x,y),(0,0,0))

    # topLeftCorner=(adjustX-int(ImageUsed.width/2),adjustY-int(ImageUsed.height/2))
    # topRightCorner=(adjustX+int(ImageUsed.width/2),adjustY-int(ImageUsed.height/2))
    # BottomLeftCorner=(adjustX-int(ImageUsed.width/2),adjustY+int(ImageUsed.height/2))
    # BottomRightCorner=(adjustX+int(ImageUsed.width/2),adjustY+int(ImageUsed.height/2))

    # return [topLeftCorner,topRightCorner,BottomLeftCorner,BottomRightCorner]

for y in range( 50):
    for x in range( 50):
        im.putpixel((validSpawnCoord[0] -int(spawnWidth/2)+ x, validSpawnCoord[1]-int(spawnHeight/2) + y), (255,255,255))

#gets the points used to draw the river, get the corners of that and check for each corner is in the bounding box of spawn

im.show()
im.save('C:/Users/david/Documents/coding projects/wegbgl experiments/nodejs/threejsFold/heightmapTexture.png')
texturemap.show()
texturemap.save('C:/Users/david/Documents/coding projects/wegbgl experiments/nodejs/threejsFold/textureMap.png')
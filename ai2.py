import random
import time
import multiprocessing
import Queue

dUP = -1
dRIGHT = 1
dDOWN = 1
dLEFT = -1
dpDir = [(0, -1),(1, 0),(0, 1),(0, -1)]
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
STOP = 4

class ai_agent():
    mapinfo = []
   
    def __init__(self):
        self.mapinfo = []
        self.flag = False
        self.flagPlace = {'x': [12, 13],  'y': [24, 25]}
        self.bulletSpeed = 5
        self.place = {'x': 0, 'y': 0}
        self.speed  = 0

    # rect:                    [left, top, width, height]
    # rect_type:            0:empty 1:brick 2:steel 3:water 4:grass 5:froze
    # castle_rect:            [12*16, 24*16, 32, 32]
    # mapinfo[0]:             bullets [rect, direction, speed]]
    # mapinfo[1]:             enemies [rect, direction, speed, type]]
    # enemy_type:            0:TYPE_BASIC 1:TYPE_FAST 2:TYPE_POWER 3:TYPE_ARMOR
    # mapinfo[2]:             tile     [rect, type] (empty don't be stored to mapinfo[2])
    # mapinfo[3]:             player     [rect, direction, speed, Is_shielded]]
    # shoot:                0:none 1:shoot
    # move_dir:                0:Up 1:Right 2:Down 3:Left 4:None
    # keep_action:            0:The tank work only when you Update_Strategy.     1:the tank keep do previous action until new Update_Strategy.

    # def Get_mapInfo:        fetch the map infomation
    # def Update_Strategy    Update your strategy


    def delay (self):
        for i in range(1000000):
            pass
        return
    
    def mapinfoToCoorMap(self):
        coorMap = [[0 for j in range(0,26)] for i in range(0,26)]
        clearMap = [['.' for j in range(0,26)] for i in range(0,26)]
        
        
        
        for i in self.mapinfo[2]:
            #print str(i[0][0]/16)+" "+str(i[0][1]/16)
            x = i[0][0]/16
            y = i[0][1]/16
            coorMap[x][y] = i[1]
            if i[1] == 1 or i[1] == 2:
                clearMap[x][y] = '#'
        
        for i in self.mapinfo[1]:
            x = i[0][0]/16
            y = i[0][1]/16
            for j in range(x, x+2):
                for k in range(y, y+2):
                    coorMap[j][k] = 7
                    clearMap[j][k] = 'E'
                    
        
        for i in self.flagPlace['x']:
            for j in self.flagPlace['y']:
                coorMap[i][j] = 8
                clearMap[i][j] = 'F'
                
        for i in self.mapinfo[3]:
            x = self.place['x'] = i[0][0]/16
            y = self.place['y'] = i[0][1]/16
            for j in range(x, x+2):
                for k in range(y, y+2):
                    coorMap[j][k] = 9
                    clearMap[j][k] = 'P'
            
        self.speed = self.mapinfo[3][0][2]
        #print self.mapinfo[3]
        
        
        return coorMap, clearMap
    
    def findNearestTank(self):
        for i in self.mapinfo[1]:
            pass
            
    def enemyActionPredict(self, bulletMap):
        
        for directionX in [-1, 1]:
            x = self.place['x']
            y = self.place['y']   
            x += directionX
            while x <= 25 and x >= 0 and bulletMap[x][y] != '#':
                bulletMap[x][y] = '*'
                x += directionX
            
        for directionY in [-1, 1]:
            x = self.place['x']
            y = self.place['y']   
            y += directionY 
            while y <= 25 and y >= 0 and bulletMap[x][y] != '#':
                bulletMap[x][y] = '*'
                y += directionY
        
        for i in self.mapinfo[1]:
            enemyX = x = i[0][0]/16
            enemyY = y = i[0][1]/16
            #print i[1]

            direction = dpDir[i[1]]
            speed = i[2]
            while bulletMap[x][y] != '#':
                
                if bulletMap[x][y] == '*':
                    disX = abs(self.place['x']-x)
                    disY = abs(self.place['y']-y)
                    #print str(enemyX)+" "+str(enemyY)
                    #print "disX: "+str(disX)+" disY: "+str(disY)
                    bulletTime = float((disX + disY) * 16 / self.bulletSpeed)
                    enemyDisX = abs(enemyX-x)
                    enemyDisY = abs(enemyY-y)
                    #print "enemyDisX: "+str(enemyDisX)+" enemyDisY: "+str(enemyDisY)
                    arriveTime = float((enemyDisX + enemyDisY) * 16 / speed)
                    if abs( bulletTime - arriveTime ) < 0.1 or arriveTime <= 0:
                        return True
                    break
                else:
                    x += direction[0]
                    y += direction[1]
                    
                if x < 0 or x > 25 or y < 0 or y > 25:
                    break
            
            return False
            
        
            
    
    def operations (self,p_mapinfo,c_control):    
        
        while True:
        #-----your ai operation,This code is a random strategy,please design your ai !!-----------------------            
            
            
            self.Get_mapInfo(p_mapinfo)
            #print self.mapinfo[0]
            #print self.mapinfo[1]
            #print self.mapinfo[2]
            #print self.mapinfo[3]
            #time.sleep(0.001)    
            
            self.delay()
            
            
            #shoot = random.randint(0,1)
            shoot = 0
            coorMap, clearMap = self.mapinfoToCoorMap() 
            if(self.enemyActionPredict(clearMap)):
                shoot = 1
            else:
                shoot = 0
            #print "--"
                         
                
            
            move_dir = random.randint(0,4)
            #keep_action = 0
            keep_action = 1
            #-----------
            #if self.flag == False:
            self.Update_Strategy(c_control,shoot,4,0)
                #self.flag = True
        #------------------------------------------------------------------------------------------------------

    def Get_mapInfo(self,p_mapinfo):
        if p_mapinfo.empty()!=True:
            try:
                self.mapinfo = p_mapinfo.get(False)
            except Queue.Empty:
                skip_this=True

    def Update_Strategy(self,c_control,shoot,move_dir,keep_action):
        if c_control.empty() ==True:
            c_control.put([shoot,move_dir,keep_action])
            return True
        else:
            return False


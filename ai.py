# import random
# import time
# import multiprocessing
import Queue

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
STOP = 4
CASTLE = {'x': [192, 224], 'y': [384, 416]}


class ai_agent():
    mapinfo = []

    def __init__(self):
        self.mapinfo = []
        self.isFirst = True

# rect:					[left, top, width, height]
# rect_type:			0:empty 1:brick 2:steel 3:water 4:grass 5:froze
# castle_rect:			[12*16, 24*16, 32, 32]
# mapinfo[0]: 			bullets [rect, direction, speed]]
# mapinfo[1]: 			enemies [rect, direction, speed, type]]
# enemy_type:			0:TYPE_BASIC 1:TYPE_FAST 2:TYPE_POWER 3:TYPE_ARMOR
# mapinfo[2]: 			tile 	[rect, type] (empty don't be stored to mapinfo[2])
# mapinfo[3]: 			player 	[rect, direction, speed, Is_shielded]]
# shoot:				0:none 1:shoot
# move_dir:				0:Up 1:Right 2:Down 3:Left 4:None
# keep_action:			0:The tank work only when you Update_Strategy.
#              1:the tank keep do previous action until new Update_Strategy.

# def Get_mapInfo:		fetch the map infomation
# def Update_Strategy	Update your strategy

    def checkEnemy(self):
        playerX = self.mapinfo[3][0][0][0]
        playerY = self.mapinfo[3][0][0][1]

        minDistance = 400000
        move_dir = STOP

        for i in self.mapinfo[1]:
            disX = abs(playerX - i[0][0])
            disY = abs(playerY - i[0][1])

            if (disX * disX) + (disY * disY) > minDistance:
                continue
            else:
                minDistance = (disX * disX) + (disY * disY)

            if disX < 80 and disY < 80:
                print "both"
                if disX > disY:
                    if disY < 24:
                        if playerX > i[0][0]:
                            move_dir = LEFT
                        else:
                            move_dir = RIGHT
                    else:
                        if playerY > i[0][1]:
                            move_dir = UP
                        else:
                            move_dir = DOWN
                else:
                    if disX < 24:
                        if playerY > i[0][1]:
                            move_dir = UP
                        else:
                            move_dir = DOWN
                    else:
                        if playerX > i[0][0]:
                            move_dir = LEFT
                        else:
                            move_dir = RIGHT
            elif disX < 80:
                print "a"
                if playerY > i[0][1]:
                    move_dir = UP
                else:
                    move_dir = DOWN
            elif disY < 80:
                print "b"
                if playerX > i[0][0]:
                    move_dir = LEFT
                else:
                    move_dir = RIGHT
            else:
                continue

        if playerY >= CASTLE['y'][0]-16 and playerY <= CASTLE['y'][1]+16:
            if move_dir == LEFT and playerX > CASTLE['x'][1]:
                move_dir = STOP
            elif move_dir == RIGHT and playerX < CASTLE['x'][0]:
                move_dir = STOP
        elif move_dir == DOWN:
            if playerX >= CASTLE['x'][0]-16 and playerX <= CASTLE['x'][1]+16:
                move_dir = STOP

        return move_dir

    def operations(self, p_mapinfo, c_control):

        while True:
            self.Get_mapInfo(p_mapinfo)

            q = 0
            for i in range(50000):
                q += 1
            del q

            print self.mapinfo[1]

            pointMap = [[0 for j in range(0, 26)] for i in range(0, 26)]
            for i in self.mapinfo[2]:
                if i[1] == 1:
                    pointMap[i[0][0]/16][i[0][1]/16] = 1
                elif i[1] == 2:
                    pointMap[i[0][0]/16][i[0][1]/16] = 2

            move_dir = self.checkEnemy()
            # print move_dir
            shoot = 0
            if move_dir != STOP:
                shoot = 1
            else:
                pass

            print "shoot:"+str(shoot)
            keep_action = 0
            self.Update_Strategy(c_control, shoot, move_dir, keep_action)
            del pointMap

    def Get_mapInfo(self, p_mapinfo):
        if not p_mapinfo.empty():
            try:
                del self.mapinfo
                self.mapinfo = []
                self.mapinfo = p_mapinfo.get(False)
            except Queue.Empty:
                skip_this = True

    def Update_Strategy(self, c_control, shoot, move_dir, keep_action):
        if c_control.empty():
            c_control.put([shoot, move_dir, keep_action])
            return True
        else:
            return False


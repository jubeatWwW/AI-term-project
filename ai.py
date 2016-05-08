# import random
# import time
# import multiprocessing
import Queue

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
STOP = 4
DP = [(0, -1), (1, 0), (0, 1), (-1, 0)]
OPPSITE = [DOWN, LEFT, UP, RIGHT]
CASTLE = {'x': [192, 224], 'y': [384, 416]}


class ai_agent():
    mapinfo = []
    pointMap = []
    playerPointX = 0
    playerPointY = 0
    playerX = 0
    playerY = 0
    targetPointX = 0
    targetPointY = 0
    targetX = 0
    targetY = 0
    stockCounter = 300
    lastPos = [0, 0]
    isStock = False
    goBack = STOP
    goBackCnt = 75
    pathStockCounter = 100
    pathLastPos = (0, 0)
    isDFS = False
    lastDfsDir = 0
    nextPos = (0, 0)

    def __init__(self):
        self.mapinfo = []
        self.pointMap = []
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
        self.playerX = self.mapinfo[3][0][0][0]
        self.playerY = self.mapinfo[3][0][0][1]
        self.playerPointX = self.playerX / 16
        self.playerPointY = self.playerY / 16

        if self.isStock:
            if self.goBackCnt > 0:
                self.goBackCnt -= 1
                return self.goBack, 1
            else:
                self.goBackCnt = 75
                self.isStock = False
                self.stockCounter = 300

        minDistance = 400000
        move_dir = STOP
        shoot = 0

        for i in self.mapinfo[1]:
            disX = abs(self.playerX - i[0][0])
            disY = abs(self.playerY - i[0][1])

            if (disX * disX) + (disY * disY) > minDistance:
                continue
            else:
                minDistance = (disX * disX) + (disY * disY)
                self.targetX = i[0][0]
                self.targetY = i[0][1]
                self.targetPointX = self.targetX / 16
                self.targetPointY = self.targetY / 16

            if disX < 80 and disY < 80:
                # print "both"
                if disX > disY:
                    if disY < 26:
                        if self.playerX > i[0][0]:
                            move_dir = LEFT
                        else:
                            move_dir = RIGHT
                    else:
                        if self.playerY > i[0][1]:
                            move_dir = UP
                        else:
                            move_dir = DOWN
                else:
                    if disX < 26:
                        if self.playerY > i[0][1]:
                            move_dir = UP
                        else:
                            move_dir = DOWN
                    else:
                        if self.playerX > i[0][0]:
                            move_dir = LEFT
                        else:
                            move_dir = RIGHT
            elif disX < 80:
                # print "a"
                if disX > 26:
                    if self.playerX > i[0][0]:
                        move_dir = LEFT
                    else:
                        move_dir = RIGHT
                else:
                    if self.playerY > i[0][1]:
                        move_dir = UP
                    else:
                        move_dir = DOWN
            elif disY < 80:
                # print "b"
                if disY > 26:
                    if self.playerY > i[0][1]:
                        move_dir = UP
                    else:
                        move_dir = DOWN
                else:
                    if self.playerX > i[0][0]:
                        move_dir = LEFT
                    else:
                        move_dir = RIGHT
            else:
                continue

        if move_dir != STOP:
            shoot = 1

        if minDistance < (28*28*2) and self.stockCounter <= 0:
            self.isStock = True
            self.goBack = OPPSITE[self.mapinfo[3][0][1]]
            return OPPSITE[self.mapinfo[3][0][1]], 0

        # print self.lastPos
        print self.stockCounter
        if self.lastPos[0] == self.playerX and \
            self.lastPos[1] == self.playerY and \
                minDistance < (24*24*2):
                self.stockCounter -= 1
        else:
            self.lastPos = [self.playerX, self.playerY]
            self.stockCounter = 300

        return move_dir, shoot

    def pathFinder(self, enemy_dir, shoot):
        ret_dir = enemy_dir
        self.pointMap = [[0 for j in range(0, 26)] for i in range(0, 26)]
        for i in self.mapinfo[2]:
            self.pointMap[i[0][0]/16][i[0][1]/16] = i[1]

        if not enemy_dir == STOP:
            mapX1 = (self.playerX + 9) / 16
            mapY1 = (self.playerY + 9) / 16
            mapX2 = (self.playerX + 17) / 16
            mapY2 = (self.playerY + 17) / 16
            while mapX1 != self.targetPointX and \
                    mapY1 != self.targetPointY and \
                    mapX2 != self.targetPointX and \
                    mapY2 != self.targetPointY:

                if mapX1 < 0 or mapX1 > 24:
                    break
                elif mapY1 < 0 or mapY1 > 24:
                    break

                if self.pointMap[mapX1][mapY1] == 2 or \
                        self.pointMap[mapX2][mapY2] == 2:
                    ret_dir = STOP
                    shoot = 0
                    break

                mapX1 += DP[enemy_dir][0]
                mapY1 += DP[enemy_dir][1]
                mapX2 += DP[enemy_dir][0]
                mapY2 += DP[enemy_dir][1]

        return ret_dir, shoot

    def DFS(self):
        currentX = self.playerPointX
        currentY = self.playerPointY
        tx = self.mapinfo[1][0][0]
        ty = self.mapinfo[1][0][1]
        searchDir = [0, 0, 0, 0]

        if currentX < tx:
            searchDir[1] = RIGHT
            searchDir[3] = LEFT
        else:
            searchDir[1] = LEFT
            searchDir[3] = RIGHT

        if currentY < ty:
            searchDir[1] = DOWN
            searchDir[3] = UP
        else:
            searchDir[1] = UP
            searchDir[3] = DOWN

        stack = []
        visited = [(currentX, currentY)]
        cannotPass = [1, 2, 3]

        while currentX != tx or currentY != ty:
            print str(currentX)+"  "+str(currentY)
            flag = False
            for i in searchDir:
                nextX = currentX + DP[i][0]
                nextY = currentY + DP[i][1]
                if nextX > 25 or nextX < 0:
                    continue
                if nextY > 25 or nextY < 0:
                    continue
                if i == 1 or i == 3:
                    if nextY+1 > 25:
                        continue
                    if self.pointMap[nextX][nextY] in cannotPass or \
                            self.pointMap[nextX][nextY+1] in cannotPass:
                        continue
                else:
                    if nextX+1 > 25:
                        continue
                    if self.pointMap[nextX][nextY] in cannotPass or \
                            self.pointMap[nextX+1][nextY] in cannotPass:
                        continue

                if (nextX, nextY) in visited:
                    continue

                stack.append((nextX, nextY))
                visited.append((nextX, nextY))
                currentX = nextX
                currentY = nextY
                flag = True
                break

            if not flag:
                stack.pop()
                if len(stack) == 0:
                    return STOP
                currentX = stack[-1:][0][0]
                currentY = stack[-1:][0][1]
            print stack
            if len(stack) > 20:
                break

        del visited
        self.nextPos = (stack[0][0], stack[0][1])
        if stack[0][0] != self.playerPointX:
            if stack[0][0] < self.playerPointX:
                return LEFT
            else:
                return RIGHT
        if stack[0][1] != self.playerPointY:
            if stack[0][1] < self.playerPointY:
                return UP
            else:
                return DOWN

    def bulletCheck(self, move_dir):
        if move_dir == STOP:
            return STOP
        for i in self.mapinfo[0]:
            if i[1] == UP or i[1] or DOWN:
                if move_dir == LEFT:
                    if i[0][0] > self.playerX - 26:
                        return STOP
                elif move_dir == RIGHT:
                    if i[0][0] < self.playerX + 26:
                        return STOP
            elif i[1] == RIGHT or i[1] == LEFT:
                if move_dir == UP:
                    if i[0][1] > self.playerY - 26:
                        return STOP
                elif move_dir == DOWN:
                    if i[0][1] < self.playerY + 26:
                        return STOP

    def operations(self, p_mapinfo, c_control):

        while True:
            self.Get_mapInfo(p_mapinfo)

            q = 0
            for i in range(50000):
                q += 1
            del q

            print self.mapinfo[3]
            shoot = 0
            enemy_dir, shoot = self.checkEnemy()
            move_dir, shoot = self.pathFinder(enemy_dir, shoot)

            if self.playerY >= CASTLE['y'][0] and \
                    self.playerY <= CASTLE['y'][1]:
                if move_dir == LEFT and self.playerX > CASTLE['x'][1]:
                    shoot = 0
                elif move_dir == RIGHT and self.playerX < CASTLE['x'][0]:
                    shoot = 0
            elif move_dir == DOWN:
                if self.playerX >= CASTLE['x'][0] and \
                        self.playerX <= CASTLE['x'][1]:
                    shoot = 0

            if move_dir == STOP and len(self.mapinfo[1]) > 0:
                if not self.isDFS:
                    move_dir = self.DFS()
                    self.isDSF = True
                    shoot = 1
                    self.lastDfsDir = move_dir

            if self.isDFS:
                move_dir = self.lastDfsDir
                if self.lastDfsDir == LEFT:
                    if abs(self.playerX - self.nextPos[0]) < 4:
                        self.isDFS = False
                elif self.lastDfsDir == RIGHT:
                    if abs(self.playerX - self.nextPos[0]) < 30:
                        self.isDFS = False
                elif self.lastDfsDir == UP:
                    if abs(self.playerY - self.nextPos[1]) < 4:
                        self.isDFS = False
                elif self.lastDfsDir == DOWN:
                    if abs(self.playerY - self.nextPos[1]) < 30:
                        self.isDFS = False

            if len(self.mapinfo[1]) == 0:
                move_dir = UP

            # bullet_avoid = self.bulletCheck(move_dir)

            # print "shoot:"+str(shoot)
            keep_action = 0
            self.Update_Strategy(c_control, shoot, move_dir, keep_action)
            del self.pointMap
            self.pointMap = []

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


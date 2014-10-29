#
# MAZE
# 
# Example game
#
# Version without baddies running around
#

from graphics import *

LEVEL_WIDTH = 35
LEVEL_HEIGHT = 20

CELL_SIZE = 24
WINDOW_WIDTH = CELL_SIZE*LEVEL_WIDTH
WINDOW_HEIGHT = CELL_SIZE*LEVEL_HEIGHT

OBJS = {}
GOLD = 0

def screen_pos (x,y):
    return (x*CELL_SIZE+10,y*CELL_SIZE+10)

def screen_pos_index (index):
    x = index % LEVEL_WIDTH
    y = (index - x) / LEVEL_WIDTH
    return screen_pos(x,y)

def index (x,y):
    return x + (y*LEVEL_WIDTH)

def win (level,window):
    for i in range(1,19):
# TODO: Index out of range error for final gold
        spot = i * 34
        if level[index(i,spot)] == 0:
            elt = Image(Point(i+CELL_SIZE/2,spot+CELL_SIZE/2),'ladder.gif')
            elt.draw(window)
            OBJS[i,spot] = elt
        else:
            break

class Character (object):
    def __init__ (self,pic,x,y,window,level):
        (sx,sy) = screen_pos(x,y)
        self._img = Image(Point(sx+CELL_SIZE/2,sy+CELL_SIZE/2+2),pic)
        self._window = window
        self._img.draw(window)
        self._x = x
        self._y = y
        self._level = level

    def same_loc (self,x,y):
        return (self._x == x and self._y == y)

    def move (self,dx,dy):
        global GOLD
        tx = self._x + dx
        ty = self._y + dy     
        if tx >= 0 and ty >= 0 and tx < LEVEL_WIDTH and ty < LEVEL_HEIGHT:
            if dy == -1 and self._level[index(tx,ty)] == 3 and self._level[index(tx,ty)] == 1:
                pass
            else:
                if self._level[index(tx,ty)] != 1:
                    self._x = tx
                    self._y = ty
                    self._img.move(dx*CELL_SIZE,dy*CELL_SIZE)
                    # logic for ladders and rope and falling
                    if self._level[index(tx,ty)] == 0 and self._level[index(tx,ty+1)] != 1:
                        if self._level[index(tx,ty+1)] != 2:
                            self.move(0,1)
                    # logic for picking up gold
                    if self._level[index(tx,ty)] == 4:
                        GOLD -= 1
                        if GOLD == 0:
                            win(self._level, self._window)
                        self._window.delItem(OBJS[self._x,self._y])
                        OBJS[self._x,self._y] = 0
                        self._level[index(tx,ty)] = 0
                        self._window.redraw()


    def dig (self,dx,dy):
        tx = self._x + dx
        ty = self._y + dy     
        if tx >= 0 and ty >= 0 and tx < LEVEL_WIDTH and ty < LEVEL_HEIGHT:
            if self._level[index(tx,ty)] == 1 and self._level[index(tx,ty-1)] == 0:
                self._window.delItem(OBJS[tx,ty])
                OBJS[tx,ty] = 0
                self._level[index(tx,ty)] = 0
                self._window.redraw()

class Player (Character):
    def __init__ (self,x,y,window,level):
        Character.__init__(self,'android.gif',x,y,window,level)

    def at_exit (self):
        return (self._y == 0)

class Baddie (Character):
    def __init__ (self,x,y,window,level,player):
        Character.__init__(self,'red.gif',x,y,window,level)
        self._player = player

def lost (window):
    t = Text(Point(WINDOW_WIDTH/2+10,WINDOW_HEIGHT/2+10),'YOU LOST!')
    t.setSize(36)
    t.setTextColor('red')
    t.draw(window)
    window.getKey()
    exit(0)

def won (window):
    t = Text(Point(WINDOW_WIDTH/2+10,WINDOW_HEIGHT/2+10),'YOU WON!')
    t.setSize(36)
    t.setTextColor('red')
    t.draw(window)
    window.getKey()
    exit(0)

# 0 empty
# 1 brick
# 2 ladder
# 3 rope
# 4 gold

def create_level (num):
    screen = []
    screen.extend([1,1,1,1,1,1,1,1,1,1,1,1,2,0,0,0,0,0,0,0,2,1,1,1,1,1,1,1,1,1,1,1,1,1,0])
    screen.extend([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    screen.extend([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,1,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0])
    screen.extend([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1])
    screen.extend([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,1,2,1,0,0,0,1,2,0,1])
    screen.extend([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,2,0,0,0,0,1,1,1,1])
    screen.extend([3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,0,0,0,0,0,0,0,0,0,2,0,0,0,0,3,3,3,3])
    screen.extend([2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0])
    screen.extend([2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1])
    screen.extend([2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0,0,0,2,3,3,3,3,3,3,3,2])
    screen.extend([2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2])
    screen.extend([2,0,0,0,0,0,3,3,0,0,0,0,0,0,3,3,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2])
    screen.extend([2,0,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,2,1,0,0,0,0,3,3,3,2,0,0,1,1,1,1,1,2])
    screen.extend([2,0,1,0,0,1,0,0,1,0,0,0,0,1,0,0,1,2,1,1,1,1,1,1,0,0,2,0,0,1,0,0,0,1,2])
    screen.extend([2,0,1,4,4,1,0,0,1,0,4,4,4,1,0,0,1,2,0,4,4,4,0,1,0,0,2,0,0,1,4,4,4,1,2])
    screen.extend([2,0,1,1,1,1,0,0,1,2,1,1,1,1,0,0,1,1,1,1,1,1,1,1,0,0,2,0,0,1,1,1,1,1,2])
    screen.extend([2,0,3,3,3,3,3,3,3,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,3,3,3,3,3,3,3,2])
    screen.extend([1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,1])
    screen.extend([1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,2,0,0,0,0,0,0,0,1])
    screen.extend([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
    return screen

def create_screen (level,window):
    global GOLD
    brick = 'brick.gif'
    ladder = 'ladder.gif'
    rope = 'rope.gif'
    gold = 'gold.gif'

    def image (sx,sy,what):
        return Image(Point(sx+CELL_SIZE/2,sy+CELL_SIZE/2),what)

    for (index,cell) in enumerate(level):
        if cell != 0:
            (sx,sy) = screen_pos_index(index)
            if cell == 1:
                elt = image(sx,sy,brick)
            elif cell == 2:
                elt = image(sx,sy,ladder)
            elif cell == 3:
                elt = image(sx,sy,rope)
            elif cell == 4:
                elt = image(sx,sy,gold)
                GOLD += 1
            elt.draw(window)
            OBJS[sx/24,sy/24] = elt

MOVE = {
    'Left': (-1,0),
    'a' : (-1,0),
    'Right': (1,0),
    'd' : (1,0),
    'Up' : (0,-1),
    'w' : (0,-1),
    'Down' : (0,1),
    's' : (0,1)
}

DIG = {
    'z' : (-1,1),
    'x' : (1,1)
}

def main ():
    window = GraphWin("Maze", WINDOW_WIDTH+20, WINDOW_HEIGHT+20, autoflush=False)

    rect = Rectangle(Point(5,5),Point(WINDOW_WIDTH+15,WINDOW_HEIGHT+15))
    rect.setFill('sienna')
    rect.setOutline('sienna')
    rect.draw(window)
    rect = Rectangle(Point(10,10),Point(WINDOW_WIDTH+10,WINDOW_HEIGHT+10))
    rect.setFill('white')
    rect.setOutline('white')
    rect.draw(window)

    level = create_level(1)

    screen = create_screen(level,window)

    p = Player(17,18,window,level)

    baddie1 = Baddie(18,2,window,level,p)
    baddie2 = Baddie(18,7,window,level,p)
    baddie3 = Baddie(23,18,window,level,p)

    while not p.at_exit():
        key = window.checkKey()
        if key == 'q':
            window.close()
            exit(0)
        if key in MOVE:
            (dx,dy) = MOVE[key]
            p.move(dx,dy)
        if key in DIG:
            (dx,dy) = DIG[key]
            p.dig(dx,dy)
        # baddies should probably move here

    won(window)

if __name__ == '__main__':
    main()

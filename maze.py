#
# MAZE
# 
# Example game
#
# Version without baddies running around
#

from graphics import *
import time

LEVEL_WIDTH = 35
LEVEL_HEIGHT = 20

CELL_SIZE = 24
WINDOW_WIDTH = CELL_SIZE*LEVEL_WIDTH
WINDOW_HEIGHT = CELL_SIZE*LEVEL_HEIGHT

OBJS = {}
GOLD = 0
BADDIE_DELAY = 1
BLOCK_DELAY = 5
TIME = time.time()

def screen_pos (x,y):
    return (x*CELL_SIZE+10,y*CELL_SIZE+10)

def screen_pos_index (index):
    x = index % LEVEL_WIDTH
    y = (index - x) / LEVEL_WIDTH
    return screen_pos(x,y)

def index (x,y):
    return x + (y*LEVEL_WIDTH)

def win (level,window,p):
    for i in range(19):
        if level[index(34,i)] == 0:
            level[index(34,i)] = 2
            (sx,sy) = screen_pos_index(index(34,i))
            elt = Image(Point(sx+CELL_SIZE/2,sy+CELL_SIZE/2),'ladder.gif')
            elt.draw(window)
            OBJS[34,i] = elt
        else:
            (sx,sy) = screen_pos(p._x,p._y)
            p._window.delItem(p._img)
            p._img = Image(Point(sx+CELL_SIZE/2,sy+CELL_SIZE/2+2),'t_android.gif')
            p._img.draw(window)
            p._window.redraw()
            break

class Character (object):
    def __init__ (self,pic,x,y,window,level):
        (sx,sy) = x,y
        self._img = Image(Point(sx+CELL_SIZE/2,sy+CELL_SIZE/2+2),pic)
        self._window = window
        self._img.draw(window)
        self._x = (x-10)/CELL_SIZE
        self._y = (y-10)/CELL_SIZE
        self._level = level
        self._level[index(self._x,self._y)] = 0

    def is_baddie (self):
        return False

    def same_loc (self,x,y):
        return (self._x == x and self._y == y)

    def move (self,dx,dy):
        global GOLD
        tx = self._x + dx
        ty = self._y + dy
        if tx >= 0 and ty >= 0 and tx < LEVEL_WIDTH and ty < LEVEL_HEIGHT:
            if self._level[index(self._x,self._y)] == 1:
                if not self.is_baddie():
                    lost(self._window)
                return
            if dy == -1 and self._level[index(tx,ty)] == 3 and self._level[index(tx,ty)] == 1:
                pass
            else:
                if self._level[index(tx,ty)] != 1:
                    self._x = tx
                    self._y = ty
                    self._img.move(dx*CELL_SIZE,dy*CELL_SIZE)
                    # logic for ladders and rope and falling
                    if ty != 19:
                        if self._level[index(tx,ty)] == 0 and self._level[index(tx,ty+1)] != 1:
                            if self._level[index(tx,ty+1)] != 2:
                                self.move(0,1)
                    # logic for picking up gold
                    if self._level[index(tx,ty)] == 4 and not self.is_baddie():
                            GOLD -= 1
                            self._window.delItem(OBJS[self._x,self._y])
                            OBJS[self._x,self._y] = 0
                            self._level[index(tx,ty)] = 0
                            self._window.redraw()

    def dig (self,dx,dy,q):
        tx = self._x + dx
        ty = self._y + dy     
        if tx >= 0 and ty >= 0 and tx < LEVEL_WIDTH and ty < LEVEL_HEIGHT:
            if self._level[index(tx,ty)] == 1 and self._level[index(tx,ty-1)] == 0:
                q.enqueue(BLOCK_DELAY,OBJS[tx,ty])
                self._window.delItem(OBJS[tx,ty]._img)
                self._level[index(tx,ty)] = 0
                self._window.redraw()

class Player (Character):
    def __init__ (self,x,y,window,level):
        Character.__init__(self,'t_android.gif',x,y,window,level)

    def at_exit (self):
        return (self._y == 0)

class Baddie (Character):
    def __init__ (self,x,y,window,level,player):
        Character.__init__(self,'t_red.gif',x,y,window,level)
        self._player = player

    def is_baddie (self):
        return True

    def event (self,q):
        p = self._player
        if self._x < p._x:
            self.move(1,0)
        elif self._x > p._x:
            self.move(-1,0)
        elif self._y < p._y:
            self.move(0,1)
        elif self._y > p._y:
            self.move(0,-1)
        else:
            self.move(1,0)
        q.enqueue(BADDIE_DELAY,self)

class Brick (object):
    def __init__ (self,pic,x,y,window,level):
        (sx,sy) = x,y
        self._pic = pic
        self._img = Image(Point(sx+CELL_SIZE/2,sy+CELL_SIZE/2+2),pic)
        self._window = window
        self._img.draw(window)
        self._x = x
        self._y = y
        self._level = level

    def event (self,q):
        self._img = Image(Point(self._x+CELL_SIZE/2,self._y+CELL_SIZE/2+2),self._pic)
        self._img.draw(self._window)
        self._window.redraw()
        self._level[index((self._x-10)/CELL_SIZE,(self._y-10)/CELL_SIZE)] = 1

class Queue (object):
    def __init__ (self):
        self.queue = []

    def enqueue (self,when,obj):
        self.queue.append([when,obj])

    def dequeue_if_ready (self):
        global TIME
        if time.time() - TIME >= .5:
            TIME = time.time()
            for obj in self.queue:
                if obj[0] == 0:
                    obj[1].event(self)
                    self.queue.remove(obj)
                else:
                    obj[0] -= 1

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
# 5 player
# 6 baddie

def read_level (num):
    screen = open('Levels/level' + str(num) + '.txt')
    lines = []
    for line in screen:
        for ch in line:
            if ch != '\n':
                ch = int(ch)
                lines.append(ch)
    return lines

def create_screen (level,window):
    global GOLD
    brick = 'brick.gif'
    ladder = 'ladder.gif'
    rope = 'rope.gif'
    gold = 'gold.gif'
    android = 't_android.gif'
    red = 't_red.gif'
    bcords = []

    def image (sx,sy,what):
        return Image(Point(sx+CELL_SIZE/2,sy+CELL_SIZE/2),what)

    for (index,cell) in enumerate(level):
        if cell != 0:
            (sx,sy) = screen_pos_index(index)
            if cell == 1:
                brk = Brick(brick,sx,sy,window,level)
                # elt = image(brk._x,brk._y,brick)
                OBJS[sx/24,sy/24] = brk
            elif cell == 2:
                elt = image(sx,sy,ladder)
            elif cell == 3:
                elt = image(sx,sy,rope)
            elif cell == 4:
                elt = image(sx,sy,gold)
                GOLD += 1
            elif cell == 5:
                pcords = (sx,sy)
            elif cell == 6:
                bcords.append((sx,sy))
                # elt = image(sx,sy,red)
                # Baddie(18,2,window,level,p)
            if cell != 1 and cell != 5 and cell != 6:
                elt.draw(window)
                OBJS[sx/24,sy/24] = elt

    return pcords,bcords

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
    num = raw_input('Which level?')

    window = GraphWin("Maze", WINDOW_WIDTH+20, WINDOW_HEIGHT+20, autoflush=False)

    rect = Rectangle(Point(5,5),Point(WINDOW_WIDTH+15,WINDOW_HEIGHT+15))
    rect.setFill('sienna')
    rect.setOutline('sienna')
    rect.draw(window)
    rect = Rectangle(Point(10,10),Point(WINDOW_WIDTH+10,WINDOW_HEIGHT+10))
    rect.setFill('white')
    rect.setOutline('white')
    rect.draw(window)

    q = Queue()
    b= []

    level = read_level(num)

    pcords,bcords = create_screen(level,window)

    p = Player(pcords[0],pcords[1],window,level)

    for cord in bcords:
        b.append(Baddie(cord[0],cord[1],window,level,p))

    for bad in b:
        q.enqueue(BADDIE_DELAY,bad)

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
            p.dig(dx,dy,q)
        if GOLD == 0:
            win(p._level,p._window,p)
        for bad in b:
            if bad._x == p._x and bad._y == p._y:
                lost(p._window)
        q.dequeue_if_ready()

    won(window)

if __name__ == '__main__':
    main()

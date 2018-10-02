#################################################################
# Title: Donut Volleyball                                             
# Programmer: Andrew Wang                                 
# Last Modified: 26/1/2018                                     
# Description: Simple and Fun Volleyball Game   
#################################################################

# Setting up modules
from tkinter import *
from time import *
from random import *
from math import *
from rainbow import *

myInterface = Tk()
s = Canvas( myInterface, width=1200, height=600, background="white" )
s.pack()


# TURN THIS ON IF YOU WOULD LIKE A BACKGROUND IMAGE
#s.create_image(600, 0, image=pImage1, anchor=N)

# PLayer Objects
class Player:
    def __init__(self, p, x, y, c, n):
        self.p = p # Player Number
        self.name = n
        self.side = "left" if p == 1 else "right"
        self.x = x # Position
        self.y = y
        self.colour = c
        self.velX = 0 # Velocity
        self.velY = 0
        self.width = 60 # Size
        self.height = 60
        self.mega = 20 # Size of Paddle
        self.speed = 2.5
        self.jump = 16
        self.megajump = 22
        self.grounded = False
        self.shrink = 0
        self.hue = randint(1, 255) / 255
        self.rainbow = c == "red"
        self.crown = False
        #self.body = s.create_oval(self.x-self.width, self.y-self.height, self.x+self.width, self.y+self.height, fill = "blue", outline = "black", width = 3)
        self.paddle = 0

    def move(self, x, y):
        # Useless function
        #s.move(self.body, x, y)
        if self.paddle:
            s.move(self.paddle, x, y)
        self.x += x
        self.y += y

    def set(self, x, y):
        # Useless function
        #s.move(self.body, x - self.x, y - self.y)
        if self.paddle:
            s.move(self.paddle, x - self.x, y - self.y)
        self.x = x
        self.y = y

    def puff(self):
        # Puffing up the donut
        self.width += self.mega
        self.height += self.mega

        # Puffing frame-perfect on the landing
        if self.y + self.height >= ground and self.grounded == False:
            self.velY = -self.megajump
            if not ball.winner:
                display.text("Mega Jump!", self.side)

        # Puffing in mid-air nest to a wall
        if self.x - self.width <= leftWall and self.grounded == False:
            self.velX = self.megajump
            self.velY = -self.jump
            if not ball.winner:
                display.text("Wall Jump!", self.side)
        if self.x + self.width >= rightWall and self.grounded == False:
            self.velX = -self.megajump
            self.velY = -self.jump
            if not ball.winner:
                display.text("Wall Jump!", self.side)
            
    def update(self):
        # Updates Player
        #dels.append(s.create_polygon(self.x-self.width, self.y-self.height, self.x+self.width, self.y-self.height, self.x+self.width, self.y+self.height, self.x, self.y+self.height, self.x-self.width, self.y+self.height, fill = "blue", outline = "black", width = 3, smooth=True))
        
        # Draws Player
        if self.shrink > 0:
            dels.append(s.create_oval(self.x-self.width, self.y-self.height, self.x+self.width, self.y+self.height, fill = "orange", outline = "black", width = 3))
            dels.append(s.create_oval(self.x-self.width+self.mega, self.y-self.height+self.mega, self.x+self.width-self.mega, self.y+self.height-self.mega, fill = self.colour, outline = "black", width = 3))
            dels.append(s.create_oval(self.x-30, self.y-30, self.x+30, self.y+30, fill = "white", outline = "black", width = 3))
            angle = atan2(ball.y-self.y, ball.x-self.x) # Player to the Ball
            tempx = cos(angle) * 10 + self.x
            tempy = sin(angle) * 10 + self.y
            dels.append(s.create_oval(tempx-15, tempy-15, tempx+15, tempy+15, fill = "black", outline = "black", width = 3))
        else:
            dels.append(s.create_oval(self.x-self.width, self.y-self.height, self.x+self.width, self.y+self.height, fill = self.colour, outline = "black", width = 3))
            dels.append(s.create_oval(self.x-30, self.y-30, self.x+30, self.y+30, fill = "white", outline = "black", width = 3))
            angle = atan2(ball.y-self.y, ball.x-self.x) # Player to the Ball
            tempx = cos(angle) * 10 + self.x
            tempy = sin(angle) * 10 + self.y
            dels.append(s.create_oval(tempx-15, tempy-15, tempx+15, tempy+15, fill = "black", outline = "black", width = 3))
        
        if self.rainbow:
            self.hue += 3/255
            self.colour = getRainbow(self.hue)
        if self.crown:
            dels.append(s.create_polygon(self.x, self.y-self.height-30, self.x+30, self.y-self.height, self.x+60, self.y-self.height-30, self.x+45, self.y-self.height+30, self.x-45, self.y-self.height+30, self.x-60, self.y-self.height-30, self.x-30, self.y-self.height, fill = "yellow", outline = "gold", width = 3))
        
        self.move(self.velX, self.velY)
        self.velX *= friction
    
        if self.y + self.height >= ground:
            self.set(self.x, ground - self.height)
            self.velY = 0
            self.grounded = True
        if self.x - self.width <= leftWall:
            self.set(leftWall + self.width, self.y)
            self.velX = 0
        if self.x + self.width >= rightWall:
            self.set(rightWall - self.width, self.y)
            self.velX = 0
        if self.x - self.width <= 600+netWidth and self.p == 2:
            self.set(600+netWidth + self.width, self.y)
            self.velX = 0
        if self.x + self.width >= 600-netWidth and self.p == 1:
            self.set(600-netWidth - self.width, self.y)
            self.velX = 0

        if not self.grounded:
            self.velY += gravity

        if self.shrink > 0:
            if self.shrink == 1:
                self.width -= self.mega
                self.height -= self.mega       
                self.grounded = False
        self.shrink -= 1

# The game ball
class Ball:
    def __init__(self, t, x, y, r):
        self.t = t # Ball type (If I choose to make more balls)
        self.x = x
        self.y = y
        self.velX = uniform(-5, 5)
        self.velY = -20
        self.radius = r
        self.winner = 0
        self.aftertimer = 50
        self.lastHit = 0

    def reset(self, x):
        self.winner = 0
        self.aftertimer = 50
        self.x = x
        self.y = 300
        self.velX = 0
        self.velY = -20
        self.lastHit = 0

    def collide(self, player):
        # Checks for Player-Ball collisions
        angle = atan2(self.y-player.y, self.x-player.x) # Angle of player to the ball
        length = sqrt((cos(angle) * player.width)**2 + (sin(angle) * player.height)**2) # Works for ovals as well
        distance = sqrt((self.x-player.x)**2 + (self.y-player.y)**2)
        if distance <= length + self.radius: # Checks if the player is touching the ball
            a = atan2(self.velY, self.velX) # The direction the ball is moving
            direction = (angle + (angle - a)) + pi # The new direction the ball is moving
            if 180-abs(degrees(a)-degrees(angle)) < 90: # Checks if the ball is moving towards the player
                self.lastHit = player # The player to last hit the ball
                force = sqrt(self.velX**2 + self.velY**2)
                self.x = cos(angle) * (length + self.radius) + player.x
                self.y = sin(angle) * (length + self.radius) + player.y
                self.velX = cos(direction) * force * 1
                if degrees(direction) > 0:
                    if not self.winner:
                        display.text("Spike!", player.side)
                    self.velY = sin(direction) * force
                else:
                    self.velY = -abs(self.velY)

    def netCheck(self):
        # Ball lands on hits top or corner
        # Checks for Player-Ball collisions
        angle = atan2(self.y-netHeight, self.x-600)
        length = netWidth
        distance = sqrt((self.x-600)**2 + (self.y-netHeight)**2)
        if distance <= length + self.radius:
            a = atan2(self.velY, self.velX)
            direction = (angle + (angle - a)) + pi
            if 180-abs(degrees(a)-degrees(angle)) < 90: # Checks if the ball is moving towards the net
                force = sqrt(self.velX**2 + self.velY**2)
                self.x = cos(angle) * (length + self.radius) + 600
                self.y = sin(angle) * (length + self.radius) + netHeight
                self.velX = cos(direction) * force * 1
                self.velY = sin(direction) * force * 1 #abs(self.velY) if degrees(direction) > 0 else -abs(self.velY)
                self.cancon = 3
        # Ball hits side
        horizontal = abs(self.x-600) < self.radius + netWidth
        if self.y > netHeight and self.velX < 0 and horizontal and self.x - self.velX > 600:
            self.x = 600+netWidth + self.radius
            self.velX = abs(self.velX)
        if self.y > netHeight and self.velX > 0 and horizontal and self.x - self.velX < 600:
            self.x = 600-netWidth - self.radius
            self.velX = -abs(self.velX)
    
    def groundCheck(self):
        # Gives a short delay before starting a new round
        if self.winner:
            n = 20
            size = (600-netWidth-leftWall) / n
            # Display cool spikes
            for spike in range(n):
                tempx = size * (spike + 0.5) + (600+netWidth if self.winner == 1 else leftWall)
                dels.append(s.create_polygon(tempx, ground-size, tempx+size/2, ground, tempx-size/2, ground, fill = "red", outline = "tomato", width = 3))

            self.aftertimer -= 1
            if self.aftertimer == 0:
                resetRound(self.winner)

        # Sets score and displays text when a player scores
        if self.y + self.radius >= ground and not self.winner: # If ball hit the ground and nobody has scored yet
            if self.x < 600:
                display.score[1] += 1
                if display.score[1] >= scoreGoal:
                    # A player has won
                    self.aftertimer += 250
                    display.text(player2.name + " Wins", "main")
                    player2.crown = True
                else:
                    display.text(player2.name + " Scores", "main")
                self.winner = 2
                if self.lastHit == 0:
                    display.text("Epic Fail!", "left")
            else:
                display.score[0] += 1
                if display.score[0] >= scoreGoal:
                    # A player has won
                    self.aftertimer += 250
                    display.text(player1.name + " Wins", "main")
                    player1.crown = True
                else:
                    display.text(player1.name + " Scores", "main")
                self.winner = 1
                if self.lastHit == 0:
                    display.text("Epic Fail!", "right")
                

    def update(self):
        # Update Function for the Ball
        dels.append(s.create_oval(self.x-self.radius, min(self.y, ground - self.radius)-self.radius, self.x+self.radius, min(self.y, ground - self.radius)+self.radius, fill = "red", outline = "black", width = 3))

        self.x += self.velX
        self.y += self.velY

        self.velX *= 0.995
        self.velY *= 0.995

        if self.x - self.radius <= leftWall:
            self.x = leftWall + self.radius
            self.velX = -self.velX
        if self.x + self.radius >= rightWall:
            self.x = rightWall - self.radius
            self.velX = -self.velX

        if self.y - self.radius <= 0:
            display.text("High Ball!", self.lastHit.side)
        if self.y + self.radius >= ground:
            self.y = ground - self.radius
            self.velY = -self.velY
        else:
            self.velY += gravity

        self.netCheck()
        self.groundCheck()
        self.collide(player1)
        self.collide(player2)

# GUI for text and score keeping
class Display:
    def __init__(self):
        self.t = {"main": ["", 0], "left": ["", 0], "right": ["", 0]}
        self.score = [0, 0]

    def text(self, s, t):
        # Sets display object to display a certain text for a short period of time
        self.t[t][0] = s
        self.t[t][1] = 50

    def update(self):
        # Updates display
        string = self.t["main"][0]
        dels.append(s.create_text(600, 200, font=("MS Sans Serif", 80, "bold"), text=string, fill=player1.colour if ball.winner == 1 else player2.colour))

        string = self.t["left"][0]
        dels.append(s.create_text(300, 100, font=("MS Sans Serif", 20, "bold"), text=string, fill=player1.colour))
    
        string = self.t["right"][0]
        dels.append(s.create_text(900, 100, font=("MS Sans Serif", 20, "bold"), text=string, fill=player2.colour))

        string = self.score[0]
        dels.append(s.create_text(150, 100, font=("MS Sans Serif", 80, "bold"), text=string, fill=player1.colour))
        string = self.score[1]
        dels.append(s.create_text(1050, 100, font=("MS Sans Serif", 80, "bold"), text=string, fill=player2.colour))

        for t in ["main", "left", "right"]:
            if self.t[t][1]:
                if self.t[t][1] == 1:
                    self.t[t][0] = ""
                self.t[t][1] -= 1
        
def resetRound(winner):
    # Resets players and the ball in position to start a new round
    global gameOn
    # Used for debugging
    player1.set(300, 440)
    player2.set(900, 440)
    if winner == 1:
        ball.reset(300)
    elif winner == 2:
        ball.reset(900)
    else:
        ball.reset(300)

    if display.score[0] >= scoreGoal:
        gameOn = False
    elif display.score[1] >= scoreGoal:
        gameOn = False

def click(event):
    # Used for debugging
    if not gameOn:
        runGame()

# Creating my own KEYDOWN event
def keyP(event):
    # Adds key to array when a player starts pressing a key
    if event.keycode not in keys: keys.append(event.keycode)

def keyR(event):
    # Deletes key from array when a player lets go of a key
    while event.keycode in keys: keys.remove(event.keycode)

def controls():
    # Runs every frame to check if certain keys are down
    if 87 in keys or 852087 in keys: # 87
        # JUMP
        if player1.grounded:
            player1.velY -= player1.jump
            player1.grounded = False
    if 65 in keys or 97 in keys:
        # SLIDE TO THE LEFT
        player1.velX -= player1.speed
    if 83 in keys or 65651 in keys:
        # PUFF UP
        if player1.shrink < -30:
            player1.shrink = 5
            player1.puff()
    if 68 in keys or 131172 in keys:
        # SLIDE TO THE RIGHT
        player1.velX += player1.speed
        
    if 73 in keys or 2228329 in keys:
        # JUMP
        if player2.grounded:
            player2.velY -= player2.jump
            player2.grounded = False
    if 74 in keys or 2490474 in keys:
        # SLIDE TO THE LEFT
        player2.velX -= player2.speed
    if 75 in keys or 2621547 in keys:
        # PUFF UP
        if player2.shrink < -30:
            player2.shrink = 5
            player2.puff()
    if 76 in keys or 2424940 in keys:
        # SLIDE TO THE RIGHT
        player2.velX += player2.speed

# Bind keyboard controls
s.bind("<Any-KeyPress>", keyP)
s.bind("<Any-KeyRelease>", keyR)
s.bind("<Button-1>", click)
s.focus_set()

gameOn = False
player1 = Player(1, 300, 440, "darkblue", "Blueberry Donut")
player2 = Player(2, 900, 440, "deeppink", "Jelly Donut")
ball = Ball("red", 600, 300, 20)
scoreGoal = 3
display = Display()
gravity = 1
friction = 0.8
ground = 500
leftWall = 50
rightWall = 1150
netWidth = 10
netHeight = 350
dels = []
keys = []

def runGame():
    global gameOn,player1,player2,ball,scoreGoal,display,gravity,friction,ground,leftWall,rightWall,netWidth,netHeight,dels,keys
    # Defining global varibles
    colours = [["darkblue", "Blueberry Donut"], ["deeppink", "Jelly Donut"], ["limegreen", "Lime Donut"], ["orange", "Orange Donut"], ["red", "Rainbow Donut"]]

    gameOn = True
    ppp1 = choice(colours)
    ppp2 = choice(colours)
    player1 = Player(1, 300, 440, ppp1[0], ppp1[1])
    player2 = Player(2, 900, 440, ppp2[0], ppp2[1])
    ball = Ball("red", 600, 300, 20)
    scoreGoal = 7
    display = Display()
    gravity = 1
    friction = 0.8
    ground = 500
    leftWall = 50
    rightWall = 1150
    netWidth = 10
    netHeight = 350
    dels = []
    keys = []

    # Setting static tkinter objects
    f = 0
    static = []
    static.append(s.create_rectangle(0, 0, 1200, 600, fill = "white", outline = "white", width = 3))
    static.append(s.create_rectangle(0, ground, 1200, 600, fill = "gray", outline = "gray", width = 3))
    static.append(s.create_rectangle(600-netWidth, netHeight, 600+netWidth, ground, fill = "yellow", outline = "gray", width = 3))
    static.append(s.create_rectangle(0, 0, leftWall, ground, fill = "gray", outline = "gray", width = 3))
    static.append(s.create_rectangle(rightWall, 0, 1200, ground, fill = "gray", outline = "gray", width = 3))
    resetRound(0)
    
    # Where the game loop is ran
    while gameOn:
        f+=1
        controls()
        player1.update()
        player2.update()
        ball.update()
        display.update()
        s.update()
        sleep(0.03)

        # Important! Deletes tkinter objects from canvas and memory
        for de in dels:
            s.delete(de)
        del dels[:] # Missing this line will slow the game down as time progresses

    # Deleting static tkinter objects after game ends to save space
    for de in static:
        s.delete(de)
    del static[:]

# LOADING SCREEN

class TitleL:
    def __init__(self, x, y, letter, c1, c2):
        self.x = x
        self.y = y
        self.k = y
        self.b = x/15
        self.c1 = c1
        self.c2 = c2
        self.text = letter
        self.offset = 0
        
    def update(self, f):
        self.y = 20*sin(0.1*(f+self.b)) + self.k
        dels.append(s.create_text(self.x-self.offset, self.y-self.offset, font=("Arial Black", 75, "bold"), text=self.text, fill=self.c2, anchor=W))
        dels.append(s.create_text(self.x, self.y, font=("Arial", 75, "bold"), text=self.text, fill=self.c1, anchor=W))

class PlayL:
    def __init__(self, x, y, letter, c1, c2):
        self.x = x
        self.y = y
        self.k = 150
        self.b = x/15
        self.c1 = c1
        self.c2 = c2
        self.text = letter
        self.offset = 0
        
    def update(self, f):
        size = 25*sin(0.08*(f+self.b)) + self.k
        dels.append(s.create_text(self.x-self.offset, self.y-self.offset, font=("Arial Black", int(size), "bold"), text=self.text, fill=self.c2, anchor=W))
        dels.append(s.create_text(self.x, self.y, font=("Arial", int(size), "bold"), text=self.text, fill=self.c1, anchor=W))

title = [TitleL(180, 150, "D", getRainbow(random()), "gray80")]

k = 250
for n, l in enumerate("onut Volleyball"):
    title.append(TitleL(k, 150, l, getRainbow(random()), "gray80"))
    if l in "ilj1":
        k += 30
    else:
        k += 60

play = [PlayL(420, 350, "P", getRainbow(random()), "gray80")]

k = 536
for n, l in enumerate("lay"):
    play.append(PlayL(k, 350, l, getRainbow(random()), "gray80"))
    if l in "ilj1":
        k += 48
    else:
        k += 96

##hue = 0
##x = 0
##speed = 0.4
##while x < 1250:
##    hue += speed/255
##    x += 1
##    col = getRainbow(hue)
##    s.create_line(x, -50, x, 650, fill=col)
##s.update()

##s.create_rectangle(500, 250, 700, 350, fill="lightblue", outline="white", width=10)
##s.create_text(600, 300, font=("MS Sans Serif", 50, "bold"), text="Play", fill="black")

dels = []
f = 0

s.create_text(200, 300, font=("Arial", 30, "bold"), text="Player 1", fill="black", anchor=N)
s.create_text(200, 400, font=("Arial", 30, "bold"), text="WASD KEYS", fill=getRainbow(random()), anchor=N)
s.create_text(1000, 300, font=("Arial", 30, "bold"), text="Player 2", fill="black", anchor=N)
s.create_text(1000, 400, font=("Arial", 30, "bold"), text="IJKL KEYS", fill=getRainbow(random()), anchor=N)
while True:
    f += 1

    for l in title+play:
        l.update(f)

    s.update()
    sleep(0.001)
    for d in dels:
        s.delete(d)
    del dels[:]

myInterface.mainloop()

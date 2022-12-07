import pygame as game
import random as r
from pygame.time import Clock
import time as t

#AG = Adam Garces, #SN = Samantha Neufeld 

game.init()

#SN if you are using sound you need this
game.mixer.pre_init(44100, -16, 2, 2048)
game.mixer.init()
game.mixer.music.load("bgmusic.mp3")
bling = game.mixer.Sound("bling.wav")
countdown = game.mixer.Sound("countdown.wav")
gameover1 = game.mixer.Sound("gameover.wav")

game.display.set_caption("Evade") 
screen = game.display.set_mode([800, 600])
bgcolor = game.color.Color("#6071a8")

##=== PRE DEFINED VARIABLES AND IMAGES ===## #SN

gameon = True
space = game.image.load("space.png")
click = game.image.load("click.png")
evade = game.image.load("evade2.png")
gameover = game.image.load("gameover.png")
black = game.color.Color("black")
white = game.color.Color("white")
clock = Clock()
timer = 0
img3 = game.image.load("3.png")
img2 = game.image.load("2.png")
img1 = game.image.load("1.png")
score = 0

# STAR #SN
star = game.image.load("star3.png")
star = game.transform.scale(star, (45, 30))
# use for star2 || star = game.transform.scale(star,(30,25)) 
stars = 0
starbox = star.get_rect()
starbox.x = r.randint(20, 780)
starbox.y = r.randint(20, 580)


# SHIP player sprite #SN #AG
ship = game.image.load("ship1.png")
rect = ship.get_rect()
rect = rect.inflate(-30, -30)
rect.x = 400
rect.y = 400
red = game.color.Color("red")
shipdir = 0
newship = ship
auto = False


# ENEMY vectors and movement #AG
vec = game.math.Vector2
pos = vec(10, 10)
end = vec(300, 125)
move = end - pos
move = move / 100
boxes = []
speed = 400
spawnrate = 800


def starspawn(): #place star in game # AG
    starbox.x = r.randint(20, 780)
    starbox.y = r.randint(20, 580)


def spawn(): #enemy spawn function determine spawn location and direction #AG
    global rect, mx, my, pos
    end = vec(rect.left, rect.top)
    dir = r.randint(1, 4)
    if rect.x >= 700:  # close to right side
        if dir == 1:  # from left
            pos = vec(-20, r.randint(100, 500))
        # elif dir==2: #from right
            #pos = vec(820, r.randint(100,500))
        elif dir == 3:  # from top
            pos = vec(r.randint(100, 700), -20)
        elif dir == 4:  # from bottom
            pos = vec(r.randint(100, 700), 620)
    elif rect.x <= 100:  # close to left side
        # if dir==1: #from left
        #pos = vec(-20, r.randint(100,500))
        if dir == 2:  # from right
            pos = vec(820, r.randint(100, 500))
        elif dir == 3:  # from top
            pos = vec(r.randint(100, 700), -20)
        elif dir == 4:  # from bottom
            pos = vec(r.randint(100, 700), 620)
    elif rect.y >= 500:  # close to bottom
        if dir == 1:  # from right
            pos = vec(-20, r.randint(100, 500))
        elif dir == 2:  # from left
            pos = vec(820, r.randint(100, 500))
        elif dir == 3:  # from top
            pos = vec(r.randint(100, 700), -20)
        # elif dir==4: #from bottom
            #pos = vec(r.randint(100,700), 620)
    elif rect.y <= 100:  # close to top
        if dir == 1:  # from left
            pos = vec(-20, r.randint(100, 500))
        elif dir == 2:  # from right
            pos = vec(820, r.randint(100, 500))
        # elif dir==3: #from top
            #pos = vec(r.randint(100,700), -20)
        elif dir == 4:  # from bottom
            pos = vec(r.randint(100, 700), 620)
    else:
        if dir == 1:  # from left
            pos = vec(-20, r.randint(100, 500))
        elif dir == 2:  # from right
            pos = vec(820, r.randint(100, 500))
        elif dir == 3:  # from top
            pos = vec(r.randint(100, 700), -20)
        elif dir == 4:  # from bottom
            pos = vec(r.randint(100, 700), 620)

    move = end - pos
    move = move / speed
    boxes.append([pos, move]) #add box to game list


def rotateship(shipdir): #rotation ship image while moving #SN 
    newship = game.transform.rotate(ship, shipdir)
    newrect = rect.copy()
    newrect.center = newship.get_rect().center
    return newship.subsurface(newrect).copy()


def getmove(): #AG 
    # returns x-y movement based on directrion facing
    # see direction_map.png for details
    global shipdir
    d = shipdir
    if d >= 349 or d < 11:
        return [0, -2]
    elif d >= 11 and d < 34:
        return [-1, -2]
    elif d >= 34 and d < 56:
        return [-2, -2]
    elif d >= 56 and d < 79:
        return [-2, -1]
    elif d >= 79 and d < 102:
        return [-2, 0]
    elif d >= 102 and d < 125:
        return [-2, 1]
    elif d >= 125 and d < 147:
        return [-2, 2]
    elif d >= 147 and d < 170:
        return [-1, 2]
    elif d >= 170 and d < 191:
        return [0, 2]
    elif d >= 191 and d < 214:
        return [1, 2]
    elif d >= 214 and d < 237:
        return [2, 2]
    elif d >= 237 and d < 260:
        return [2, 1]
    elif d >= 260 and d < 282:
        return [2, 0]
    elif d >= 282 and d < 305:
        return [2, -1]
    elif d >= 305 and d < 328:
        return [2, -2]
    elif d >= 328 and d < 349:
        return [1, -2]


# EVENTS AND TEXT #SN

SPAWNENEMY = 10  # interval for enemy spawn
CLOCK = 11


game.time.set_timer(SPAWNENEMY, spawnrate)
game.time.set_timer(CLOCK, 1000)

font = game.font.Font(None, 20)
bigfont = game.font.Font(None, 50)
timetext = font.render("Time: 0", 0, black)
endtimetext = font.render("You survived for % seconds!", 0, black)
scoretext = font.render("Score: 0", 0, white)
startext = bigfont.render("Stars: 0", 0, white)


##===============PRE GAME LOOP===============## #SN #AG

while True: #pre game screen 
    screen.fill(bgcolor)
    screen.blit(space, (0, 0))
    screen.blit(click, (110, 350))
    screen.blit(evade, (100, 215))
    game.display.flip()
    event = game.event.poll()  # listens for mouse, keyboard, quitting
    key = game.key.get_pressed()
    if key[game.K_SPACE]:
        break

    if event.type == game.QUIT:
        gameon = False
        game.quit()


while True: #countdown screen
    pass
    if event.type == game.QUIT:
        gameon = False
        game.quit()
    screen.fill(bgcolor)
    screen.blit(space, (0, 0))
    screen.blit(img3, (320, 215))
    game.display.flip()
    countdown.play()
    t.sleep(1)
    screen.blit(space, (0, 0))
    screen.blit(img2, (320, 215))
    game.display.flip()
    t.sleep(1)
    screen.blit(space, (0, 0))
    screen.blit(img1, (335, 215))
    game.display.flip()
    t.sleep(1)
    break


game.mixer.music.play(-1) #starts music
##===================== MAIN GAME LOOP ===========================## ##AG #SN

while gameon:
    

    # GAME DRAWING AND PLACING 
    screen.fill(bgcolor)
    screen.blit(space, (0, 0))
    screen.blit(newship, (rect.x, rect.y))
    screen.blit(timetext, (280, 0))
    screen.blit(scoretext, (420, 0))
    screen.blit(star, (starbox.x, starbox.y))

    for box in boxes:
        game.draw.rect(screen, red, (box[0].x, box[0].y, 15, 15))
        box[0] += box[1]

    game.display.flip()  # redraws / refreshes screen
    event = game.event.poll()  # listens for mouse, keyboard, quitting
    key = game.key.get_pressed()

    auto = True #Allow movement for ship

    if rect.x > 800: #go through wall 
        rect.x = 0
    elif rect.x < 0:
        rect.x = 800
    elif rect.y > 600:
        rect.y = 0
    elif rect.y < 0:
        rect.y = 600

   # KEY DETECTION
    if key[game.K_RIGHT]: #rotate ship right
        if shipdir == 0:
            shipdir = 360
        shipdir -= 1
        newship = rotateship(shipdir)

    if key[game.K_LEFT]: #rotate ship left
        if shipdir == 360:
            shipdir = 0
        shipdir += 1
        newship = rotateship(shipdir)

    if auto == True: #movement/speed of ship
        game.time.delay(2)
        move = getmove()
        rect.x += move[0]
        rect.y += move[1]

    # if auto==True or key[game.K_SPACE]:
        #move = getmove()
        #rect.x += move[0]
        #rect.y += move[1]

    game.time.delay(5) #GAME PACE

# =============================================================================
#     mx, my = game.mouse.get_pos()
#     if event.type == game.MOUSEBUTTONDOWN:
#         spawn()
# =============================================================================

    if event.type == SPAWNENEMY: #spawn enemy according to timer
        spawn()
        game.time.set_timer(SPAWNENEMY, spawnrate)

    if starbox.colliderect(rect): #star collect
        bling.play()
        starspawn()
        score += 100
        stars += 1

    if event.type == CLOCK:

       # print(spawnrate)
        #print(speed)
        timer += 1
        timetext = font.render("Time: %d" % timer, 0, white)
        score += timer*2.5
        scoretext = font.render("Score: %d" % score, 0, white)
        startext = bigfont.render("Stars: %d" % stars, 0, white)

        if spawnrate > 300:  # increasing spawnrate as time progresses
            spawnrate -= 7

        if speed > 150:  # inncreasing speed of enemies as time progresses
            speed -= 2

    for box in boxes: #create hitbox for enemy boxes and test for collision with player
        hitbox = game.rect.Rect(box[0].x, box[0].y, 15, 15)
        if hitbox.colliderect(rect):
            gameon = False
            

    if event.type == game.QUIT:
        gameon = False


gameover1.play()
##==================== END OF MAIN GAME LOOP ===================##
while True: #end music and display endscreen
    game.mixer.music.stop()  
    endtimetext = bigfont.render("Time: %d" % timer, 0, white)
    scoretext = bigfont.render("Score: %d" % score, 0, white)
    startext = bigfont.render("Stars: %d" % stars, 0, white)
    screen.blit(space, (0, 0))
    ship = game.transform.scale(ship, (160, 180))
    screen.blit(ship, (320, 200))
    screen.blit(endtimetext, (160, 300))
    screen.blit(scoretext, (500, 300))
    screen.blit(startext, (325, 400))
    screen.blit(gameover, (85, 75))

    game.display.flip()
    event = game.event.poll()
    if event.type == game.QUIT:
        break

game.quit()

# if gameon==True:
# pass
# if dir==1: #from top
#    pos = vec(-20, r.randint(100,500))
# elif dir==2: #from bottom
#    pos = vec(820, r.randint(100,500))
# elif dir==3: #from left
#    pos = vec(r.randint(100,700), -20)
# elif dir==4: #from right
#    pos = vec(r.randint(100,700), 620)

# https://www4.flamingtext.com/logo/Design-Star-Wars
# https://flamingtext.com/logo/Design-Dance?text=Evade

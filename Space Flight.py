app.stepsPerSecond = 25
app.dx = 1
app.level = 1
ships = []
lasers = Group()
playerLasers = Group()
menu = Group()
img = 'cmu://550703/21981557/milky-way-2695569__480.jpg'
### https://cdn.pixabay.com/photo/2017/08/30/01/05/milky-way-2695569__480.jpg
shipImage = 'cmu://550703/21986666/My+project-1+(1).png'
### https://www.deviantart.com/ibyosl/art/pixel-spaceship-800830035
playerShipImage = 'cmu://550703/21987638/My+project-1+(3).png'
### https://www.pngegg.com/en/png-ykljd
Image (img,-200,0).toBack()
player = Image(playerShipImage,200,350,align = 'center')

player.win = False
player.won = False
player.dead = False

def makeShips(rows,columns):
    for i in range(rows):
        xGap = 400 / (rows + 1)
        x = xGap * (i + 1)
        for k in range (columns):
            yGap = 300 / (columns + 1)
            y = yGap * (k + 1)
            ship = Image(shipImage,x,y,align='center',rotateAngle = 180)
            ships.append(ship)

def moveShips():
    for ship in ships :
        if ship.left < 0 :
            app.dx = 1
        elif ship.right >= 400 :
            app.dx = -1
    for ship in ships :
        ship.centerX += app.dx
    
def shoot(ship):
    if ship in ships :
        laser = Rect(ship.centerX,ship.centerY - 5, 3, 5, fill = 'red',align = 'center')
        laser.toFront()        
        lasers.add(laser)
    else:
        laser = Rect(ship.centerX,ship.centerY + 5, 3, 5 , fill = 'red',align = 'center')
        laser.toFront()
        playerLasers.add(laser)

def enemyShooting(max):
    if (len(ships) > 0) :
        if len(lasers) < max :
            shoot(choice(ships))
    for laser in lasers :
        if laser.centerY > 405 :
            lasers.remove(laser)
        if (laser.hitsShape(player)):
            lasers.remove(laser)
            player.dead = True
        laser.centerY += 8

def playerShooting():
    if len(playerLasers) < 1 :
        shoot(player)
    for laser in playerLasers :
        if (laser.centerY < 0) :
            playerLasers.remove(laser)
        for ship in ships :
            if (laser.hitsShape(ship)):
                ships.remove(ship)
                ship.visible = False
                playerLasers.remove(laser)
        laser.centerY -= 8

def movePlayer(keys):
    if (player.left > 0) :
        if ('left' in keys or 'a' in keys):
            player.centerX -= 5 
    if (player.right < 400) :
        if ('right' in keys or 'd' in keys):
            player.centerX += 5
    if (player.top > 300) :
        if ('up' in keys or 'w' in keys):
            player.centerY -= 5
    if (player.bottom < 400) :
        if ('down' in keys or 's' in keys): 
            player.centerY += 5
    else:
        None

def makeLevel(difficulty):
    lasers.clear()
    for ship in ships:
        ship.visible = False
    ships.clear()
    menu.clear()
    if (difficulty == 'easy'):
        makeShips(5,1)
    elif (difficulty == 'normal'):
        makeShips(5,3)
    elif (difficulty == 'hard'):
        makeShips(5,5)
    else:
        makeShips(5,3)
    player.dead = False
    player.win = False
    player.won =False
    player.centerX = 200
    player.centerY= 350

def playerDeath():
    menu.add(
    Rect(200,200,250,250, fill = 'darkGray', align = 'center'),
    Label('Defeat',200,125, size = 36, font = 'orbitron'),
    Label('You lost at level ' + str(app.level), 200,200, size = 20, font = 'orbitron'),
    Rect(200,265,225,50, fill = 'slateGray', align = 'center'),
    Label('Click anywhere to restart',200,265,size = 14, font = 'orbitron')
    )
    menu.toFront()
    app.level = 1

def playerWin():
    menu.add(
    Rect(200,200,250,250, fill = 'darkGray', align = 'center'),
    Label('Victory',200,125, size = 36, font = 'orbitron'),
    Label('Level ' + str(app.level) + ' completed', 200,200, size = 20, font = 'orbitron'),
    Rect(200,265,225,50, fill = 'slateGray', align = 'center'),
    Label('Click anywhere to proceed', 200, 265, size = 14, font = 'orbitron')
    )
    menu.toFront()
    app.level += 1
    player.won = True
    
difficulty = app.getTextInput('Easy - Normal - Hard').lower()
makeLevel(difficulty)
def onStep():
    if (not player.dead) :
        if (not player.win) :
            moveShips()
            enemyShooting(app.level)
            playerShooting()
            if (len(ships) < 1) :
                    player.win = True
            elif (player.dead == True):
                playerDeath()
    if (player.win == True):
        if (player.won == False):
            playerWin()

def onKeyHold(keys):
    if (not player.dead) :
        if (not player.win) :
            movePlayer(keys)

def onMousePress(mouseX,mouseY):
    if (player.dead or player.win):
        makeLevel(difficulty)
        

    

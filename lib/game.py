from lib.config import *
import pygame
import operator


class Game():
    debugGFX = pygame.image.load('img/UI/debug_bar.png')
    # Create a surface to draw the map on
    mapWindow = pygame.Surface((MU_DISPWIDTH, MU_DISPHEIGHT - UU_DEBUGHEIGHT))
    # Create a surface to draw debug info onto
    debugWindow = pygame.Surface((UU_DEBUGWIDTH, UU_DEBUGHEIGHT))
    # Create a players list
    players = []
    # Create a controllers list
    controllers = []
    # List of map regions to redraw
    redraw = []

    def __init__(self, mapFile):
        print('Building Game()')
        self.map = Map(mapFile)
        print('Done building Game()')

    def debugShow(self):
        fontDebug = pygame.font.Font('img/UI/runescape_uf.ttf', 24)
        # Erase debug screen
        self.debugWindow.fill((0, 0, 0))
        # Draw debug window
        self.debugWindow.blit(self.debugGFX, (0, 0))
        # Draw hitboxes
        # for widget in self.players + self.map.tiles_llw:
        #     pygame.draw.rect(self.mapWindow, (255, 0, 0), widget.hitBox, 2)
        # for widget in self.players:
        #     pygame.draw.rect(self.mapWindow, (0, 0, 255), widget.useBox, 2)
        for player in self.players:
            fontText = fontDebug.render(str(player.x), True, (255, 255, 255))
            self.debugWindow.blit(fontText, (16, 32))
            fontText = fontDebug.render(str(player.y), True, (255, 255, 255))
            self.debugWindow.blit(fontText, (80, 32))
            fontText = fontDebug.render(
                str(player.xMomentum), True, (255, 255, 255))
            self.debugWindow.blit(fontText, (16, 64))
            fontText = fontDebug.render(
                str(player.yMomentum), True, (255, 255, 255))
            self.debugWindow.blit(fontText, (80, 64))
            fontText = fontDebug.render(
                str(self.map.tiles_llw[0].xratio), True, (255, 255, 255))
            self.debugWindow.blit(fontText, (128, 32))
            fontText = fontDebug.render(
                str(self.map.tiles_llw[0].yratio), True, (255, 255, 255))
            self.debugWindow.blit(fontText, (128, 64))

    def stepControllers(self):
        # Go through each controller to get updates
        # Get events once and pass it to each controller
        events = pygame.event.get()
        for i, controller in enumerate(self.controllers):
            controller.update(events, self.players[i])

    def stepTriggers(self):
        # Check for use Triggers
        for player in self.players:
            player.trigger(self.map.tiles_llw + self.players)

    def stepMove(self):
        # Calculate tile physics
        for i, itemPhys in enumerate(self.map.tiles_ll2 + self.map.tiles_llw + self.players):
            itemPhys.physics(itemPhys.xMomentum, 0)
            itemPhys.collide(self.map.tiles_ll2 +
                             self.map.tiles_llw + self.players)
            itemPhys.physics(0, itemPhys.yMomentum)
            itemPhys.collide(self.map.tiles_ll2 +
                             self.map.tiles_llw + self.players)

    def stepShake(self):
        # self.map.tiles_llw.sort(key=operator.attrgetter('y'))
        # Animate everyone
        self.redraw = []
        for widget in self.map.tiles_llw + self.players:
            widget.animator.animate()
            self.redraw.append(pygame.Rect(
                widget.x, widget.y, DEF_WIDGET_W, DEF_WIDGET_H))
        # Erase map screen
        self.mapWindow.fill((0, 0, 0))
        self.allTiles = self.map.tiles_llw + \
            self.map.tiles_ll1 + self.map.tiles_ll2 + self.players
        self.allTiles.sort(key=operator.attrgetter('y'))
        self.layers = 0
        for widget in self.map.tiles_llw + self.players:
            self.widgetRegion = pygame.Rect(
                widget.x, widget.y, DEF_WIDGET_W, DEF_WIDGET_H)
            for tile in self.allTiles:
                self.tileRegion = pygame.Rect(
                    tile.x, tile.y, DEF_WIDGET_W, DEF_WIDGET_H)
                if self.widgetRegion.colliderect(self.tileRegion):
                    tile.redraw = True
        while self.layers <= 2:
            for tile in self.allTiles:
                if tile.layer == self.layers:
                    if tile.redraw:
                        tile.redraw = False
                        self.mapWindow.blit(tile.draw(), (tile.x, tile.y))
            self.layers += 1
        if self.map.freshMap:
            self.redraw = [pygame.Rect(0, 0, MU_DISPWIDTH, MU_DISPHEIGHT)]
            self.map.freshMap = False
        self.redraw.append(pygame.Rect(UU_DEBUGX, UU_DEBUGY,
                                       UU_DEBUGWIDTH, UU_DEBUGHEIGHT))

    def gameLoop(self):

        self.stepControllers()
        self.stepTriggers()
        self.stepMove()
        self.stepShake()

        # Add map hue / fog
        # self.mapWindow.blit(self.map.hueMap((0, 0, 0, 0)), (0, 0))
        self.debugShow()


class Map():
    tiles_ll1 = []
    tiles_ll2 = []
    tiles_llw = []
    mapHue = (0, 0, 0, 0)

    def __init__(self, mapFile):
        print('Building Map()')
        for filetype in list(['ll1', 'll2', 'llw']):
            mapData = open(mapFile + '.' + filetype, "r").readlines()
            for rowIndex, row in enumerate(mapData):
                for colIndex, col in enumerate(mapData[rowIndex]):
                    if filetype == 'll1':
                        if col is '.':
                            self.tiles_ll1.append(
                                Tile('img/tiles/lv1/grass5.png', colIndex * GU_GRID, rowIndex * GU_GRID, GU_GRID,
                                     GU_GRID, 0))  # Grass 5
                    if filetype == 'll2':
                        if col is 'X':
                            self.tiles_ll2.append(
                                Tile('img/tiles/lv2/bush.png', colIndex * GU_GRID, rowIndex * GU_GRID, GU_GRID, GU_GRID,
                                     1))  # Bush
                        if col is '/':
                            self.tiles_ll2.append(
                                Tile('img/tiles/lv2/tree1.png', colIndex * GU_GRID, rowIndex * GU_GRID, GU_GRID,
                                     GU_GRID, 1))  # Tree Trunk Right
                        if col is '\\':
                            self.tiles_ll2.append(
                                Tile('img/tiles/lv2/tree2.png', colIndex * GU_GRID, rowIndex * GU_GRID, GU_GRID,
                                     GU_GRID, 1))  # Trunk Left
                        if col is '(':
                            self.tiles_ll2.append(
                                Tile('img/tiles/lv3/tree4.png', colIndex * GU_GRID, rowIndex * GU_GRID, GU_GRID,
                                     GU_GRID, 2))  # Tree top left
                        if col is ')':
                            self.tiles_ll2.append(
                                Tile('img/tiles/lv3/tree5.png', colIndex * GU_GRID, rowIndex * GU_GRID, GU_GRID,
                                     GU_GRID, 2))  # Tree top right
                    # TODO: Instead of this loop, make the widgets load from a list of widgets in a file
                    if filetype == 'llw':
                        import lib.widgets
                        if col is 'X':
                            self.tiles_llw.append(
                                lib.widgets.W_Bush('bush', colIndex * GU_GRID, rowIndex * GU_GRID, GU_GRID, GU_GRID,
                                                   1))  # Bush
                        if col is 'J':
                            self.tiles_llw.append(
                                lib.widgets.W_Jack('jack', colIndex * GU_GRID, rowIndex * GU_GRID, 32, 48, 1))  # Bush
        print('Done building Map()')
        self.freshMap = True

    def hueMap(self, color):
        # Hue map screen
        self.mapHue = (color[0], color[1], color[2], color[3])
        self.hueSurf = pygame.Surface((MU_DISPWIDTH, MU_DISPHEIGHT))
        self.hueSurf.fill(self.mapHue)
        self.hueSurf.set_alpha(self.mapHue[3])
        return self.hueSurf


class Tile():
    def __init__(self, img, x, y, w, h, layer):
        self.contacting = []
        self.img = pygame.image.load(img)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.xMomentum = self.yMomentum = 0
        self.layer = layer
        self.hitBox = pygame.Rect((self.x, self.y, self.w, self.h))
        self.redraw = True

    def draw(self):
        self.tileSurf = pygame.Surface((self.w, self.h))
        self.tileSurf.fill((254, 1, 1))
        self.tileSurf.set_colorkey((254, 1, 1))
        self.tileSurf.blit(self.img, (0, 0))
        return self.tileSurf

    def physics(self, px, py):
        return

    # TODO: Update with physics from PySmash
    def collide(self, colliders):
        for collider in colliders:
            if collider is not self:
                # If there's any collision at all
                if self.hitBox.colliderect(collider.hitBox):
                    if collider not in self.contacting:
                        self.contacting.append(collider)
                        if collider.layer == self.layer:
                            collider.xMomentum = collider.xMomentum * -0.75
                            collider.yMomentum = collider.yMomentum * -0.75
                else:
                    if collider in self.contacting:
                        self.contacting.remove(collider)


class Widget(Tile):
    xratio = 0.5
    yratio = 0.5

    # widget stuff here
    def __init__(self, animationType, x, y, w, h, layer):
        super().__init__('img/tiles/lv2/bush.png', x, y, w, h, layer)
        # self.gfxCenter = (int(DEF_WIDGET_W / 2), int(DEF_WIDGET_H / 2))
        self.gfxTop = (DEF_WIDGET_H / 2) - (self.h / 2)
        self.gfxLeft = (DEF_WIDGET_W / 2) - (self.w / 2)
        self.hitBox = pygame.Rect(
            (self.x + self.gfxLeft, (self.y + self.gfxTop + self.h) - (self.h / 2), self.w, self.h / 2))
        # self.hitBox = pygame.Rect((self.x + self.gfxLeft, self.y + self.gfxTop, self.w, self.h))
        self.shadow = True
        self.shadowIMG = pygame.image.load('img/tiles/shadow.png')

        self.animator = Animator(animationType)

        self.xMomentum = self.yMomentum = 0
        self.xAccelerate = GP_xACCEL
        self.yAccelerate = GP_yACCEL
        self.xDecelerate = GP_xDECEL
        self.yDecelerate = GP_yDECEL
        self.direction = 'left'
        self.maxRun = 15

    def draw(self):
        self.tileSurf = pygame.Surface(
            (DEF_WIDGET_W, DEF_WIDGET_H), pygame.SRCALPHA)
        # pygame.draw.rect(self.tileSurf, (255, 0, 0), pygame.Rect(
        #     0, 0, DEF_WIDGET_W - 1, DEF_WIDGET_H - 1), 2)
        if self.shadow:
            self.tileSurf.blit(self.shadowIMG, ((
                DEF_WIDGET_W - self.shadowIMG.get_rect().size[0]) / 2,
                self.gfxTop + self.h - (
                self.shadowIMG.get_rect().size[1] / 2)))
        self.tileSurf.blit(self.animator.aniFrame, (self.gfxLeft, self.gfxTop))
        # # Gfx region
        # pygame.draw.rect(self.tileSurf, (255, 0, 255), pygame.Rect(
        #    (0, 0, DEF_WIDGET_W - 1, DEF_WIDGET_H - 1)), 2)
        # # Aggro
        # pygame.draw.circle(
        #    self.tileSurf, (0, 255, 0), self.gfxCenter, 256, 2)
        # # Ranged
        # pygame.draw.circle(
        #    self.tileSurf, (255, 255, 0), self.gfxCenter, 128, 2)
        # # Attack
        # pygame.draw.circle(
        #    self.tileSurf, (255, 128, 0), self.gfxCenter, 64, 2)
        return self.tileSurf

    def activate(self, activator):
        print('Activated ' + str(self))

    def faceWidget(self, source, target):
        # If the difference between the widget X's is greater than the difference between their Y's
        # Then the target must be more left or right of the source
        # Can this be done better?
        if abs(abs(source.x) - abs(target.x)) >= abs(abs(source.y) - abs(target.y)):
            if source.x > target.x:
                # Left of source
                source.direction = 'left'
                source.animator.setDirection('left')
            else:
                # Right of source
                source.direction = 'right'
                source.animator.setDirection('right')
        # Otherwise, the target must be above or below
        else:
            if source.y > target.y:
                # Above source
                source.direction = 'up'
                source.animator.setDirection('up')
            else:
                # Below source
                source.direction = 'down'
                source.animator.setDirection('down')

    def moveToPoint(self, x, y, speed):
        # if abs(self.x - player.x) > abs(self.y - player.y):
        #     self.xratio = abs(self.y - player.y) / abs(self.x - player.x)
        #     self.yratio = 1 - abs(self.y - player.y) / abs(self.x - player.x)
        # elif abs(self.x - player.x) < abs(self.y - player.y):
        #     self.xratio = abs(self.x - player.x) / abs(self.y - player.y)
        #     self.yratio = 1 - abs(self.x - player.x) / abs(self.y - player.y)
        #
        # if self.x > player.x:
        #     self.x -= 2 * self.xratio
        # if self.x < player.x:
        #     self.x += 2 * self.xratio
        # if self.y > player.y:
        #     self.y -= 2 * self.yratio
        # if self.y < player.y:
        #     self.y += 2 * self.yratio
        print('borked')

    def moveToTile(self, x, y, speed):
        print('borked')

    def moveToWidget(self, widget, speed):
        print('borked')

    def updateHitbox(self):
        # self.hitBox = pygame.Rect((self.x + self.gfxLeft, self.y + self.gfxTop, self.w, self.h))
        self.hitBox = pygame.Rect(
            (self.x + self.gfxLeft, (self.y + self.gfxTop + self.h) - (self.h / 2), self.w, self.h / 2))

    def physics(self, px, py):
        # px and py are the horizontal and vertical speeds we are calculating

        # If left momentum, decelerate
        if px < 0:
            # If moving left at a speed lower than minimum deceleration speed
            if abs(px) < self.xDecelerate:
                # Then just stop altogether
                self.xMomentum = 0
            # Otherwise, decelerate
            else:
                self.xMomentum += self.xDecelerate

        # If right momentum (see left above)
        if px > 0:
            if abs(px) < self.xDecelerate:
                self.xMomentum = 0
            else:
                self.xMomentum -= self.xDecelerate

        # If moving up
        if py < 0:
            if py > self.xDecelerate:
                self.yMomentum = 0
            else:
                self.yMomentum += self.xDecelerate

        # If moving down
        if py > 0:
            if py < self.xDecelerate:
                self.yMomentum = 0
            else:
                self.yMomentum -= self.xDecelerate

        # If momentum remaining (in either direction), move the xy and recreate hitbox
        if abs(px) > 0:
            # Change the fighter's actual speed to manageable number
            self.xMomentum = round(self.xMomentum, 2)
            # Move the fighter's actual horizontal position by the horizontal speed
            self.x += self.xMomentum
            # Round to the nearest full pixel
            self.x = round(self.x)
            # Update hitbox
            self.updateHitbox()

        # If moving vertically, move and recreate hitbox:
        if abs(py) > 0:
            # See horizontal movement above
            self.yMomentum = round(self.yMomentum, 2)
            self.y += self.yMomentum
            self.y = round(self.y)
            self.updateHitbox()

        if self.xMomentum + self.yMomentum == 0:
            self.animator.Momentum = 0  # If not moving
        else:
            self.animator.Momentum = (abs(self.xMomentum) + abs(
                self.yMomentum)) / 2  # Average X and Y momentum together


class Player(Widget):
    def __init__(self, animationType, x, y, w, h):
        super().__init__(animationType, x, y, w, h, 1)
        self.hitBox = pygame.Rect(
            (self.x + self.gfxLeft, (self.y + self.gfxTop + self.h) - (self.h / 2), self.w, self.h / 2))
        self.useBox = pygame.Rect(
            (self.x + self.gfxLeft, self.y + self.gfxTop + self.h, self.w, self.h / 2))
        self.useTrigger = False

    def updateHitbox(self):
        self.hitBox = pygame.Rect(
            (self.x + self.gfxLeft, (self.y + self.gfxTop + self.h) - (self.h / 2), self.w, self.h / 2))

    def blink(self, x, y):
        self.x = x
        self.y = y

    def moveUp(self, velocity):
        # If the fighter is not already running their max speed
        if abs(self.yMomentum) < self.maxRun:
            # Add to momentum equal to global acceleration and joystick value
            self.yMomentum -= (self.yAccelerate * velocity)
            # Round momentum to a smaller decimal place
            self.yMomentum = round(self.yMomentum, 2)
        if abs(self.yMomentum) > abs(self.xMomentum):
            self.animator.setDirection('up')
            self.direction = 'up'

    def moveLeft(self, velocity):
        # If the fighter is not already running their max speed
        if abs(self.xMomentum) < self.maxRun:
            # Add to momentum equal to global acceleration and joystick value
            self.xMomentum -= (self.xAccelerate * velocity)
            # Round momentum to a smaller decimal place
            self.xMomentum = round(self.xMomentum, 2)
        if abs(self.xMomentum) > abs(self.yMomentum):
            self.animator.setDirection('left')
            self.direction = 'left'

    def moveDown(self, velocity):
        # If the fighter is not already running their max speed
        if abs(self.yMomentum) < self.maxRun:
            # Add to momentum equal to global acceleration and joystick value
            self.yMomentum += (self.yAccelerate * velocity)
            # Round momentum to a smaller decimal place
            self.yMomentum = round(self.yMomentum, 2)
        if abs(self.yMomentum) > abs(self.xMomentum):
            self.animator.setDirection('down')
            self.direction = 'down'

    def moveRight(self, velocity):
        # If the fighter is not already running their max speed
        if abs(self.xMomentum) < self.maxRun:
            # Add to momentum equal to global acceleration and joystick value
            self.xMomentum += (self.xAccelerate * velocity)
            # Round momentum to a smaller decimal place
            self.xMomentum = round(self.xMomentum, 2)
        if abs(self.xMomentum) > abs(self.yMomentum):
            self.animator.setDirection('right')
            self.direction = 'right'

    def use(self):
        self.useTrigger = True
        if self.direction == 'up':
            self.useBox = pygame.Rect(
                (self.x + self.gfxLeft, self.y + self.gfxTop, self.w, self.h / 2))
        elif self.direction == 'left':
            self.useBox = pygame.Rect(
                (self.x + self.gfxLeft - self.w, (self.y + self.gfxTop + self.h) - (self.h / 2), self.w, self.h / 2))
        elif self.direction == 'right':
            self.useBox = pygame.Rect(
                (self.x + self.gfxLeft + self.w, (self.y + self.gfxTop + self.h) - (self.h / 2), self.w, self.h / 2))
        else:
            self.useBox = pygame.Rect(
                (self.x + self.gfxLeft, self.y + self.gfxTop + self.h, self.w, self.h / 2))

    def trigger(self, colliders):
        if self.useTrigger == True:
            self.useTrigger = False
            for collider in colliders:
                if collider is not self:
                    # If there's any collision at all
                    if self.useBox.colliderect(collider.hitBox):
                        collider.activate(self)


class Controller():
    Up = Left = Down = Right = Use = False
    LastUp = LastLeft = LastDown = LastRight = LastUse = False

    def update(self, events, player):
        self.events = events
        # Look for events
        for event in events:
            # If one of the events was "QUIT"
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.KEYDOWN:
                # Escape key quits the game
                if event.key == pygame.K_ESCAPE:
                    quit()
                # UP (W)
                if event.key == pygame.K_w:
                    self.Up = True
                # LEFT (A)
                if event.key == pygame.K_a:
                    self.Left = True
                # DOWN (S)
                if event.key == pygame.K_s:
                    self.Down = True
                # RIGHT (D)
                if event.key == pygame.K_d:
                    self.Right = True
                # USE (SPACE)
                if event.key == pygame.K_SPACE:
                    self.Use = True

            # If the event is a key RELEASE (up)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.Up = False
                if event.key == pygame.K_a:
                    self.Left = False
                if event.key == pygame.K_s:
                    self.Down = False
                if event.key == pygame.K_d:
                    self.Right = False
                if event.key == pygame.K_SPACE:
                    self.Use = False

        # This repeats even if a key is not pressed again
        # Lifitng the specific key will cause acceleration to stop
        if self.Up:
            player.moveUp(1)
        if self.Left:
            player.moveLeft(1)
        if self.Right:
            player.moveRight(1)
        if self.Down:
            player.moveDown(1)
        if self.Use:
            if not self.useLast:
                player.use()
                self.useLast = True
        else:
            self.useLast = False


class Animator():
    aniMultiplier = 1
    aniCounter = 0
    aniTick = 0
    aniFrame = pygame.image.load('img/tiles/bush.png')
    frameList = []
    Momentum = 0
    aniDirection = 'down'

    def __init__(self, animationType):
        self.animationType = animationType
        self.setAnimation(self.animationType)

    def setAnimation(self, animationType):
        if animationType == 'jack':
            dir = 'img/characters/jack/'
            if self.aniDirection == 'up':
                self.frameList = [pygame.image.load(dir + 'Jack-1-2.png'),
                                  pygame.image.load(dir + 'Jack-0-2.png'),
                                  pygame.image.load(dir + 'Jack-1-2.png'),
                                  pygame.image.load(dir + 'Jack-2-2.png')]
            elif self.aniDirection == 'left':
                self.frameList = [pygame.image.load(dir + 'Jack-1-1.png'),
                                  pygame.image.load(dir + 'Jack-0-1.png'),
                                  pygame.image.load(dir + 'Jack-1-1.png'),
                                  pygame.image.load(dir + 'Jack-2-1.png')]
            elif self.aniDirection == 'right':
                self.frameList = [pygame.image.load(dir + 'Jack-1-3.png'),
                                  pygame.image.load(dir + 'Jack-0-3.png'),
                                  pygame.image.load(dir + 'Jack-1-3.png'),
                                  pygame.image.load(dir + 'Jack-2-3.png')]
            else:
                self.frameList = [pygame.image.load(dir + 'Jack-1-0.png'),
                                  pygame.image.load(dir + 'Jack-0-0.png'),
                                  pygame.image.load(dir + 'Jack-1-0.png'),
                                  pygame.image.load(dir + 'Jack-2-0.png')]

        if animationType == 'draco':
            dir = 'img/characters/draco/'
            if self.aniDirection == 'up':
                self.frameList = [pygame.image.load(dir + 'draco-1-0.png'),
                                  pygame.image.load(dir + 'draco-0-0.png'),
                                  pygame.image.load(dir + 'draco-1-0.png'),
                                  pygame.image.load(dir + 'draco-2-0.png')]
            elif self.aniDirection == 'left':
                self.frameList = [pygame.image.load(dir + 'draco-1-3.png'),
                                  pygame.image.load(dir + 'draco-0-3.png'),
                                  pygame.image.load(dir + 'draco-1-3.png'),
                                  pygame.image.load(dir + 'draco-2-3.png')]
            elif self.aniDirection == 'right':
                self.frameList = [pygame.image.load(dir + 'draco-1-1.png'),
                                  pygame.image.load(dir + 'draco-0-1.png'),
                                  pygame.image.load(dir + 'draco-1-1.png'),
                                  pygame.image.load(dir + 'draco-2-1.png')]
            else:
                self.frameList = [pygame.image.load(dir + 'draco-1-2.png'),
                                  pygame.image.load(dir + 'draco-0-2.png'),
                                  pygame.image.load(dir + 'draco-1-2.png'),
                                  pygame.image.load(dir + 'draco-2-2.png')]

        if animationType == 'bush':
            self.frameList = [pygame.image.load('img/tiles/bush.png')]

    def setDirection(self, direct):
        self.aniDirection = direct
        self.setAnimation(self.animationType)

    def animate(self):
        if not self.Momentum:
            self.aniCounter += 1
            if self.aniCounter >= BPM:
                self.aniCounter = 0
                self.aniTick += 1
        else:
            self.aniCounter += self.Momentum
            if self.aniCounter >= FU_FRAMESPEED:
                self.aniCounter = 0
                self.aniTick += 1
        if self.aniTick >= len(self.frameList):
            self.aniTick = 0
        self.aniFrame = self.frameList[self.aniTick]


class Window():
    def __init__(self, x, y, w, h):
        self.windowSurf = pygame.Surface((w, h))
        self.windowSurf.fill((128, 128, 255))

        return self.windowSurf

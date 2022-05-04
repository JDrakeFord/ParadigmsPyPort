import pygame
import time

from pygame.locals import*
from time import sleep

class Sprite():
    def __init__(self, image_url):
        self.image = pygame.image.load(image_url)
        self.x = 0
        self.y = 0
        self.delete = False
        self.isPot = False
        self.rect = self.image.get_rect()

    def breakPot(self):
        pass

    def update(self, view):
        self.rect.left = self.left - view.scrollPosX
        self.rect.top = self.top - view.scrollPosY

class Link(Sprite):
    def __init__(self):
        super().__init__("link_images/link01.png")
        self.height = 70
        self.width = 60
        self.x = 85
        self.y = 165
        self.absX = 85
        self.absY = 165
        self.speed = 8.0
        self.top = self.absY
        self.bottom = self.absY + self.height
        self.left = self.absX
        self.right = self.absX + self.width
        self.link_images = []
        self.lastImageIndex = 0
        self.count = 0
        for i in range(50):
            if(i < 9):
                self.link_images.append(pygame.image.load("link_images/link" + "0" + str((i + 1)) + ".png"))
            else:
                self.link_images.append(pygame.image.load("link_images/link" + str((i + 1)) + ".png"))

    def setView(self, view):
        self.view = view

    def setController(self, controller):
        self.controller = controller

    def setGame(self, game):
        self.game = game

    def update(self, link, sprites, view):
        self.oldRight = self.right
        self.oldLeft = self.left
        self.oldTop = self.top
        self.oldBottom = self.bottom

        self.top = self.absY
        self.bottom = self.absY + self.height
        self.left = self.absX
        self.right = self.absX + self.width

        if(self.absX > self.game.width):
            self.x = self.absX
            self.view.scrollPosX = self.game.width

        else:
            self.x = self.absX
            self.view.scrollPosX = 0

        if(self.absY > self.game.height):
            self.y = self.absY
            self.view.scrollPosY = self.game.height

        else:
            self.y = self.absY
            self.view.scrollPosY = 0

        if(self.controller.key_down):
            if(self.count == 9):
                self.count = 0
            if(not(self.controller.key_up and self.controller.key_left and self.controller.key_right)):
                self.image = self.link_images[4 + self.count]
                self.lastImageIndex = 4 + self.count
            self.count = self.count + 1

        if(self.controller.key_left):
            if(self.count == 9):
                self.count = 0
            if(not(self.controller.key_up and self.controller.key_down and self.controller.key_right)):
                self.image = self.link_images[13 + self.count]
                self.lastImageIndex = 13 + self.count
            self.count = self.count + 1

        if(self.controller.key_right):
            if(self.count == 9):
                self.count = 0
            if(not(self.controller.key_up and self.controller.key_left and self.controller.key_down)):
                self.image = self.link_images[30 + self.count]
                self.lastImageIndex = 30 + self.count
            self.count = self.count + 1

        if(self.controller.key_up):
            if(self.count == 9):
                self.count = 0
            if(not(self.controller.key_down and self.controller.key_left and self.controller.key_right)):
                self.image = self.link_images[40 + self.count]
                self.lastImageIndex = 40 + self.count
            self.count = self.count + 1

        if(not(self.controller.key_left or self.controller.key_right or self.controller.key_up or self.controller.key_down)):
            self.image = self.link_images[self.lastImageIndex]

        super().update(view)

class Boomerang(Sprite):
    def __init__(self, xIn, yIn, direction):
        super().__init__("boomerang1.png")
        self.boomerangSize = 20
        self.speed = 10.0
        self.direction = direction
        self.x = xIn
        self.y = yIn
        self.left = self.x
        self.right = self.boomerangSize + self.x
        self.top = self.y
        self.bottom = self.boomerangSize + self.y

    def isColliding(self, s):
        if(s.right < self.left):
            return False
        if(s.left > self.right):
            return False
        if(s.bottom < self.top):
            return False
        return s.top <= self.bottom

    def update(self, l, sprites, view):
        if(self.direction == "RIGHT"):
            self.x += self.speed
        elif(self.direction == "LEFT"):
            self.x -= self.speed
        elif(self.direction == "UP"):
            self.y -= self.speed
        elif(self.direction == "DOWN"):
            self.y += self.speed
        self.left = self.x
        self.right = self.boomerangSize + self.x
        self.top = self.y
        self.bottom = self.boomerangSize + self.y
        for i in range(len(sprites)):
            if(self.isColliding(sprites[i])):
                if(isinstance(sprites[i], Brick)):
                    self.delete = True
                elif(isinstance(sprites[i], Pot)):
                    sprites[i].breakPot()
                    self.delete = True
        super().update(view)

class Brick(Sprite):
    def __init__(self, xIn, yIn):
        super().__init__("brick.jpg")
        self.brickSize = 50
        self.x = xIn
        self.y = yIn
        self.left = self.x
        self.right = self.brickSize + self.x
        self.top = self.y
        self.bottom = self.brickSize + self.y

    def isColliding(self, sprite):
        if(sprite.right < self.left):
            return False
        if(sprite.left > self.right):
            return False
        if(sprite.bottom < self.top):
            return False
        return sprite.top <= self.bottom

    def update(self, link, sprites, view):
        if(self.isColliding(link)):
            if (link.right > self.left and link.oldRight <= self.left):
                link.absX = link.oldLeft
            elif (link.left < self.right and link.oldLeft >= self.right):
                link.absX = link.oldRight - link.width
            elif (link.bottom > self.top and link.oldBottom <= self.top):
                link.absY = link.oldTop
            elif (link.top < self.bottom and link.oldTop >= self.bottom):
                link.absY = link.oldBottom - link.height
        super().update(view)

class Pot(Sprite):
    def __init__(self, xIn, yIn):
        super().__init__("pot.png")
        self.potSize = 48
        self.speed = 10.0
        self.brokenFrames = 20
        self.direction = "NONE"
        self.broken = False
        self.x = xIn
        self.y = yIn
        self.left = self.x
        self.right = self.potSize + self.x
        self.top = self.y
        self.bottom = self.potSize + self.y
        self.isPot = True

    def isColliding(self, s):
        if(s.right < self.left):
            return False
        if(s.left > self.right):
            return False
        if(s.bottom < self.top):
            return False
        return s.top <= self.bottom

    def breakPot(self):
        self.direction = "NONE"
        self.broken = True
        self.image = pygame.image.load("pot_broken.png")

    def samePot(self, p1, p2):
        if(p1.x == p2.x and p1.y == p2.y):
            return True
        else:
            return False

    def update(self, link, sprites, view):
        if(self.direction == "RIGHT"):
            self.x += self.speed
        if(self.direction == "LEFT"):
            self.x -= self.speed
        if(self.direction == "UP"):
            self.y -= self.speed
        if(self.direction == "DOWN"):
            self.y += self.speed
        self.left = self.x
        self.right = self.potSize + self.x
        self.top = self.y
        self.bottom = self.potSize + self.y
        if(self.isColliding(link)):
            if (link.right > self.left and link.oldRight <= self.left):
                self.direction = "RIGHT"
            elif (link.left < self.right and link.oldLeft >= self.right):
                self.direction = "LEFT"
            elif (link.bottom > self.top and link.oldBottom <= self.top):
                self.direction = "DOWN"
            elif (link.top < self.bottom and link.oldTop >= self.bottom):
                self.direction = "UP"
        for i in range(len(sprites)):
            if(isinstance(sprites[i], Brick) and self.isColliding(sprites[i])):
                self.breakPot()
            if(isinstance(sprites[i], Pot) and self.isColliding(sprites[i]) and not(self.samePot(self, sprites[i]))):
                self.breakPot()
                sprites[i].breakPot()
        if(self.broken):
            if(self.brokenFrames == 0):
                self.delete = True
            else:
                self.brokenFrames = self.brokenFrames - 1
        super().update(view)

class Model():
    def __init__(self, link):
        self.link = link
        self.sprites = []
        self.sprites.append(self.link)
        for i in range(24):
            self.sprites.append(Brick(0, i*50))
            self.sprites.append(Brick(1550, i*50))
            if(i != 3 and i != 19 and i != 4 and i != 20):
                self.sprites.append(Brick(750, i*50))
                self.sprites.append(Brick(800, i*50))
        for i in range(32):
            self.sprites.append(Brick(i * 50, 0))
            self.sprites.append(Brick(i * 50, 1150))
            if(i != 3 and i != 25 and i != 4 and i != 26):
                self.sprites.append(Brick(i * 50, 550))
                self.sprites.append(Brick(i * 50, 600))
        self.sprites.append(Pot(200, 200))
        self.sprites.append(Pot(200, 400))
        self.sprites.append(Pot(1000, 300))
        self.sprites.append(Pot(1100, 400))
        self.sprites.append(Pot(300, 900))
        self.sprites.append(Pot(300, 1000))
        self.sprites.append(Pot(1000, 1000))
        self.sprites.append(Pot(1100, 800))

    def setView(self, v):
        self.view = v

    def setLink(self, l):
        self.link = l

    def update(self, l, view):
        self.link = l
        for i in range(0, len(self.sprites)):
            self.sprites[i].update(self.link, self.sprites, view)
        self.sprites = [sprite for sprite in self.sprites if not sprite.delete]
        self.link.update(self.link, self.sprites, view)

    def addBrick(self, x, y):
        temp = Brick(x, y)
        self.sprites.append(temp)

    def addPot(self, x, y):
        temp = Pot(x, y)
        self.sprites.append(temp)

class View():
    def __init__(self, model):
        screen_size = (800,600)
        self.screen = pygame.display.set_mode(screen_size, 32)
        self.model = model
        self.scrollPosX = 0
        self.scrollPosY = 0

    def setGame(self, game):
        self.game = game

    def setModel(self, model):
        self.model = model

    def setLink(self, link):
        self.link = link

    def update(self, sprites):
        self.screen.fill([19, 237, 230])
        for sprite in sprites:
            self.screen.blit(sprite.image, sprite.rect)
        pygame.display.flip()

class Controller():
    def __init__(self, model, view, game, link):
        self.model = model
        self.view = view
        self.game = game
        self.link = link
        self.key_right = False
        self.key_left = False
        self.key_up = False
        self.key_down = False
        self.keep_going = True

    def update(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.keep_going = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.keep_going = False
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.key_left = True
            self.link.absX -= self.link.speed
        else:
            self.key_left = False

        if keys[K_RIGHT]:
            self.key_right = True
            self.link.absX += self.link.speed
        else:
            self.key_right = False

        if keys[K_UP]:
            self.key_up = True
            self.link.absY -= self.link.speed
        else:
            self.key_up = False

        if keys[K_DOWN]:
            self.key_down = True
            self.link.absY += self.link.speed
        else:
            self.key_down = False

        if keys[K_LCTRL] or keys[K_RCTRL]:
            if(self.link.lastImageIndex >= 4 and self.link.lastImageIndex <= 12):
                self.model.sprites.append(Boomerang(self.link.absX + self.link.width / 2, self.link.absY + self.link.height / 2, "DOWN"))
            elif(self.link.lastImageIndex >= 13 and self.link.lastImageIndex <= 21):
                self.model.sprites.append(Boomerang(self.link.absX + self.link.width / 2, self.link.absY + self.link.height / 2, "LEFT"))
            elif(self.link.lastImageIndex >= 30 and self.link.lastImageIndex <= 38):
                self.model.sprites.append(Boomerang(self.link.absX + self.link.width / 2, self.link.absY + self.link.height / 2, "RIGHT"))
            else:
                self.model.sprites.append(Boomerang(self.link.absX + self.link.width / 2, self.link.absY + self.link.height / 2, "UP"))


class Game:
    def __init__(self):
        self.link = Link()
        self.model = Model(self.link)
        self.view = View(self.model)
        self.link.setView(self.view)
        self.controller = Controller(self.model, self.view, self, self.link)
        self.link.setController(self.controller)
        self.link.setGame(self)
        self.view.setGame(self)
        self.width = 800
        self.height = 600

print("Use the arrow keys to move. Press Esc to quit.")
pygame.init()
game = Game()
while game.controller.keep_going:
    game.controller.update()
    game.model.update(game.model.link, game.view)
    game.view.update(game.model.sprites)
    sleep(0.04)
print("Goodbye")

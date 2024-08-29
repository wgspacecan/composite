import sys
import pygame

pygame.init()
screen = pygame.display.set_mode((500, 820))
clock = pygame.time.Clock()
running = True
dt = 0

font = pygame.font.SysFont('Arial', 40)

objects = []
states = []

for i in range(9):
    states.append(0)

print(states)

usercolor1 = '#333333'
usercolor2 = '#ff6347'

current_user = 1

class Button():
    def __init__(self, x, y, width, height, buttonName='', onClick=None, user=1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.buttonName = buttonName
        self.onclickFunction = onClick
        self.alreadyPressed = False

        if user == 1:
            self.usercolor = usercolor1
        elif user == 2:
            self.usercolor = usercolor2

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': self.usercolor,
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render('', True, (20, 20, 20))

        objects.append(self)
    
    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if not self.alreadyPressed:
                    self.onclickFunction(self.buttonName)
                    self.alreadyPressed = True
                    states[self.buttonName-1] = 1
            else:
                self.alreadyPressed = False
                states[self.buttonName-1] = 0
            

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)

class ButtonMenu():
    def __init__(self, x, y, width, height, buttonName='', onClick=None, buttonText=''):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.buttonName = buttonName
        self.buttonText = buttonText
        self.onclickFunction = onClick
        self.alreadyPressed = False

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(self.buttonText, True, (20, 20, 20))

        objects.append(self)
    
    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if not self.alreadyPressed:
                    self.onclickFunction(self.buttonName)
                    self.alreadyPressed = True
                    states[self.buttonName-1] = 1
            else:
                self.alreadyPressed = False
                states[self.buttonName-1] = 0
            

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)

def buttonPressed(name):
    print('Button Pressed: ' + str(name))

# first row
Button(30, 30, 100, 100, 1, buttonPressed, 1)
Button(140, 30, 100, 100, 2, buttonPressed, 2)
Button(250, 30, 100, 100, 3, buttonPressed)

# second row
Button(30, 140, 100, 100, 4, buttonPressed)
Button(140, 140, 100, 100, 5, buttonPressed)
Button(250, 140, 100, 100, 6, buttonPressed)

# third row
Button(30, 250, 100, 100, 7, buttonPressed)
Button(140, 250, 100, 100, 8, buttonPressed)
Button(250, 250, 100, 100, 9, buttonPressed)

# menu
ButtonMenu(30, 400, 300, 100, 0, buttonPressed, 'reset')
ButtonMenu(30, 510, 300, 100, 0, buttonPressed, 'user1')
ButtonMenu(30, 620, 300, 100, 0, buttonPressed, 'user2')

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    for object in objects:
        object.process()

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
import sys
import pygame

pygame.init()
screen = pygame.display.set_mode((470, 820))
clock = pygame.time.Clock()
running = True
dt = 0

allowRelease = False
allowOverwrite = False

# set the pygame window name
pygame.display.set_caption('Tic Tac Toe')

font = pygame.font.SysFont('Arial', 40)

winner = 0
objects = []
states = []
state1 = []
state2 = []

for i in range(9):
    states.append(0)
    state1.append(0)
    state2.append(0)

current_user = 1

class Button():
    def __init__(self, x, y, width, height, buttonName='', onClick=None, buttonText=''):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.buttonName = buttonName
        self.buttonText = buttonText
        self.onclickFunction = onClick
        self.alreadyPressed = False
        self.toggledUser = 0
        self.usercolor1 = '#15dbed'
        self.usercolor2 = '#ff6347'

        if self.buttonText == '':
            self.fillColors = {
                'normal': '#ffffff',
                'hover': '#666666',
                'pressed': '#333333',
            }
        else:
            self.fillColors = {
                'pressed': '#ffffff',
                'normal': '#666666',
                'hover': '#333333',
            }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(self.buttonText, True, (20, 20, 20))

        objects.append(self)
    
    def process(self):
        # update game button color
        if self.buttonText == '':
            if self.toggledUser == 1:
                self.fillColors['pressed'] = self.usercolor1
            elif self.toggledUser == 2:
                self.fillColors['pressed'] = self.usercolor2
    
        mousePos = pygame.mouse.get_pos()
        if states[self.buttonName-1] == 0 or self.buttonText != '': self.buttonSurface.fill(self.fillColors['normal'])
        else: self.buttonSurface.fill(self.fillColors['pressed'])

        if self.buttonText != '' and current_user == self.buttonName: self.buttonSurface.fill(self.fillColors['pressed'])
        # hover
        if self.buttonRect.collidepoint(mousePos):
            if self.toggledUser != current_user and states[self.buttonName-1] == 0: self.buttonSurface.fill(self.fillColors['hover'])
            # pressed
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                # first press
                if not self.alreadyPressed:
                    if self.buttonText != '': self.onclickFunction(self.buttonName)
                    if self.buttonText == '':
                        self.alreadyPressed = True
                        # manage state
                        if states[self.buttonName-1] == 1 and allowRelease:
                            states[self.buttonName-1] = 0
                            if current_user == 1: state1[self.buttonName-1] = 0
                            if current_user == 2: state2[self.buttonName-1] = 0
                        elif states[self.buttonName-1] == 0 or allowOverwrite:
                            states[self.buttonName-1] = 1
                            if current_user == 1: state1[self.buttonName-1] = 1
                            if current_user == 2: state2[self.buttonName-1] = 1
                            self.toggledUser = current_user
                            self.onclickFunction(self.buttonName)
                # update press color
                self.buttonSurface.fill(self.fillColors['pressed'])

            # release
            else:
                self.alreadyPressed = False
                if states[self.buttonName-1] == 0: self.toggledUser = 0
            

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)

def resetBoard(user):
    global winner
    winner = 0
    for i in range(9):
        states[i] = 0
        state1[i] = 0
        state2[i] = 0
    print('reset board')

def changeUser(user):
    global current_user
    current_user = user
    print('changed current user: ' + str(user))

def detectWin(state):
    result = False
    if state[0] == state[1] == state[2] == 1: result = True
    elif state[3] == state[4] == state[5] == 1: result = True
    elif state[6] == state[7] == state[8] == 1: result = True
    elif state[2] == state[4] == state[6] == 1: result = True
    elif state[0] == state[4] == state[8] == 1: result = True
    elif state[1] == state[4] == state[7] == 1: result = True
    elif state[3] == state[4] == state[5] == 1: result = True
    elif state[0] == state[3] == state[6] == 1: result = True
    elif state[2] == state[5] == state[8] == 1: result = True
    return result

def detectTie():
    allOne = True
    for each in states:
        if each == 0: allOne = False
    return allOne

def scanState():
    global winner
    if current_user == 1:
        if detectWin(state1):
            winner = 1
            print("User 1 has won!")
    elif current_user == 2:
        if detectWin(state2):
            winner = 2
            print("User 2 has won!")
    
    if detectTie():
        winner = 9
        print("TIE")

def buttonPressed(name):
    scanState()
    if current_user == 1: changeUser(2)
    elif current_user == 2: changeUser(1)

# first row
Button(70, 120, 100, 100, 1, buttonPressed)
Button(180, 120, 100, 100, 2, buttonPressed)
Button(290, 120, 100, 100, 3, buttonPressed)

# second row
Button(70, 230, 100, 100, 4, buttonPressed)
Button(180, 230, 100, 100, 5, buttonPressed)
Button(290, 230, 100, 100, 6, buttonPressed)

# third row
Button(70, 340, 100, 100, 7, buttonPressed)
Button(180, 340, 100, 100, 8, buttonPressed)
Button(290, 340, 100, 100, 9, buttonPressed)

# menu
Button(30, 490, 400, 50, 1, changeUser, 'User 1')
Button(30, 560, 400, 50, 2, changeUser, 'User 2')
Button(30, 650, 400, 50, 0, resetBoard, 'Reset')

# text
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
userTextX = 150
userTextY = 750
# - title
titleTextX = 150
titleTextY = 70
text = font.render('TicTacToe!!', True, green, blue)
textRect = text.get_rect()
textRect.center = (titleTextX, titleTextY)
# - winner
winnerTextX = 200
winnerTextY = 300

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # title text
    screen.blit(text, textRect)

    # user text
    usertext = font.render('User: ' + str(current_user), True, green, blue)
    usertextRect = text.get_rect()
    usertextRect.center = (userTextX, userTextY)
    screen.blit(usertext, usertextRect)

    # button objects
    for object in objects:
        object.process()
    
    # winner text
    if winner != 0:
        if winner == 9: message = 'TIE'
        else: message = 'User ' + str(winner) + ' Wins'
        winnerText = font.render(message, True, green, blue)
        winnerRect = winnerText.get_rect()
        winnerRect.center = (winnerTextX, winnerTextY)
        screen.blit(winnerText, winnerRect)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
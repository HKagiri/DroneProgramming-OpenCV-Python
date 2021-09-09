'''Allows for Drone Keyboard Control
Created a window that allow the function to be called anywhere inside my project'''
import pygame

# func_create window
def init():
    pygame.init()
    win = pygame.display.set_mode((400 , 400))

#funct get Key Presses

def getKey(keyName):
    ans = False
    #check the events
    for eve in pygame.event.get():pass
    keyInput = pygame.key.get_pressed()  #Create input
    myKey = getattr(pygame, 'K_{}'.format(keyName)) # Format to be output for a key pressed e.g K_LEFT
    if keyInput[myKey]:
        ans = True
    pygame.display.update()

    return ans

def main():
    if getKey("LEFT"):
        print("Left Key Pressed")
    if getKey("RIGHT"):
        print("Right Key Pressed")
    #print(getKey("a"))

if __name__ == '__main__':
    init()
    while True:
        main()
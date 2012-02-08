SCREEN_SIZE = (800, 600)


import sys
from math import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import pygame
from pygame.locals import *

from aspen import *

def resize(width, height):

    if height == 0:
        height = 1
    
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, float(width)/height, 0.1, 3000.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def init():
    
    glEnable(GL_DEPTH_TEST)
    glutInit(sys.argv)
    glShadeModel(GL_FLAT)
    #glClearColor(1.0, 1.0, 1.0, 0.0)

    #glEnable(GL_COLOR_MATERIAL)
    
    #glEnable(GL_LIGHTING)
    #glEnable(GL_LIGHT0)
    #glLight(GL_LIGHT0, GL_POSITION,  (0, 1, 1, 0))    


def drawGround():
    extent = 20000.0
    step = 50.0
    y = -100.0

    i = -extent
    glColor(255,0,0)
    glBegin(GL_LINES)
    while i <= extent:
        glVertex(i,y,extent)
        glVertex(i,y,-extent)

        glVertex(extent,y,i)
        glVertex(-extent,y,i)
        i += step
        
    glEnd()


def run():
    
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE|OPENGL|DOUBLEBUF)
    
    resize(*SCREEN_SIZE)
    init()
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()
    
    #glMaterial(GL_FRONT, GL_AMBIENT, (0.1, 0.1, 0.1, 1.0))    
    #glMaterial(GL_FRONT, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))

    #sphere constants
    rot_degree = 0.0
    direction = 1
    step = 5
    cur_dist = 100
    max_dist = 100
    min_dist = 25




    TIME_TO_EXIT = False
    player = Player()
    
    while True:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                TIME_TO_EXIT = True
                #pygame.display.quit()
                #pygame.quit()
                #sys.exit()
            if event.type == KEYUP and event.key == K_ESCAPE:
                TIME_TO_EXIT = True
                #pygame.display.quit()
                #pygame.quit()
                #sys.exit()

        if TIME_TO_EXIT == True:
            break
        
        # Clear the screen, and z-buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

        
        time_passed = clock.tick()
        time_passed_seconds = time_passed / 1000.0

        pygame.display.set_caption("FPS "+str(clock.get_fps()))




 

        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        #ANYTHING ON A HUD WOULD GO HERE

        #Camera movement stuff
        player.getMove()
        player.placePlayer()

        #Everything after this is part of the "world"

        drawGround()

        glPushMatrix()

        
        glTranslate(0.0,0.0,-300)
        glColor(255,0,0)
        glRotate(405,1,0,0)
 


        

        glTranslate(0.0,0.0,-300)
        glRotate(rot_degree,0.0,1.0,0.0)
        #glTranslate(0.0,0.0,cur_dist*-1)
        

        
        
        glColor(255,0,0)
        glutSolidSphere(10.0, 15, 15)
        """
        glPushMatrix()
        glTranslate(0,50,50)
        glColor(0,0,255)
        glutSolidSphere(10.0, 15, 15)
        glPopMatrix()

        glPushMatrix()
        glTranslate(100,0,50)
        glColor(0,0,255)
        glutSolidSphere(10.0, 15, 15)
        glPopMatrix()

        glTranslate(-100,0,50)
        glColor(0,0,255)
        glutSolidSphere(10.0, 15, 15)
		"""
        
 

        # Light must be transformed as well
        glLight(GL_LIGHT0, GL_POSITION,  (0, 1.5, 1, 0)) 


        glPopMatrix()
        # Show the screen

        pygame.display.flip()


        cur_dist += step * direction
        if cur_dist > max_dist or cur_dist < min_dist:

                direction = direction * -1
                cur_dist += step * direction


        rot_degree += 0.5
        if rot_degree > 360:
                rot_degree = 0.0

    pygame.display.quit()
    pygame.quit()

run()

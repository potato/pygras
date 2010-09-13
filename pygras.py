#!/usr/bin/env python

import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from random import random
from math import sqrt

class Star:
    def __init__(self):
        # position
        self.pos = (0.0, 0.0, 0.0)

        # velocity
        self.v  = (0.0, 0.0, 0.0)

        # mass
        self.m = 0.02 # * pow(10, 11)

def handleKeypress(key, x, y):
    if ord(key) == 27:
        sys.exit()

def handleResize(w, h):
    glViewport(0, 0, w, h)

    glMatrixMode(GL_PROJECTION)

    glLoadIdentity()
    gluPerspective(45.0, w / h, 1.0, 200.0)

def initRendering():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_NORMALIZE)

def drawScene():
    global stars

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -50.0)

    for star in stars:
        glPushMatrix()
        glTranslatef(star.pos[0], star.pos[1], star.pos[2])
        glutSolidSphere(0.1, 100, 100)
        glPopMatrix()
    
    glutSwapBuffers()

def update(value):
    global stars, g

    for bstar in stars:
        for star in stars:
            if bstar != star:
                if abs(star.pos[0] - bstar.pos[0]) < 0.5 and abs(star.pos[1] - bstar.pos[1]) < 0.5 and abs(star.pos[2] - bstar.pos[2]) < 0.5:
                    stars.remove(star)
                    continue
                d = sqrt(pow(star.pos[0] - bstar.pos[0], 2) + pow(star.pos[1] - bstar.pos[1], 2) + pow(star.pos[2] - bstar.pos[2], 2))
                i = ( (star.pos[0] - bstar.pos[0]) / d, (star.pos[1] - bstar.pos[1]) / d, (star.pos[2] - bstar.pos[2]) / d )
                f = g * ((bstar.m * star.m) / (d*d))
                f = (f * i[0], f * i[1], f * i[2])
                a = (f[0] / bstar.m, f[1] / bstar.m, f[2] / bstar.m)
                bstar.v = (bstar.v[0] + a[0], bstar.v[1] + a[1], bstar.v[2] + a[2]) 

    glutPostRedisplay();
    for star in stars:
        star.pos = (star.pos[0] + star.v[0], star.pos[1] + star.v[1], star.pos[2] + star.v[2]) 
    glutTimerFunc(25, update, 0)

if __name__ == '__main__':
    g = 6.67428 # * pow(10, -11)
    stars = []

    star = Star()
    star.pos = (5.0, 0.0, 0.0)
    star.v = (0.0, 0.1, 0.1)
    stars.append(star)

    star = Star()
    star.pos = (-5.0, 0.0, 0.0)
    star.v = (0.0, -0.1, -0.1)
    stars.append(star)
    
    star = Star()
    star.pos = (0.0, 0.0, 0.0)
    star.v = (0.0, 0.0, 0.0)
    stars.append(star)

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(700, 700)

    glutCreateWindow("PyGraS - v0.00001 =)")
    initRendering()

    glutDisplayFunc(drawScene)
    glutKeyboardFunc(handleKeypress)
    glutReshapeFunc(handleResize)

    glutTimerFunc(25, update, 0)
    glutMainLoop()

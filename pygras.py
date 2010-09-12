#!/usr/bin/env python

import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math

class Star:
    def __init__(self):
        # position
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

        # velocity
        self.vx = 0.0
        self.vy = 0.0
        self.vz = 0.0

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
        glTranslatef(star.x, star.y, star.z)
        glutSolidSphere(0.1, 100, 100)
        glPopMatrix()
    
    glutSwapBuffers()

def update(value):
    global stars, g

    for bstar in stars:
        for star in stars:
            if bstar != star:
                if abs(star.x - bstar.x) < 0.5 and abs(star.y - bstar.y) < 0.5 and abs(star.z - bstar.z) < 0.5:
                    stars.remove(star)
                    continue
                d = math.sqrt(pow(star.x - bstar.x, 2) + pow(star.y - bstar.y, 2) + pow(star.z - bstar.z, 2))

                ix = (star.x - bstar.x) / d
                iy = (star.y - bstar.y) / d
                iz = (star.z - bstar.z) / d

                f = g * ((bstar.m * star.m) / (d*d))

                fx = f * ix
                fy = f * iy
                fz = f * iz

                ax = fx / bstar.m
                ay = fy / bstar.m
                az = fz / bstar.m

                bstar.vx += ax
                bstar.vy += ay
                bstar.vz += az

    glutPostRedisplay();
    for star in stars:
        star.x += star.vx
        star.y += star.vy
        star.z += star.vz
    glutTimerFunc(25, update, 0)

if __name__ == '__main__':
    g = 6.67428 # * pow(10, -11)
    stars = []

    star = Star()
    star.x = 5.0
    star.y = 0.0
    star.z = 0.0
    star.vx = 0.0
    star.vy = 0.1
    star.vz = 0.0
    stars.append(star)

    star = Star()
    star.x = -5.0
    star.y = 0.0
    star.z = 0.0
    star.vx = 0.0
    star.vy = -0.1
    star.vz = 0.0
    stars.append(star)
    
    star = Star()
    star.x = 0.0
    star.y = 0.0
    star.z = 0.0
    star.vx = 0.0
    star.vy = 0.0
    star.vz = 0.0
    stars.append(star)

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(700, 700)

    glutCreateWindow("PyGraS - v0.00001 =)")
    initRendering()

    glutDisplayFunc(drawScene)
    glutKeyboardFunc(handleKeypress)
    glutReshapeFunc(handleResize)
    glutPassiveMotionFunc(handleMouse)

    glutTimerFunc(25, update, 0)
    glutMainLoop()

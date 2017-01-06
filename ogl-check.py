#!/usr/bin/env python2
#Time-stamp: <2017-01-07 08:24:22 hamada>
import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
#import pyglut
#import pygame
import os
import logging as LG

# create logger
logger = LG.getLogger(os.path.basename(__file__))
logger.setLevel(LG.DEBUG)

# create console handler and set level to debug
ch = LG.StreamHandler()
ch.setLevel(LG.DEBUG)

# create formatter
formatter = LG.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

init_flag = 0

def display():
    global init_flag
    if not init_flag:
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_DEPTH_TEST)
        init_flag = 1
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        gluLookAt(0,3,-10, 0,0,0, 0,1,0)
        glutWireTorus(1., 3., 200, 200) 
        glutSolidTeapot(2)
        glPopMatrix()
        glFlush()

def reshape(w,h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, 1.0*w/h, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def key(k, x, y):
    logger.info('key: "%c" (%d, %d) ', k, x, y)
    if 'q'     == k: quit_app(0) # q
    if 'a'     == k: quit_app(1) # a
    if 'b'     == k: quit_app(2) # b
    if 'c'     == k: quit_app(3) # c
    if 'd'     == k: quit_app(4) # d
    if chr(27) == k: quit_app(0) # ESC
    if chr(13) == k: quit_app(0) # Enter

def quit_app(id):
    if 0 == id:
        logger.info('God bless you !')
    elif 1 == id:
        logger.debug('GOD bless you !')
    elif 2 == id:
        logger.warn('GOD BLESS you !')
    elif 3 == id:
        logger.error('GOD BLESS YOU !')
    else:
        logger.critical('GOD BLESS YOU !!')
    sys.exit(id)

if  '__main__' == __name__:
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1024, 768)
    glutCreateWindow('pyOpenGL is working fine on your system: Enter/Esc/q for quit')
    glutReshapeFunc(reshape)
    glutKeyboardFunc(key)
    glutDisplayFunc(display)
    glutMainLoop()

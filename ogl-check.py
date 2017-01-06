#!/usr/bin/env python2
#Time-stamp: <2017-01-07 07:40:11 hamada>

import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
#import pyglut
#import pygame

init_flag = 0

def display():
    global init_flag
    if not init_flag:
        glEnable( GL_LIGHTING )
        glEnable( GL_LIGHT0 )
        glEnable( GL_DEPTH_TEST )
        init_flag = 1

        glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
        glPushMatrix()
        gluLookAt( 0,3,-10, 0,0,0, 0,1,0 )
        glutSolidTeapot( 2 )
        glPopMatrix()
        glFlush()

def reshape(w,h):
    glViewport( 0, 0, w, h )
    glMatrixMode( GL_PROJECTION )
    glLoadIdentity()
    gluPerspective( 45.0, 1.0*w/h, 0.1, 100.0 )
    glMatrixMode( GL_MODELVIEW )
    glLoadIdentity()

def keyboard(key,x,y):
    if key==chr(27): sys.exit(0)

if __name__ == '__main__':
    glutInit( sys.argv )
    glutInitDisplayMode( GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH )
    glutInitWindowSize( 256, 256 )
    glutCreateWindow( 'teapot' )
    glutReshapeFunc( reshape )
    glutKeyboardFunc( keyboard )
    glutDisplayFunc( display )
    glutMainLoop()

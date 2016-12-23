#!/usr/bin/env python2
#Time-stamp: <2016-12-24 02:14:47 hamada>
import OpenGL 
OpenGL.ERROR_ON_COPYs = True 
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.constants import GLfloat
import sys, time, math, random

def init():
    glLightfv(GL_LIGHT0, GL_AMBIENT, vec4(0.5, 0.1,  -0.1, 0.1))
    glLightfv(GL_LIGHT1, GL_AMBIENT, vec4(0.5, 0.1,  1.0,  0.1))
    glEnable(GL_CULL_FACE)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)

if __name__ == '__main__':
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowPosition(800, 0)
    glutInitWindowSize(800, 800)
    glutCreateWindow("SPHpy")
    init()


    print "hello"





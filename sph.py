#!/usr/bin/env python2
import OpenGL 
OpenGL.ERROR_ON_COPYs = True 
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.constants import GLfloat
import sys, time, math, random


if __name__ == '__main__':
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowPosition(800, 0)
    glutInitWindowSize(800, 800)
    glutCreateWindow("SPHpy")
    time.sleep(5)

    print "Hello SPH.py"




#!/usr/bin/env python2
#Time-stamp: <2016-12-24 02:59:31 hamada>
import OpenGL 
OpenGL.ERROR_ON_COPYs = True 
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.constants import GLfloat
import sys, time, math, random

vec4 = GLfloat_4

class Viewer: 
    def __init__(self, 
                 is_3D=True, mouse_l=0, mouse_m=0, mouse_r=0,
                 view_rot=[0., 180., 0.],
                 r_max = 20., v_max=1., radius_max=0.001,
                 fps_calc = 0., fps_phys=0., sim_step=0, sim_time=0.,
                 sphere_radius_coef = 300, sphere_slic = 32, sphere_stack = 32,
                 mpos = [0,0], trans = [0., 1.4, -14.]):
        self.is_3D = is_3D
        self.mouse_l = mouse_l
        self.mouse_m = mouse_m
        self.mouse_r = mouse_r
        self.view_rot = [view_rot[i] for i in range (0, 3)]
        self.r_max = r_max
        self.v_max = v_max
        self.radius_max = radius_max
        self.mpos = [mpos[i] for i in range (0, 2)]
        self.trans = [trans[i] for i in range (0, 3)]
        self.fps_calc = fps_calc
        self.fps_phys = fps_phys
        self.sim_step = sim_step
        self.sim_time = sim_time
        self.sphere_radius_coef = sphere_radius_coef
        self.sphere_slic = sphere_slic
        self.sphere_stack = sphere_stack

viewer = Viewer()

def draw_box():
    c_min = [ -6.0, -10.0,  -1.5]
    c_max = [  6.0,  10.0,   1.5]

    glLineWidth(2)
    glBegin(GL_LINES)
    glColor3f(1.0, 1.0, 1.0)
    glVertex3f(c_min[0], c_min[1], c_min[2]),    glVertex3f(c_max[0], c_min[1], c_min[2])
    glVertex3f(c_min[0], c_max[1], c_min[2]),    glVertex3f(c_max[0], c_max[1], c_min[2])
    glVertex3f(c_min[0], c_min[1], c_max[2]),    glVertex3f(c_max[0], c_min[1], c_max[2])
    glVertex3f(c_min[0], c_max[1], c_max[2]),    glVertex3f(c_max[0], c_max[1], c_max[2])

    glVertex3f(c_min[0], c_min[1], c_min[2]),    glVertex3f(c_min[0], c_max[1], c_min[2])
    glVertex3f(c_max[0], c_min[1], c_min[2]),    glVertex3f(c_max[0], c_max[1], c_min[2])
    glVertex3f(c_min[0], c_min[1], c_max[2]),    glVertex3f(c_min[0], c_max[1], c_max[2])
    glVertex3f(c_max[0], c_min[1], c_max[2]),    glVertex3f(c_max[0], c_max[1], c_max[2])

    glVertex3f(c_min[0], c_min[1], c_min[2]),    glVertex3f(c_min[0], c_min[1], c_max[2])
    glVertex3f(c_min[0], c_max[1], c_min[2]),    glVertex3f(c_min[0], c_max[1], c_max[2])
    glVertex3f(c_max[0], c_min[1], c_min[2]),    glVertex3f(c_max[0], c_min[1], c_max[2])
    glVertex3f(c_max[0], c_max[1], c_min[2]),    glVertex3f(c_max[0], c_max[1], c_max[2])
    glEnd()

def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0., 0.,-40.+viewer.trans[2], 0.0, 0.0,  0.0, 0.0, 1.0, 0.0) 

    glPushMatrix()
    glRotatef(viewer.view_rot[0], 1.0, 0.0, 0.0)
    glRotatef(viewer.view_rot[1], 0.0, 1.0, 0.0)
    glRotatef(viewer.view_rot[2], 0.0, 0.0, 1.0)

    draw_box()

    glPopMatrix()
    glutSwapBuffers()

def reshape(width, height):
    h = float(height) / float(width)
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(30.0, h, 0.001, 1000.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -40.0)

def idle():
    glutPostRedisplay()


def key(k, x, y):
    global viewer

    if  k == 'q':
        sys.exit(0)
    elif ord(k) == 27: # Escape
        sys.exit(0)
    else:
        return

    glutPostRedisplay()


def mouse(button, state, x, y):
    global viewer
    
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN: 
            viewer.mpos[0] = x
            viewer.mpos[1] = y
            viewer.mouse_l = 1
        if state == GLUT_UP:
            viewer.mouse_l = 0
    elif button == GLUT_MIDDLE_BUTTON:
        if state == GLUT_DOWN:
            viewer.mpos[0] = x
            viewer.mpos[1] = y
            viewer.mouse_m = 1
        if state == GLUT_UP:
            viewer.mouse_m = 0
    elif button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            viewer.mpos[0] = x
            viewer.mpos[1] = y
            viewer.mouse_r = 1
        if state == GLUT_UP:
            viewer.mouse_r = 0
    else:
        return


def init():
    glLightfv(GL_LIGHT0, GL_AMBIENT, vec4(0.5, 0.1,  -0.1, 0.1))
    glLightfv(GL_LIGHT1, GL_AMBIENT, vec4(0.5, 0.1,  1.0,  0.1))
    glEnable(GL_CULL_FACE)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)

def visible(vis):
    if vis == GLUT_VISIBLE:
        glutIdleFunc(idle)

if __name__ == '__main__':
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowPosition(800, 0)
    glutInitWindowSize(800, 800)
    glutCreateWindow("SPHpy")
    init()

    glutDisplayFunc(draw)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(key)
    glutMouseFunc(mouse)
    glutVisibilityFunc(visible)

    if "--info" in sys.argv:
        print "GL_RENDERER   = ", glGetString(GL_RENDERER)
        print "GL_VERSION    = ", glGetString(GL_VERSION)
        print "GL_VENDOR     = ", glGetString(GL_VENDOR)
        print "GL_EXTENSIONS = ", glGetString(GL_EXTENSIONS)

    print "hello"

    glutMainLoop()



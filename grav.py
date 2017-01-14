#!/usr/bin/env python
# Time-stamp: <2017-01-08 04:12:34 hamada>
# GRAVpy
# Copyright(c) 2017 by Tsuyoshi Hamada. All rights reserved.

import os
import logging as LG
import OpenGL
OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.constants import GLfloat
import sys, time, math, random

def create_logger():
    # create logger
    _logger = LG.getLogger(os.path.basename(__file__))
    _logger.setLevel(LG.DEBUG)
    # create console handler and set level to debug
    ch = LG.StreamHandler()
    ch.setLevel(LG.DEBUG)
    # create formatter
    formatter = LG.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    _logger.addHandler(ch)
    return _logger


def get_logger(str_position = ''):

    log_basename = __file__

    # Don't use Python's hasattr()
    #     unless you're writing Python 3-only code 
    #     and understand how it works.
    if getattr(get_logger, "__count_called", None) is not None:
        log_basename = "%s @%s" % (__file__, str_position)
        get_logger.__count_called = get_logger.__count_called + 1
    else:
        get_logger.__count_called = 1

    # create logger
    logger = LG.getLogger(os.path.basename(log_basename))

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

    # 'application' code
    ## logger.debug('debug message')
    ## logger.info('info message')
    ## logger.warn('warn message')
    ## logger.error('error message')
    ## logger.critical('critical message')
    return logger

logger = get_logger()

## logger.debug('debug message')
## logger.info('info message')
## logger.warn('warn message')
## logger.error('error message')
## logger.critical('critical message')



vec4 = GLfloat_4
particles = [ ]
help_msg = [
"-------------------------",
"k: rotate simulation box",
"j: rotate simulation box",
"J: box size --",
"K: box size ++",
"t: dt--",
"T: dt++",
"r: shuffle particles",
"o: Sphere size --",
"O: Sphere size ++",
"v: decrease velocity",
"V: increase velocity",
"[Space]: increase particles",
"-: delete a particle",
"1: for debug",
"2: change 3D->2D",
"q: quit",
"h: show this message",
]


class Simulation_Parameters:
    def __init__(self, scale = 1.00,
                 sim_box_min = [-10., -10.0, -10.0],
                 sim_box_max = [ 10.,  10.0,  10.0],
                 limit=200., dt=0.004):
        self.limit = limit         #  velocity limitation at boundary condition
        self.dt    = dt            #  delta time for each time-stemps (shared time-step scheme)
        self.scale = scale         # multiples x,y,z by this value
        self.sim_box_min = sim_box_min # simulation box size
        self.sim_box_max = sim_box_max # simulation box size

class Viewer:
    def __init__(self,
                 is_3D=True, mouse_l=0, mouse_m=0, mouse_r=0, view_rot=[0., 180., 0.],
                 fps_calc = 0., fps_phys=0., sim_step=0, sim_time=0.,
                 sphere_radius_coef = 300, sphere_slic = 32, sphere_stack = 32,
                 mpos = [0,0], trans = [0., 1.4, -14.]):
        self.is_3D = is_3D
        self.mouse_l = mouse_l
        self.mouse_m = mouse_m
        self.mouse_r = mouse_r
        self.view_rot = [view_rot[i] for i in range (0, 3)]
        self.mpos = [mpos[i] for i in range (0, 2)]
        self.trans = [trans[i] for i in range (0, 3)]
        self.fps_calc = fps_calc
        self.fps_phys = fps_phys
        self.sim_step = sim_step
        self.sim_time = sim_time
        self.sphere_radius_coef = sphere_radius_coef
        self.sphere_slic = sphere_slic
        self.sphere_stack = sphere_stack

class Particle:
    def __init__(self, gl_index=0, gl_color=vec4(1.,1.,1.,1.) , mass=1., r=[0., 0., 0.], v=[0., 0., 0.], a=[0., 0., 0.], f=[0., 0., 0.], pot=[0., 0., 0.], radii=0.002):
        self.gl_index = gl_index # index for OpenGL display list
        self.gl_color = gl_color
        self.m  = mass
        self.r = [r[i] for i in range (0, 3)]
        self.v = [v[i] for i in range (0, 3)]
        self.a = [a[i] for i in range (0, 3)]
        self.f = [f[i] for i in range (0, 3)]
        self.pot = [pot[i] for i in range (0, 3)]
        self.radii = radii


viewer = Viewer()
sparams = Simulation_Parameters()


def nbody_init():
    global particles, sparams, viewer

    sparams.sim_box_min   = [ -7.0, -7.0,  -7.0]
    sparams.sim_box_max   = [  7.0,  7.0,   7.0]
    sparams.scale = 0.01
    sparams.dt = 0.003
    sparams.limit = 100.0
    viewer.sphere_radius_coef = 144.0
    viewer.sphere_slic = 16
    viewer.sphere_stack = 16

    xmax = sparams.sim_box_max[0]
    xmin = sparams.sim_box_min[0]
    ymax = sparams.sim_box_max[1]
    ymin = sparams.sim_box_min[1]
    zmax = sparams.sim_box_max[2]
    zmin = sparams.sim_box_min[2]

    for i in range(4):
        p = Particle()
        p.r[0] = random.uniform(xmin, xmax)
        p.r[1] = random.uniform(ymin, ymax)
        p.r[2] = random.uniform(zmin, zmax)
        p.v[0] = p.v[1] = p.v[2] = 0.0
        logger.debug("%.2f, %.2f, %.2f" % (p.r[0], p.r[1], p.r[2]))
        particles.append(p)

    logger.debug("# of particles: %d", len(particles))


def calculate_force():
    global particles

    ieps2 = 1.0e-4

    for pi in particles:
        pi.a = [0., 0., 0.]

    npar = len(particles)

    for i in range(npar):
        pi = particles[i]
        for j in range(i+1, npar):
            pj = particles[j]
            dr = [ (pj.r[k] - pi.r[k]) * sparams.scale for k in range(len(pi.r)) ]
            r  = math.sqrt( dr[0]*dr[0] + dr[1]*dr[1] + dr[2]*dr[2] + ieps2)
            r1i = 1.0/r
            r2i = r1i * r1i
            r3i = r1i * r2i
            dr3 = [dr[0]*r3i, dr[1]*r3i, dr[2]*r3i] 
            for dim in range(3):
                pi.a[dim] += dr3[dim] * pj.m     # i-th particle
                pj.a[dim] -= dr3[dim] * pi.m     # j-th particle

#    for p in particles: print p.gl_index, p.a

# periodic boundary
def _calculate_boundary_condition():
    global particles
    c_min = sparams.sim_box_min
    c_max = sparams.sim_box_max

    for pi in particles:
        for k in range(3):
            r = c_max[k]-c_min[k]
            if ( pi.r[k] < c_min[k] ):
                pi.r[k] = pi.r[k] + r
            if ( pi.r[k] > c_max[k] ):
                pi.r[k] = pi.r[k] - r

# hard wall
def calculate_boundary_condition():
    global particles
    c_min = sparams.sim_box_min
    c_max = sparams.sim_box_max

    for pi in particles:
        for k in range(3):
            r = c_max[k]-c_min[k]
            if ( pi.r[k] < c_min[k] ):
                pi.v[k] = -pi.v[k]
            if ( pi.r[k] > c_max[k] ):
                pi.v[k] = -pi.r[k]

def time_integration():
    time_integration_LeapFrog2ndOrder()

# 2nd order Leapfrog (Velocity Verlet scheme) integration
is_first_integral=True
def time_integration_LeapFrog2ndOrder():
    global particles
    global is_first_integral

    dt = sparams.dt

    if is_first_integral is True:
        calculate_force()
        calculate_boundary_condition()
        is_first_integral = False

    for pi in particles:
        if viewer.is_3D is not True:
            pi.r[2] = 0.0
            pi.v[2] = 0.0
        pi.v = [ pi.v[k] + pi.a[k] * dt * 0.5 for k in range(0,3) ]
        pi.r = [ pi.r[k] + pi.v[k] * dt for k in range(0,3) ]

    calculate_force()
    calculate_boundary_condition()

    for pi in particles:
        pi.v = [ pi.v[k] + pi.a[k] * dt * 0.5 for k in range(0,3) ]

    viewer.sim_time += dt
    viewer.sim_step += 1


# 1st order Euler integration
def time_integration_Euler1stOrder():
    global particles

    dt = sparams.dt

    calculate_force()
    calculate_boundary_condition()

    for pi in particles:
        if viewer.is_3D is not True:
            pi.r[2] = 0.0
            pi.v[2] = 0.0
        pi.v = [ pi.v[k] + pi.a[k] * dt for k in range(0,3) ]
        pi.r = [ pi.r[k] + pi.v[k] * dt for k in range(0,3) ]

    viewer.sim_time += dt
    viewer.sim_step += 1



def simulate():
    global particles
    time_integration()

def  _glutSolidSphere(radius):
        glutSolidSphere(radius*viewer.sphere_radius_coef, viewer.sphere_slic, viewer.sphere_stack)

def add_particle():
    global particles, viewer
    r_box = sparams.sim_box_max[0] - sparams.sim_box_min[0]
    p = Particle()

    for k in range(3):
        p.r[k] = random.uniform(-0.5, 0.5) * r_box
        p.v[k] = 0.
        p.a[k] = 0.

    p.gl_color  = vec4(random.random(), random.random(), random.random(), 0.0)
    p.gl_index = glGenLists(1)
    glNewList(p.gl_index, GL_COMPILE)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, p.gl_color)
    _glutSolidSphere(p.radii)
    glEndList()
    particles.append(p)


def del_particle():
    global particles
    if 0 < len(particles):
        particles.pop()


def reset_pos_vel_acc():
    global particles
    
    r_box = sparams.sim_box_max[0] - sparams.sim_box_min[0]

    for p in particles:
        for dim in range(3):
            p.r[dim] = (0.5 - random.random()) * r_box
            p.v[dim] = (0.5 - random.random()) * sparams.limit/16.


tStart = t0 = time.time()
frames = 0

def framerate():
    global t0, frames, viewer
    t = time.time()
    frames += 1
    if t - t0 >= 1.0:
        seconds = t - t0
        fps_calc = frames/seconds
        fps_phys =  viewer.sim_time/(t - tStart)
#        print "%.0f frames in %3.1f seconds = %6.3f FPS" % (frames,seconds,fps_calc)
        t0 = t
        frames = 0
        viewer.fps_calc = fps_calc
        viewer.fps_phys = fps_phys


def draw_text_left_top():
    global particles

    text_list = [ ]
    if viewer.is_3D: 
        text_list.append( "simulation mode: 3D" )
    else:
        text_list.append( "simulation mode: 2D" )
    text_list.append( "simulation time : %f" % viewer.sim_time )
    text_list.append( "simulation steps: %d" % viewer.sim_step )
    text_list.append( "FPS:       %f" % viewer.fps_calc )
    text_list.append( "FPS(Phys): %f" % viewer.fps_phys )
    text_list.append( "# of particles: %d" % len(particles) )
    text_list.append( "dt: %.2e" % sparams.dt)
    text_list.append( "number of particles: %d" % len(particles))

    glColor4f( 1.0, 1.0, 0.5, 1.0 )
    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glTranslatef(-.9, .8, 0)
    glScalef(.0006, .0006, 1)

    y = 10

    for s in text_list:
        glRasterPos2f(2.0, y)
        y -= 47.
        for c in s:
            glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(c))

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)

def draw_text_left_down():
    text_list = [ ]
    text_list.append( "--- Keybind ---")
    text_list.append( "k: rotate simulation box")
    text_list.append( "j: rotate simulation box")
    text_list.append( "[Space]: increase particles")
    text_list.append( "-: reduce particles")
    text_list.append( "q: quit")

    glColor4f( 1.0, 1.0, 0.5, 1.0 )
    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glTranslatef(-.9, .8, 0)
    glScalef(.0006, .0006, 1)

    y = -2600

    for s in text_list:
        glRasterPos2f(2.0, y)
        y -= 53.
        for c in s:
            glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(c))

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)

def draw_box():
    c_min = sparams.sim_box_min
    c_max = sparams.sim_box_max

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


def update():
    global viewer
    istep = viewer.sim_step
    simulate()
    draw()


def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0.0, 15.0, -0.5*viewer.trans[2]-30., # position of camera
              0.0,  0.0, 0.0,                  # position of center
              0.0,  1.0, 0.0)                  # direction of Up
    glPushMatrix()
    glRotatef(viewer.view_rot[0], 1.0, 0.0, 0.0)
    glRotatef(viewer.view_rot[1], 0.0, 1.0, 0.0)
    glRotatef(viewer.view_rot[2], 0.0, 0.0, 1.0)

    for i in range(0, len(particles)):
        p = particles[i]
        glPushMatrix()
        glTranslatef(p.r[0], p.r[1], p.r[2])
        glCallList(p.gl_index)
        _glutSolidSphere(p.radii)
        glPopMatrix()

    draw_box()
    glPopMatrix()

    draw_text_left_top()
    draw_text_left_down()
    glutSwapBuffers()

    framerate()

def idle():
    glutPostRedisplay()



def decrease_velocity():
    global particles
    logger.info("decreasing velocity")

    for p in particles:
        for k in range(3): p.v[k] = p.v[k] * 0.9

def increase_velocity():
    global particles
    logger.info("increasing velocity")

    for p in particles:
        for k in range(3): p.v[k] = p.v[k] * 1.1


# change view angle, exit upon ESC
def key(k, x, y):
    global viewer, sparams, particles

    if k == 'k':
        viewer.view_rot[2] += 5.0
    elif k == 'j':
        viewer.view_rot[2] -= 5.0

    elif k == 'i':
        viewer.view_rot[0] -= 5.0
    elif k == 'u':
        viewer.view_rot[0] += 5.0

    elif k == 't':  # cahnge the box size
        sparams.dt *= 0.8
        logger.info(sparams.dt)
    elif k == 'T':  # cahnge the box size
        sparams.dt += 0.0001
        logger.info(sparams.dt)
    elif k == 'J':  # cahnge the box size
        sparams.sim_box_min   = [ sparams.sim_box_min[k] / 1.3 for k in  range(3)]
        sparams.sim_box_max   = [ sparams.sim_box_max[k] / 1.3 for k in  range(3)]
    elif k == 'K':  # cahnge the box size
        sparams.sim_box_min   = [ sparams.sim_box_min[k] * 1.3 for k in  range(3)]
        sparams.sim_box_max   = [ sparams.sim_box_max[k] * 1.3 for k in  range(3)]
    elif k == 'r':
        reset_pos_vel_acc()
    elif k == 'o':
        for p in particles:
            if 0.0 < p.radii: p.radii -= 1e-4
        logger.info(particles[0].radii)

    elif k == 'O':
        for p in particles:
            if 10.0 > p.radii: p.radii += 1e-4
        logger.info(particles[0].radii)

    elif k == ' ':
        add_particle()
    elif k == '-':
        del_particle()
    elif k == '1':
        logger.info("r,v,a:\n\t%s\n\t%s\n\t%s" % (particles[0].r,particles[0].v,particles[0].a))
    elif k == 'h':
        for s in help_msg: print s
    elif k == '2':
        if viewer.is_3D:
            print "3D -> 2D"
            viewer.is_3D = False
        else:
            print "2D -> 3D"
            viewer.is_3D = True
    elif k == 'v':
        decrease_velocity()
    elif k == 'V':
        increase_velocity()
    elif k == '9':
        viewer.sphere_radius_coef *= 1.2
        print "sphere_radius_coef:", viewer.sphere_radius_coef
    elif k == '0':
        viewer.sphere_radius_coef /= 1.2
        print "sphere_radius_coef:", viewer.sphere_radius_coef
    elif k == 'q':
        sys.exit(0)
    elif ord(k) == 27: # Escape
        sys.exit(0)
    else:
        return

    glutPostRedisplay()


# change view angle
def special(k, x, y):
    global viewer, sparams

    if k == GLUT_KEY_UP:
        viewer.view_rot[0] += 5.0
    elif k == GLUT_KEY_DOWN:
        viewer.view_rot[0] -= 5.0
    elif k == GLUT_KEY_LEFT:
        viewer.view_rot[1] += 5.0
    elif k == GLUT_KEY_RIGHT:
        viewer.view_rot[1] -= 5.0
    else:
        return

    glutPostRedisplay()

def mouse(button, state, x, y):
    global mpos, viewer

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

def motion(x, y):
    global viewer, sparams

    print "motion: ", x, y, viewer.trans
    if viewer.mouse_l == 1 :
        speed = 1.2
        viewer.view_rot[0] = (y - viewer.mpos[1]) * speed
        viewer.view_rot[2] = (x - viewer.mpos[0]) * speed
    elif viewer.mouse_r == 1:
        viewer.trans[1] += (x - viewer.mpos[0]) * 0.01
        viewer.trans[2] -= (y - viewer.mpos[1]) * 0.01
        print viewer.trans

    if viewer.mouse_l ==1 or viewer.mouse_m == 1 or viewer.mouse_r == 1:
        glutPostRedisplay()


def reshape(width, height):
    h = float(height) / float(width)
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, h, 0.1, 1000.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -40.0)


def init():
    global particles


    random.seed(3141592653589793238462643383279502884)
    pos   = vec4(-5.0, -5.0, 10.0, 0.0)
    red   = vec4(0.8, 0.1, 0.0, 1.0)
    green = vec4(0.0, 0.8, 0.2, 1.0)
    blue  = vec4(0.2, 0.2, 1.0, 1.0)

    glLightfv(GL_LIGHT0, GL_AMBIENT, vec4(0.5, 0.1,  -0.1, 0.1))
    glEnable(GL_CULL_FACE)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)

    nbody_init()

    for p in particles:
        p.gl_color  = vec4(random.random(), random.random(), random.random(), 0.0)
        p.gl_index = glGenLists(1)
        glNewList(p.gl_index, GL_COMPILE)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, p.gl_color)
        _glutSolidSphere(p.radii)
        glEndList()

    glEnable(GL_NORMALIZE)


def visible(vis):
    if GLUT_VISIBLE == vis:
        glutIdleFunc(idle)


if __name__ == '__main__':
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)

    glutInitWindowPosition(800, 0)
    glutInitWindowSize(800, 800)
    glutCreateWindow("GRAVpy")
    init()

    glutDisplayFunc(update)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(key)
    glutSpecialFunc(special)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)
    glutVisibilityFunc(visible)

    if "--info" in sys.argv:
        logger.info("GL_RENDERER   = %s", glGetString(GL_RENDERER))
        logger.info("GL_VERSION    = %s", glGetString(GL_VERSION))
        logger.info("GL_VENDOR     = %s", glGetString(GL_VENDOR))
        logger.info("GL_EXTENSIONS = %s", glGetString(GL_EXTENSIONS))

    glutMainLoop()

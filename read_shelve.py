#!/usr/bin/env python
# Time-stamp: <2017-01-15 05:28:54 hamada>
# read_shelve.py
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
import shelve
import pickle

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

vec4 = GLfloat_4
particles = [ ]

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

def read_shelve(fname='/tmp/grav.dump', logger=None):
    global particles
    particles = [ ]

    pickle_protocol = pickle.HIGHEST_PROTOCOL
    try:
        dic = shelve.open(fname, protocol=pickle_protocol)
    except Exception as e:
        logger.error(str(type(e)))
        logger.error(str(e.args))
        logger.error(e.message)
        logger.error(fname)
        sys.exit(-1)

    n = dic['n_particles']
    for i in range(n):
        p = Particle()
        [p.r, p.v] = dic["key%d"%i]
        particles.append(p)
    dic.close()


    print n
    for p in particles:
        print p.r, p.v

    return True


if __name__ == '__main__':
    logger = create_logger()
    read_shelve('/tmp/grav.dump', logger)

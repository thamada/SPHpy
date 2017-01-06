#!Time-stamp: <2017-01-07 07:44:50 hamada>


all:
	@echo 'Smoothed Particle Hydrodynamics simulation -> ./sph.py [ENTER]'
	@echo 'Gravitational N-body simulation -> ./grav.py [ENTER]'
	@echo 'check your system whether OpenGL is available or not: ./ogl-check.py [ENTER]'

sph:
	./spy.py


grav:
	./grav.py

opengl:
	./ogl-check.py


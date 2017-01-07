#!Time-stamp: <2017-01-08 01:13:48 hamada>

# SPHpy:
Smoothed Particle Hydrodynamics written in python.

## Requirements

- python 2.7.x
- pyOpenGL


## Applications

- sph.py : SPHpy itself for Smoothed Particle Hydrodynamics written in python.
- grav.py : another app for gravitational N-body simulation written in python.
- ogl-check.py : pyOpenGL example for checking your system works fine or not.


## Usage 

```python:sphy.py
ubuntu:~/SPHpy$ ./sph.py [ENTER]
```

```python:grav.py
ubuntu:~/SPHpy$ ./grav.py [ENTER]
```

```python:ocl-check.py
ubuntu:~/SPHpy$ ./ocl-check.py [ENTER]
```


## Keybind

- k: rotate simulation box
- j: rotate simulation box
- J: box size --
- K: box size ++
- t: dt--
- T: dt++
- r: shuffle particles
- e: wall(e) --
- E: wall(e) ++
- v: viscosity ++
- V: viscosity --
- [Space]: increase particles
- -: reduce particles
- 1: for debug
- 2: change 3D->2D
- q: quit
- h: show this message


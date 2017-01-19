Time-stamp: <2017-01-20 03:00:34 hamada>

# SPHpy:
Smoothed Particle Hydrodynamics simulation written in python.

## Requirements

- python 3.6.x
- pyOpenGL


## Applications

- sph.py : SPHpy itself for Smoothed Particle Hydrodynamics simulation written in python.
- grav.py : gravitational N-body simulation written in python.
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

## Target users

schoolchildren, and absolutery not for N-body/SPH experts


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

## References

- [Gingold R. A., Monaghan, J. J., 1977, MNRAS, 181, 375](http://mnras.oxfordjournals.org/content/181/3/375.abstract)
- [Lucy L., 1977, AJ, 82, 1013](http://adsabs.harvard.edu/abs/1977AJ.....82.1013L)
- [Trenti, M., Hut, P., 2008, Scholarpedia, 3(5):3930](http://www.scholarpedia.org/article/N-body_simulations_(gravitational))

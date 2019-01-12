chaosmagpy
==========

This is a simple python package for evaluating the CHAOS geomagnetic field model.

Refs
----
Finlay, C.C., Olsen, N., Kotsiaros, S., Gillet, N. and Toeffner-Clausen, L.
(2016), Recent geomagnetic secular variation from Swarm and ground observatories
as estimated in the CHAOS-6 geomagnetic field model Earth Planets Space,
Vol 68, 112. doi: 10.1186/s40623-016-0486-1

Olsen, N., Luehr, H., Finlay, C.C., Sabaka, T. J., Michaelis, I., Rauberg, J.
and Toeffner-Clausen, L. (2014), The CHAOS-4 geomagnetic field model,
Geophys. J. Int., Vol 197, 815-827, doi: 10.1093/gji/ggu033.

Olsen, N.,  Luehr, H.,  Sabaka, T.J.,  Mandea, M. ,Rother, M., Toeffner-Clausen, L.
and Choi, S. (2006), CHAOS—a model of Earth's magnetic field derived from CHAMP,
Ørsted, and SAC-C magnetic satellite data, Geophys. J. Int., vol. 166 67-75

Installation
============

1. Install the following packages for example with conda:

	>>> conda install python numpy scipy pandas cython cartopy matplotlib=2

   (At the moment, you need matplotlib 2 as pcolormesh is not working with the
   current cartopy release. But it will be hopefully updated soon.)

2. Install cdflib with pip:

    >>> pip install cdflib

3. Finally install chaosmagpy-x.x (replace 'x' with version) from the archive:

	>>> pip install chaosmagpy-x.x.tar.gz

Contents
========

The directory contains the files/directories:

1. "chaosmagpy-x.x.tar.gz": pip installable archive of the chaospy package
   (version x.x)

2. "chaos_examples.py": executable Python script containing several examples
   that can be run by changing the examples in line 16, save and run in the
   command line:

   >>> python chaos_examples.py

   example 1: Calculate CHAOS model field predictions from input coordinates
              and time and output simple data file
   example 2: Calculate and plot residuals between between CHAOS model and
              Swarm A data (from L1b MAG pdf data file, example from May 2014).
   example 3: Calculate core field and its time derivatives for specified times
              and radii and plot maps
   example 4: Calculate static (i.e. small-scale crustal) magnetic field and
              plot maps
   example 5: Calculate timeseries of the magnetic field at a ground
              observatory and plot
   example 6: Calculated external and associated induced fields described in SM
              and GSM reference systems and plot maps

3. "data/CHAOS-6-x7.mat": mat-file containing CHAOS-6 model (extension 7)

4. "SW_OPER_MAGA_LR_1B_20140502T000000_20140502T235959_0505_MDR_MAG_LR.cdf":
   cdf-file containing Swarm A magnetic field data from May 2, 2014.

5. directory called "html" containing the built documentation as
   html-files. Open "index.html" in your browser to access the main site.


Clemens Kloss (ancklo@space.dtu.dk)


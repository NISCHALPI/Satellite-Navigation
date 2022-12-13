# Satellite Navigation and Reciver Triangulation

This python based project is design to read and process RINEX files. The dependencies of this 
project are [GeoRinex](https://pypi.org/project/georinex/)-a rinex parser, [NumPy](https://numpy.org/)- scientific computation, and optional [Manim](https://docs.manim.community/en/stable/) -animation library.


The RINEX files 
are available in the following NASA website,

[Download Rinex Files](https://cddis.nasa.gov/Data_and_Derived_Products/GNSS/RINEX_Version_3.html)




## Installation

To install, just clone the repositery and use the triangulate.py script.
```bash
git clone https://github.com/NISCHALPI/Satellite-Navigation

```


## Triangulation Script

```bash
Command : python triangulate.py --help

--------------------------------------------------------------------------------------
usage: triangulate.py [-h] [-o OBS] [-n NAV] [-c COMPUTE] [-a]

Triangulate GPS reciever coordinate using RINEX files!

options:
  -h, --help            show this help message and exit
  -o OBS, --obs OBS     Path to RINEX observation file
  -n NAV, --nav NAV     Path to RINEX navigation file
  -c COMPUTE, --compute_mode COMPUTE
                        Choose a compute mode : <thread> ot <process>
  -a, --auto            Auto Read Rinex files from data directory

----------------------------------------------------------------------------------------
```

To use the script, user need two RINEX files observation and navigation files. Two sample files are
provided in data directory.

Either user can pass the full path of the RINEX files using command line args or use the --auto flag to
automatically read rinex file in data directory- only two files should be in the data directory at runtime. The 
observation file should have "MO" in fillename and navigation must "GN".

```bash
python triangulate.py --auto

```

However, user can also pass the rinex file path to the argument. 

```bash
python triangulate.py --obs <full_path_to_observation_file> --nav <full_path_to_navigation_file>

```

The compute mode option can be either set to thread (default) or process.

```bash
python triangulate.py --compute process --obs <full_path_to_observation_file> --nav <full_path_to_navigation_file>

```



## Animation Script 

User can animate the orbital path and satellite position using this script. 

```bash


'''

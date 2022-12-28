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

Create a conda environment using the dependencies listed in dependencies directory,

```bash
conda create -n navPy --file dependencies/environment.yml 

```
For the animation script to work, you will need specific version of manim , numpy,  moderngl and GPU,
```Text
manim==0.16.0.post0
moderngl==5.6.4
numpy==1.21.6
```

## Triangulation Script

```bash
Command : python triangulate.py --help

--------------------------------------------------------------------------------------
Usage: triangulate.py [OPTIONS]

  Triangulate GPS reciever coordinate using RINEX files!

Options:
  -n, --nav PATH                  Path to RINEX navigation file
  -o, --obs PATH                  Path to RINEX observational file
  -c, --compute [thread|process]  Choose a compute mode
  -a, --auto                      Read data automatically from ./data/
                                  directry
  -q, --quite                     Only prints reciever coordinate to stdout
  --help                          Show this message and exit.
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
python animate.py --help
--------------------------------------------------------------------------------------
Usage: animate.py [OPTIONS]

  Animate GPS satellite path and find satellite coordinate from brodcast
  ephimeris

Options:
  -n, --nav PATH    Path to RINEX navigation file  [required]
  -a, --auto        Choose epoch automatically for Animation
  -s, --sv TEXT     Select specific SV's
  --no-axis         Turn off axis
  --trajectory      Show the trajectory
  -t, --time FLOAT  animation time (default: 8 sec)
  --no-legend       Toggle Legend
  --help            Show this message and exit.
----------------------------------------------------------------------------------------
```
For example, use the script to animate satellite coordinate and trajectory using a sample RINEX file
```bash
python animate.py -n data2/MADR00ESP_R_20220390000_01D_GN.rnx  --auto --time 12 --no-axis --trajectory
```
Animation would look something like this, 

https://user-images.githubusercontent.com/60031022/209759494-083191ed-a7ea-4671-8bad-ad276a4a8bc4.mp4

Users can toggle trjectory and legend in animation. If you know manim, feel free to edit the internal of animation script to suite your needs.







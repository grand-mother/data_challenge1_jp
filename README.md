REAStoROOT converter
===========================

Basic Info
-----------

**How to run**

Run:
python REAStoROOTconverter.py -d <directory_with_corsika_files>

It will generate a _SIM000000.root_ file containing the trees RunTree, ADCEventTree, VoltageEventTree, EfieldEventTree and ShowerEventTree in the specified directory. 

**How to read**

After generating the _SIM000000.root_ file you can read it using one of the root file readers we have. For example:

python DataReadingExample.py SIM000000.root


**warning**

If a parameter is stored as "1111", it (most likely) means that it was not found in the loaded SIM.reas file.


Corsika Parameters
-------------------
This is a brief overview of which parameters we get from which Corsika files.

**SIM.reas**
The main shower info, such as:

TimeResolution - in s
AutomaticTimeBoundaries - 0: off, x: automatic boundaries with width x in s
TimeLowerBoundary - in s, only if AutomaticTimeBoundaries set to 0
TimeUpperBoundary - in s, only if AutomaticTimeBoundaries set to 0
ResolutionReductionScale - 0: off, x: decrease time resolution linearly every x cm in radius
GroundLevelRefractiveIndex - specify refractive index at 0 m asl
EventNumber
RunNumber
GPSSecs
GPSNanoSecs         
RotationAngleForMagfieldDeclination - in degrees
ShowerZenithAngle - in degrees
ShowerAzimuthAngle - in degrees, 0: shower propagates to north, 90: to west
PrimaryParticleEnergy - in eV
PrimaryParticleType - as defined in CORSIKA
DepthOfShowerMaximum - slant depth in g/cm^2
DistanceOfShowerMaximum - geometrical distance of shower maximum from core in cm
MagneticFieldStrength - in Gauss
MagneticFieldInclinationAngle - in degrees, >0: in northern hemisphere, <0: in southern hemisphere
GeomagneticAngle - in degrees

**RUN.inp**
Extra information that was used to generate the shower simulation. Might be interesting for ensuring ZhaireS compatability.

**SIM.list**
Antenna positions

**SIM_coreas/raw.dat**
Traces for each antenna

**DAT.long**
Energy deposit and particle numbers

**RUN.log**
The log of the simulation run. Contains the Corsika version and configuration, interaction models, etc.

# FERC -- Translate a (lon,lat) point to a Flynn-Engdahl region code.

This is code transliterated by G. Helffrich 24 July 2022, from perl into
Python based on the version at
[ftp://hazards.cr.usgs.gov/feregion/fe_1995/feregion.pl](ftp://hazards.cr.usgs.gov/feregion/fe_1995/feregion.pl)
```
   Perl Version 0.2 - Bob Simpson January, 2003 <simpson<at>usgs.gov>
   With fix supplied by George Randall <ger<at>geophysics.lanl.gov> 2003-02-03
```

It uses the 1995 revision of F-E region definitions.

## Usage

```
class FERC():
    '''
    ## FERC class - Convert a lat/lon pair to a region code name and/or number.

    Public methods:
       code(lon=, lat=):  Return region code (integer) for given (lat,lon).
       name(lon=, lat=):  Return region name (string) for given (lat,lon).
       codename(lon=, lat=):  Return region (code,name) as tuple for given
          (lat,lon).

    Usage:
       from ferc import FERC

       reg = FERC()
       code = reg.code(...)
       name = reg.name(...)
       (code,name) = reg.codename(...)
    '''
```

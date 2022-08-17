## FERC -- Translate (lon,lat) to Flynn-Engdahl region code.
##         Code pythonified and transliterated from perl version at
##             ftp://hazards.cr.usgs.gov/feregion/fe_1995/feregion.pl
##         by G. Helffrich 24 July 2022.
##
##         Perl Version 0.2 - Bob Simpson January, 2003 <simpson<at>usgs.gov>
##             With fix supplied by George Randall <ger<at>geophysics.lanl.gov>
##             2003-02-03
##
##         1995 revision of F-E region definitions.

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

    # Names of files containing Flinn-Engdahl Regionalization info.
    names = "names.asc"
    quadsindex = "quadsidx.asc";
    quadorder = [
        ("ne", "nesect.asc"), ("nw", "nwsect.asc"),
        ("se", "sesect.asc"), ("sw", "swsect.asc")
    ]

    def __init__(self):
        # Read the file of region names...
        NAMES = open(FERC.names,'rb')
        self.names = NAMES.readlines()
        NAMES.close()
        self.nstrp = bytearray(len(self.names)) # name strip() & decode() later

        # The quadsindex file contains a list for all 4 quadrants of the number
        # of longitude entries for each integer latitude in the "sectfiles".
        QUADSINDEX, quadsindex = open(FERC.quadsindex,'rb'), []
        for l in QUADSINDEX.readlines():
            for itm in l.decode('utf-8').split():
                quadsindex.append(int(itm))
        QUADSINDEX.close()
        if len(quadsindex) % 91 != 0:
            raise RuntimeError("**Corrupt quads index file.")

        self.lonsperlat, self.latbegins = dict(), dict()
        self.lons, self.fenums = dict(), dict()
        for (quad, file) in FERC.quadorder:
            # Break the quadindex array into 4 arrays, one for each quadrant.
            self.lonsperlat[quad] = quadsindex[0:91]
            del quadsindex[0:91]

            # Convert the lonsperlat array, which counts how many longitude
            # items there are for each latitude, into an array that tells the
            # location of the beginning item in a quadrant's latitude stripe.
            end, self.latbegins[quad] = -1, []
            for item in self.lonsperlat[quad]:
                self.latbegins[quad].append(end+1)
                end += item

            SECTFILE, self.lons[quad], self.fenums[quad] = open(file,'rb'),[],[]
            for l in SECTFILE.readlines():
                itms = l.decode('utf-8').split()
                if len(itms) % 2 != 0:
                    raise RuntimeError(
                        "**Corrupt %s sector file (format)." % quads
                    )
                for i in range(0,len(itms),2):
                    # input is pairs of (lon, code) values
                    ferc = int(itms[i+1])
                    if ferc < 0 or ferc > len(self.names):
                        raise RuntimeError(
                            "**Corrupt %s sector file (region code)." % quads
                        )
                    self.lons[quad].append(int(itms[i]))
                    self.fenums[quad].append(ferc)
            SECTFILE.close()

    def _strip(self,num):
        # Strip region name of trailing \n & decode if not already done.
        n = num-1
        if self.nstrp[n:num] == b'\x00':
            self.names[n] = self.names[n].strip().decode('utf-8')
            self.nstrp[n:num] = b'\x01'
        return self.names[n]

    def code(self,lat=None,lon=None):
        if lon<= -180: lon += 360
        if lon > +180: lon -= 360

        # Take absolute values...
        alat = abs(lat)
        alon = abs(lon)
        if alat > 90.0 or alon > 180.0:
            raise ValueError

        # Truncate absolute values to integers...
        lt = int(alat)
        ln = int(alon)

        # Get quadrant
        if lat >= 0.0 and lon >= 0.0: quad = "ne"
        if lat >= 0.0 and lon <  0.0: quad = "nw"
        if lat <  0.0 and lon >= 0.0: quad = "se"
        if lat <  0.0 and lon <  0.0: quad = "sw"

        # Find location of the latitude tier in the appropriate quadrant file.
        beg = self.latbegins[quad][lt]  # Loc. of first item for latitude lt.
        num = self.lonsperlat[quad][lt] # Number of items for latitude lt.
        rng = slice(beg,beg+num)

        # Extract this tier of longitude and f-e numbers for latitude lt.
        lons = self.lons[quad][rng]
        fenums = self.fenums[quad][rng]

        # Find region number extending up to requested longitude
        for n in range(num):
            if lons[n] > ln: break
        else:
            n = num
        ferc = fenums[n-1]
        del rng, lons, fenums
        return ferc

    def name(self,lat=None,lon=None):
        return self._strip(self.code(lat,lon))

    def codename(self,lat=None,lon=None):
        num = self.code(lat,lon)
        return (num, self._strip(num))

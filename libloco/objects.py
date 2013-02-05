from .structs import auxdesc, objclass, objdesc, varinf
from .helper import descnumspec, descnumif, descnumand, descnumuntil

spriteflags = [
	"hasdata", "", "chunked", "",
	"", "", "copy", "",
]

namealiases = {
	'wideslope': 'steepslope',
	'curvetypes': 'trackpieces',
	'salecostfact': 'sellcostfact',
	'numdata': 'numaux01',
	'numaux2ent': 'numtiles',
	'numaux4': 'numnodes',
	'numaux5': 'numedges',
	'approach': 'flight',
	'helitakeoff': 'helibegin',
	'heliland': 'heliend',
	'takeoff': 'touchdown',
}

nobits = []

# ***********************
#  SIMPLE CLASS HANDLER
# ***********************

simplevars = [
	varinf( 0x00, 1, 6, "" )
]
simpledesc = [
	objdesc( 'desc_objdata' ),
	objdesc( 'desc_lang', [ 0 ] ),
	objdesc( 'desc_sprites' )
]

# ***********************
# Class 00:  INTERFACES
# ***********************

interfacevars = [
	varinf( 0x00, 1, 24, "" )
]


# ***********************
# Class 01:  SOUNDS
# ***********************

sfxvars = [
	varinf( 0x00, 1, 8, "" ),
	varinf( 0x08,-4, 1, "" )
]

sfxdesc = [
	objdesc( 'desc_objdata' ),
	objdesc( 'desc_lang', [ 0 ] ),
	objdesc( 'desc_sounds' ),
]

# ***********************
# Class 02:  CURRENCIES
# ***********************

currvars = [
	varinf( 0x00, 1, 10, "" ),
	varinf( 0x0A, 1, 1, "zeroes" ),
	varinf( 0x0B, 1, 1, "shiftnum" )
]

currdesc = [
	objdesc( 'desc_objdata' ),
	objdesc( 'desc_lang', [ 0 ] ),
	objdesc( 'desc_lang', [ 1 ] ),
	objdesc( 'desc_lang', [ 2 ] ),
	objdesc( 'desc_sprites' ),
]

# ***********************
# Class 03:  EXHAUST FX
# ***********************

exhfxvars = [
	varinf( 0x00, 1, 30, "" ),
	varinf( 0x1E, 1, 1, "numsnd" ),
	varinf( 0x1F, 1, 9, "" ),
]

exhfxaux = [
	auxdesc( "", None ),
	auxdesc( "", None ),
]

exhfxdesc = [
	objdesc( 'desc_objdata' ),
	objdesc( 'desc_lang', [ 0 ] ),
	objdesc( 'desc_auxdatavar', [ 0, 0, 2, 1 ] ),
	objdesc( 'desc_auxdatavar', [ 1, 0, 2, 1 ] ),
	objdesc( 'desc_useobj', [ 0xFFFFFFE2, 'soundeffect', 0x01 ] ), # FFFF FFE2 == -0x1e
	objdesc( 'desc_sprites' ),
]

# ***********************
# Class 04:  CLIFF FACES
# ***********************

# (see simple vars above)

# ***********************
# Class 05:   WATER
# ***********************

watervars = [
	varinf( 0x00, 1, 2, "" ),
	varinf( 0x02, 1, 1, "costind" ),
	varinf( 0x03, 1, 1, "" ),
	varinf( 0x04,-2, 1, "costfactor" ),
	varinf( 0x06, 1, 8, "" ),
]


# ***********************
# Class 06:  GROUND
# ***********************

groundvars = [
	varinf( 0x00, 1, 2, "" ),
	varinf( 0x02, 1, 1, "costind" ),
	varinf( 0x03, 1, 5, "" ),
	varinf( 0x08,-2, 1, "costfactor" ),
	varinf( 0x0A, 1, 20, "" ),
]

grounddesc = [
	objdesc( 'desc_objdata' ),
	objdesc( 'desc_lang', [ 0 ] ),
	objdesc( 'desc_useobj', [ 0, 'cliff', 0x04, -1 ] ),
	objdesc( 'desc_sprites' ),
]

# ***********************
# Class 07:  TOWN NAMES
# ***********************

townpart = [
	varinf( 0x00, 1, 1, "num" ),
	varinf( 0x01, 1, 1, "numempty" ),
	varinf( 0x02, 2, 1, "indexofs" ),
]

townvars = [
	varinf( 0x00, 1, 2, "" ),
	varinf( 0x02, 4, 6, "part", townpart ),
]

towndesc = [
	objdesc( 'desc_objdata' ),
	objdesc( 'desc_lang', [ 0 ] ),
	objdesc( 'desc_strtable', [ 0, 2+0*4, 4+0*4 ] ),
	objdesc( 'desc_strtable', [ 1, 2+1*4, 4+1*4 ] ),
	objdesc( 'desc_strtable', [ 2, 2+2*4, 4+2*4 ] ),
	objdesc( 'desc_strtable', [ 3, 2+3*4, 4+3*4 ] ),
	objdesc( 'desc_strtable', [ 4, 2+4*4, 4+4*4 ] ),
	objdesc( 'desc_strtable', [ 5, 2+5*4, 4+5*4 ] ),
]

# ***********************
# Class 08:  CARGO TYPES
# ***********************

cargoflags = [
	"", "refitoption",
]

cargovars = [
	varinf( 0x00, 1, 2, "" ),
	varinf( 0x02, 2, 1, "unitweight" ),
	varinf( 0x04, 1, 12, "" ),
	varinf( 0x10, 1, 1, "id" ),
	varinf( 0x11, 1, 1, "" ),
	varinf( 0x12, 1, 1, "flags", None, cargoflags ),
	varinf( 0x13, 1, 2, "" ),
	varinf( 0x15, 1, 1, "peakdays" ),
	varinf( 0x16, 1, 1, "decay1days" ),
	varinf( 0x17, 2, 1, "decay1rate" ),
	varinf( 0x19, 2, 1, "decay2rate" ),
	varinf( 0x1B, 2, 1, "paymentfactor" ),
	varinf( 0x1D, 1, 1, "paymentind" ),
	varinf( 0x1E, 1, 1, "" ),
]

cargodesc = [
	objdesc( 'desc_objdata' ),
	objdesc( 'desc_lang', [ 0 ] ),
	objdesc( 'desc_lang', [ 1 ] ),
	objdesc( 'desc_lang', [ 2 ] ),
	objdesc( 'desc_lang', [ 3 ] ),
	objdesc( 'desc_sprites' ),
]


# ***********************
# Class 09:    FENCES
# ***********************

fenceflags = [
]

fencevars = [
	varinf( 0x00, 1, 7, "" ),
	varinf( 0x07, 1, 1, "flags", None, fenceflags ),
	varinf( 0x08, 1, 1, "" ),
	varinf( 0x09, 1, 1, "" ),
]


# ***********************
# Class 0A:    SIGNALS
# ***********************

signalvars = [
	varinf( 0x00, 1, 6, "" ),
	varinf( 0x06,-2, 1, "costfactor" ),
	varinf( 0x08,-2, 1, "sellcostfactor" ),
	varinf( 0x0A, 1, 1, "costind" ),
	varinf( 0x0B, 1, 15, "" ),
	varinf( 0x1A, 2, 1, "designed" ),
	varinf( 0x1C, 2, 1, "obsolete" ),
]

signaldesc = [
	objdesc( 'desc_objdata' ),
	objdesc( 'desc_lang', [ 0 ] ),
	objdesc( 'desc_lang', [ 1 ] ),
	objdesc( 'desc_sprites' ),
]


# ***********************
# Class 0B:  CROSSINGS
# ***********************

crossingvars = [
	varinf( 0x00, 1, 2, "" ),
	varinf( 0x02,-2, 1, "costfactor" ),
	varinf( 0x04, 1, 2, "" ),
	varinf( 0x06, 1, 1, "costind" ),
	varinf( 0x07, 1, 11, "" ),
]


# ***********************
# Class 0C: STREET LIGHTS
# ***********************

lightvars = [
	varinf( 0x00, 1, 2, "" ),
	varinf( 0x02, 2, 3, "year" ),
	varinf( 0x08, 1, 4, "" ),
]


# ***********************
# Class 0D:    TUNNELS
# ***********************

# (see simplevars above)


# ***********************
# Class 0E:   BRIDGES
# ***********************

bridgevars = [
	varinf( 0x00, 1, 2, "" ),
	varinf( 0x02, 1, 1, "noroof" ),
	varinf( 0x03, 1, 1, "" ),
	varinf( 0x04, 1, 1, "" ),
	varinf( 0x05, 1, 1, "" ),
	varinf( 0x06, 1, 1, "" ),
	varinf( 0x07, 1, 1, "" ),
	varinf( 0x08, 1, 1, "spanlength" ),
	varinf( 0x09, 1, 1, "pillarspacing" ),
	varinf( 0x0A, 2, 1, "maxspeed" ),
	varinf( 0x0C, 1, 1, "maxheight" ),
	varinf( 0x0D, 1, 1, "costind" ),
	varinf( 0x0E,-2, 1, "basecostfact" ),
	varinf( 0x10,-2, 1, "heightcostfact" ),
	varinf( 0x12,-2, 1, "sellcostfact" ),
	varinf( 0x14, 2, 1, "disabledtrackcfg" ),
	varinf( 0x16, 1,22, "" ),
]


# ***********************
# Class 0F:  TRAIN STATIONS
# ***********************

track_pieces = [
	"diagonal", "widecurve", "mediumcurve", "smallcurve",	# 1 2 4 8
	"tightcurve", "normalslope", "steepslope", "",		# 10 20 40 80
	"slopedcurve", "sbend",					# 100 200
]

trnstatvars = [
	varinf( 0x00, 1, 4, "" ),
	varinf( 0x04, 2, 1, "trackpieces", None, track_pieces ),
	varinf( 0x06,-2, 1, "buildcostfact" ),
	varinf( 0x08,-2, 1, "sellcostfact" ),
	varinf( 0x0A, 1, 1, "costind" ),
	varinf( 0x0B, 1,23, "" ),
	varinf( 0x22, 1, 1, "numcompat" ),
	varinf( 0x23, 1, 7, "" ),
	varinf( 0x2a, 2, 1, "designed" ),
	varinf( 0x2c, 2, 1, "obsolete" ),
	varinf( 0x2e, 1, 128, "" ),
]

trnstataux = [
	auxdesc( "", None ),
]

trnstatdesc = [
	objdesc( 'desc_objdata' ),
	objdesc( 'desc_lang', [ 0 ] ),
	objdesc( 'desc_auxdatavar', [ 0, 32, 1, 4 ] ),
	objdesc( 'desc_sprites' ),
]


# ***********************
# Class 10:  TRACK MODS
# ***********************

trkmodvars = [
	varinf( 0x00, 1, 2, "" ),
	varinf( 0x02, 2, 1, "trackpieces", None, track_pieces ),
	varinf( 0x04, 1, 1, "isoverhead" ),
	varinf( 0x05, 1, 1, "costind" ),
	varinf( 0x06,-2, 1, "buildcostfact" ),
	varinf( 0x08,-2, 1, "sellcostfact" ),
	varinf( 0x0A, 1, 8, "" ),
]


# ***********************
# Class 11:   TRACKS
# ***********************

trackvars = [
	varinf( 0x00, 1, 2, "" ),
	varinf( 0x02, 2, 1, "trackpieces", None, track_pieces ),
	varinf( 0x04, 2, 1, "stationtrackpieces", None, track_pieces ),
	varinf( 0x06, 1, 1, "" ),
	varinf( 0x07, 1, 1, "numcompat" ),
	varinf( 0x08, 1, 1, "nummods" ),
	varinf( 0x09, 1, 1, "numsignals" ),
	varinf( 0x0A, 1, 10, "" ),
	varinf( 0x14,-2, 1, "buildcostfact" ),
	varinf( 0x16,-2, 1, "sellcostfact" ),
	varinf( 0x18,-2, 1, "tunnelcostfact" ),
	varinf( 0x1A, 1, 1, "costind" ),
	varinf( 0x1B, 1, 1, "" ),
	varinf( 0x1C, 2, 1, "curvespeed" ),
	varinf( 0x1E, 1, 6, "" ),
	varinf( 0x24, 1, 1, "numbridges" ),
	varinf( 0x25, 1, 7, "" ),
	varinf( 0x2C, 1, 1, "numstations" ),
	varinf( 0x2D, 1, 7, "" ),
	varinf( 0x34, 1, 1, "displayoffset" ),
	varinf( 0x35, 1, 1, "" ),
]

trackdesc = [
	objdesc( 'desc_objdata' ),
	objdesc( 'desc_lang', [ 0 ] ),
	objdesc( 'desc_useobj', [ 0xFFFFFFF9, 'compatible', 0x11, 0x14, -1 ] ),
	objdesc( 'desc_useobj', [ 0xFFFFFFF8, 'trackmod', 0x10, -1 ] ),
	objdesc( 'desc_useobj', [ 0xFFFFFFF7, 'signal', 0x0A, -1 ] ),
	objdesc( 'desc_useobj', [  0, 'tunnel', 0x0D, -1 ] ),
	objdesc( 'desc_useobj', [ 0xFFFFFFDC, 'bridge', 0x0E, -1 ] ),
	objdesc( 'desc_useobj', [ 0xFFFFFFD4, 'station', 0x0F, -1 ] ),
	objdesc( 'desc_sprites' ),
]


# ***********************
# Class 12:  ROAD STATIONS
# ***********************

road_pieces = [
	"smallcurve", "tightcurve", "normalslope", "steepslope",
	"", "reverse",
]

roadstvars = [
	varinf( 0x00, 1, 4, "" ),
	varinf( 0x04, 2, 1, "roadpieces", None, road_pieces ),
	varinf( 0x06,-2, 1, "buildcostfact" ),
	varinf( 0x08,-2, 1, "sellcostfact" ),
	varinf( 0x0A, 1, 1, "costind" ),
	varinf( 0x0B, 1,22, "" ),
	varinf( 0x21, 1, 1, "numcompat" ),
	varinf( 0x22, 1, 6, "" ),
	varinf( 0x28, 2, 1, "designed" ),
	varinf( 0x2a, 2, 1, "obsolete" ),
	varinf( 0x2c, 1,66, "" ),
]

roadstaux = [
	auxdesc( "", None ),
]

roadstdesc = [
	objdesc( 'desc_objdata' ),
	objdesc( 'desc_lang', [ 0 ] ),
	objdesc( 'desc_useobj', [ 0, 'cargo', 0x08, -1 ] ),
	objdesc( 'desc_auxdatavar', [ 0, 16, 1, 4 ] ),
	objdesc( 'desc_sprites' ),
]


# ***********************
# Class 13:  ROAD MODS
# ***********************

# (same as track mods)


# ***********************
# Class 14:    ROADS
# ***********************

roadvars = [
	varinf( 0x00, 1, 2, "" ),
	varinf( 0x02, 2, 1, "roadpieces", None, road_pieces ),
	varinf( 0x04,-2, 1, "buildcostfact" ),
	varinf( 0x06,-2, 1, "sellcostfact" ),
	varinf( 0x08,-2, 1, "tunnelcostfact" ),
	varinf( 0x0A, 1, 1, "costind" ),
	varinf( 0x0B, 1, 9, "" ),
	varinf( 0x14, 1, 1, "numbridges" ),
	varinf( 0x15, 1, 8, "" ),
	varinf( 0x1D, 1, 1, "numstations" ),
	varinf( 0x1E, 1, 10, "" ),
	varinf( 0x28, 1, 1, "numcompat" ),
	varinf( 0x29, 1, 7, "" ),
]

roaddesc = [
	objdesc( 'desc_objdata' ),
	objdesc( 'desc_lang', [ 0 ] ),
	objdesc( 'desc_useobj', [ 0xFFFFFFD8, 'compatible', 0x11, 0x14, -1 ] ),
	objdesc( 'desc_useobj', [ 0xFFFFFFDB, 'roadmod', 0x13, -1 ] ),
	objdesc( 'desc_useobj', [  0, 'tunnel', 0x0D, -1 ] ),
	objdesc( 'desc_useobj', [ 0xFFFFFFEC, 'bridge', 0x0E, -1 ] ),
	objdesc( 'desc_useobj', [ 0xFFFFFFE4, 'station', 0x12, -1 ] ),
	objdesc( 'desc_sprites' ),
]


# ***********************
# Class 15:   AIRPORTS
# ***********************

airport_aux0 = [
	varinf( 0x00, 1, 0, "height" ),
]

airport_aux1 = [
	varinf( 0x00, 2, 0, "frames" ),
]

airport_aux2 = [
	varinf( 0x00, 1, 0, "spriteset" ),
]

layoutvars = [
	varinf( 0x00, 1, 1, "tilenum" ),
	varinf( 0x01, 1, 1, "rotate" ),
	varinf( 0x02,-1, 1, "x" ),
	varinf( 0x03,-1, 1, "y" ),
]

airport_aux3 = [
	varinf( 0x00, 4, 0, "tilepos", layoutvars ),
]

airportaux4flags = [
	"terminal", "aircraftend", "", "ground",
	"flight", "helibegin", "aircraftbegin", "heliend",
	"touchdown",
]

airport_aux4 = [
	varinf( 0x00,-2, 1, "x" ),
	varinf( 0x02,-2, 1, "y" ),
	varinf( 0x04,-2, 1, "z" ),
	varinf( 0x06, 2, 1, "flags", None, airportaux4flags ),
]

airport_aux5 = [
	varinf( 0x00, 1, 1, "" ),
	varinf( 0x01, 1, 1, "from" ),
	varinf( 0x02, 1, 1, "to" ),
	varinf( 0x03, 1, 1, "" ),
	varinf( 0x04, 4, 1, "busymask", None, nobits ),
	varinf( 0x08, 4, 1, "", None, nobits ),
]

airportvars = [
	varinf( 0x00, 1, 2, "" ),
	varinf( 0x02,-2, 1, "buildcostfact" ),
	varinf( 0x04,-2, 1, "sellcostfact" ),
	varinf( 0x06, 1, 1, "costind" ),
	varinf( 0x07, 1, 9, "" ),
	varinf( 0x10, 2, 1, "allowedplanetypes" ),
	varinf( 0x12, 1, 1, "numspritesets" ),
	varinf( 0x13, 1, 1, "numtiles" ),
	varinf( 0x14, 1,140,"" ),
	varinf( 0xA0, 4, 1, "2x2tiles", None, nobits ),
	varinf( 0xA4,-1, 1, "minx" ),
	varinf( 0xA5,-1, 1, "miny" ),
	varinf( 0xA6,-1, 1, "maxx" ),
	varinf( 0xA7,-1, 1, "maxy" ),
	varinf( 0xA8, 2, 1, "designed" ),
	varinf( 0xAA, 2, 1, "obsolete" ),
	varinf( 0xAC, 1, 1, "numnodes" ),
	varinf( 0xAD, 1, 1, "numedges" ),
	varinf( 0xAE, 1, 8, "", ),
	varinf( 0xB6, 4, 1, "", None, nobits ),
]

airportaux = [
	auxdesc( "spriteheight", airport_aux0 ),
	auxdesc( "spriteanimframes", airport_aux1 ),
	auxdesc( "tile", airport_aux2 ),
	auxdesc( "layout", airport_aux3 ),
	auxdesc( "node", airport_aux4 ),
	auxdesc( "edge", airport_aux5),
]

airportdesc = [
	objdesc( 'desc_objdata' ),
	objdesc( 'desc_lang', [ 0 ] ),
	objdesc( 'desc_auxdata',    [ 0, 0,           1, 0xFFFFFFEE ] ),
	objdesc( 'desc_auxdata',    [ 1, 0,          -2, 0xFFFFFFEE ] ),
	objdesc( 'desc_auxdatavar', [ 2, 0xFFFFFFED,  1, 1 ] ),
	objdesc( 'desc_auxdatavar', [ 3, 0x00000000, -4, 1 ] ),
	objdesc( 'desc_auxdata',    [ 4, 0xFFFFFF54,  1, 8 ] ),
	objdesc( 'desc_auxdata',    [ 5, 0xFFFFFF53,  1 , 12 ] ),
	objdesc( 'desc_sprites' ),
]


# ***********************
# Class 16:     DOCKS
# ***********************

dockvars = [
	varinf( 0x00, 1, 2, "" ),
	varinf( 0x02,-2, 1, "buildcostfact" ),
	varinf( 0x04,-2, 1, "sellcostfact" ),
	varinf( 0x06, 1, 1, "costind" ),
	varinf( 0x07, 1,11, "" ),
	varinf( 0x12, 1, 1, "numaux01" ),
	varinf( 0x13, 1, 1, "numaux2ent" ),
	varinf( 0x14, 1,12, "" ),
	varinf( 0x20, 2, 1, "designed" ),
	varinf( 0x22, 2, 1, "obsolete" ),
	varinf( 0x24, 1, 4, "" ),
]

dockaux = [
	auxdesc( "", None ),
	auxdesc( "", None ),
	auxdesc( "", None ),
]

dockdesc = [
	objdesc( 'desc_objdata' ),
	objdesc( 'desc_lang', [ 0 ] ),
	objdesc( 'desc_auxdata',    [ 0, 0,  1, 0xFFFFFFEE ] ),
	objdesc( 'desc_auxdata',    [ 1, 0, -2, 0xFFFFFFEE ] ),
	objdesc( 'desc_auxdatavar', [ 2, 0xFFFFFFED, 1, 1 ] ),
	objdesc( 'desc_sprites' ),
]

# ***********************
# Class 17:   VEHICLES
# ***********************

# the known bits in the vehicle sprite structure flags
vehspriteflags = [
	"hassprites", "", "", "", "",
	"reversed",
]
# the vehicle sprite definition structure
vehsprites = [
	varinf( 0x00, 1, 1, "numdir" ),
	varinf( 0x01, 1, 1, "" ),
	varinf( 0x02, 1, 1, "" ),
	varinf( 0x03, 1, 1, "vehtype" ),
	varinf( 0x04, 1, 1, "numunits" ),
	varinf( 0x05, 1, 1, "" ),
	varinf( 0x06, 1, 1, "bogeypos" ),
	varinf( 0x07, 1, 1, "flags", None, vehspriteflags ),
	varinf( 0x08, 1, 1, "" ),
	varinf( 0x09, 1, 1, "" ),
	varinf( 0x0A, 1, 1, "" ),
	varinf( 0x0B, 1, 1, "" ),
	varinf( 0x0C, 1, 1, "" ),
	varinf( 0x0D, 1, 1, "" ),
	varinf( 0x0E, 1, 1, "spritenum" ),
	varinf( 0x0F, 1, 3, "" ),
	varinf( 0x12, 4, 1, "" ),
	varinf( 0x16, 4, 1, "" ),
	varinf( 0x1A, 4, 1, "" ),
]

# a vehicle structure whose purpose is mostly unknown
vehunk = [
	varinf( 0x00, 1, 1, "length" ),
	varinf( 0x01, 1, 1, "" ),
	varinf( 0x02, 1, 1, "" ),
	varinf( 0x03, 1, 1, "" ),
	varinf( 0x04, 1, 1, "spriteind" ),
	varinf( 0x05, 1, 1, "" ),
]

# the vehicle flags
vehflags = [
	"", "", "", "",
	"", "", "rackrail", "",
	"", "anytrack", "", "cancouple",
	"dualhead", "", "refittable", "noannounce",
]

# the main vehicle data structure
vehvars = [
    # ofs, size, num (array_length), name, structvars
	varinf( 0x000, 1, 2, "" ),
	varinf( 0x002, 1, 1, "class" ),
	varinf( 0x003, 1, 1, "type" ),
	varinf( 0x004, 1, 1, "" ),
	varinf( 0x005, 1, 1, "" ),
	varinf( 0x006, 1, 1, "nummods" ),
	varinf( 0x007, 1, 1, "costind" ),
	varinf( 0x008,-2, 1, "costfact" ),	# size -2 means signed word
	varinf( 0x00A, 1, 1, "reliability" ),
	varinf( 0x00B, 1, 1, "runcostind" ),
	varinf( 0x00C,-2, 1, "runcostfact" ),
	varinf( 0x00E, 1, 1, "colourtype" ),
	varinf( 0x00F, 1, 1, "numcompat" ),
	varinf( 0x010, 1,20, "" ),
	varinf( 0x024, 6, 4, "", vehunk ),
	varinf( 0x03C,30, 4, "sprites", vehsprites ),
	varinf( 0x0B4, 1,36, "" ),
	varinf( 0x0D8, 2, 1, "power" ),
	varinf( 0x0DA, 2, 1, "speed" ),
	varinf( 0x0DC, 2, 1, "rackspeed" ),
	varinf( 0x0DE, 2, 1, "weight" ),
	varinf( 0x0E0, 2, 1, "flags", None, vehflags ),
	varinf( 0x0E2, 1,44, "" ),
	varinf( 0x10E, 1, 1, "visfxheight" ),
	varinf( 0x10F, 1, 1, "visfxtype" ),
	varinf( 0x110, 1, 1, "" ),
	varinf( 0x111, 1, 1, "" ),
	varinf( 0x112, 1, 1, "wakefxtype" ),
	varinf( 0x113, 1, 1, "" ),
	varinf( 0x114, 2, 1, "designed" ),
	varinf( 0x116, 2, 1, "obsolete" ),
	varinf( 0x118, 1, 1, "" ),
	varinf( 0x119, 1, 1, "startsndtype" ),
	varinf( 0x11A, 1,64, "" ),
	varinf( 0x15A, 1, 1, "numsnd" ),
	varinf( 0x15B, 1, 3, "" )
]

vehdesc = [
	objdesc( 'desc_objdata' ),
	objdesc( 'desc_lang',   [ 0 ] ),
	objdesc( 'desc_useobj', [ descnumspec(0), 'tracktype', 0x11, 0x14 ] ),
	objdesc( 'desc_useobj', [ 0xFFFFFFFA, 'trackmod', 0x10, 0x13 ] ), # 0xFFFFFFFA = -6
	objdesc( 'desc_cargo',  [ 2 ] ),
	objdesc( 'desc_useobj', [ descnumif(0x10f), 'visualeffect', 0x03 ] ),
	objdesc( 'desc_useobj', [ descnumif(0x112), 'wakeeffect', 0x03 ] ),
	objdesc( 'desc_useobj', [ descnumspec(1), 'rackrail', 0x10 ] ),
	objdesc( 'desc_useobj', [ 0xFFFFFFF1, 'compatible', 0x17 ] ), # 0xFFFFFFF1 = -15
	objdesc( 'desc_useobj', [ descnumif(0x119), 'startsnd', 0x01 ] ),
	objdesc( 'desc_useobj', [ descnumand(0x15a,0x7f), 'soundeffect', 0x01 ] ),
	objdesc( 'desc_sprites' ),
]

# ***********************
# Class 18:    TREES
# ***********************

treevars = [
	varinf( 0x00, 1, 3, "" ),
	varinf( 0x03, 1, 1, "height" ),
	varinf( 0x04, 1,59, "" ),
	varinf( 0x3F, 1, 1, "costind" ),
	varinf( 0x40,-2, 1, "buildcostfact" ),
	varinf( 0x42,-2, 1, "clearcostfact" ),
	varinf( 0x44, 1, 8, "" ),
]


# ***********************
# Class 19:    SNOW
# ***********************

# (see simple vars above)


# ***********************
# Class 1A:   CLIMATES
# ***********************

climvars = [
	varinf( 0x00, 1, 2, "" ),
	varinf( 0x02, 1, 1, "firstseason" ),
	varinf( 0x03, 1, 4, "seasonlength" ),
	varinf( 0x07, 1, 3, "" ),
]

climdesc = [
	objdesc( 'desc_objdata' ),
	objdesc( 'desc_lang', [ 0 ] ),
]


# ***********************
# Class 1B:   SHAPES
# ***********************

shapevars = [
	varinf( 0x00, 1, 14, "" ),
]


# ***********************
# Class 1C:   BUILDINGS
# ***********************

bldg_flags = [
	"", "", "", "ishq",	# 1 2 4 8
]

bldngvars = [
	varinf( 0x00, 1, 6, "" ),
	varinf( 0x06, 1, 1, "numaux01" ),
	varinf( 0x07, 1, 1, "numaux2ent" ),
	varinf( 0x08, 1,140,"" ),
	varinf( 0x94, 2, 1, "earliestyr" ),
	varinf( 0x96, 2, 1, "latestyr" ),
	varinf( 0x98, 1, 1, "flags", None, bldg_flags ),
	varinf( 0x99, 1, 1, "costind" ),
	varinf( 0x9A,-2, 1, "clearcostfact" ),
	varinf( 0x9C, 1, 4, "" ),
	varinf( 0xA0, 1, 2, "numproduce" ),
	varinf( 0xA2, 1, 4, "" ),
	varinf( 0xA6, 1, 4, "numaccept" ),
	varinf( 0xAA, 1, 3, "" ),
	varinf( 0xAD, 1, 1, "numaux3ent" ),
	varinf( 0xAE, 1,16, "" ),
]

bldngaux = [
	auxdesc( "", None ),
	auxdesc( "", None ),
	auxdesc( "", None ),
	auxdesc( "", None ),
]

bldngdesc = [
	objdesc( 'desc_objdata' ),
	objdesc( 'desc_lang', [ 0 ] ),
	objdesc( 'desc_auxdata',    [ 0, 0, 1, 0xFFFFFFFA ] ),
	objdesc( 'desc_auxdata',    [ 1, 0, -2, 0xFFFFFFFA ] ),
	objdesc( 'desc_auxdatavar', [ 2, 0xFFFFFFF9, 1, 1 ] ),
	objdesc( 'desc_useobj',     [ 4, 'cargo', 0x08, 0xFF, -1 ] ),
	objdesc( 'desc_auxdatafix', [ 3, 0xFFFFFF53, 1, 2 ] ),
	objdesc( 'desc_sprites' ),
]


# ***********************
# Class 1D:  SCAFFOLDING
# ***********************

scaffvars = [
	varinf( 0x00, 1, 18, "" ),
]


# ***********************
# Class 1E:  INDUSTRIES
# ***********************

industryflags = [
	"", "", "", "",		# 1, 2, 4, 8
	"", "", "", "",		# 10, 20, 40, 80
	"", "", "", "",		# 100, 200, 400, 800
	"", "", "", "",		# 1000, 2000, 4000, 8000
	"", "needall", "canincreaseproduction", "candecreaseproduction",
				# 100000, 200000, 400000, 800000
]

indvars = [
	varinf( 0x00, 1,30, "" ),
	varinf( 0x1E, 1, 1, "numaux01" ),
	varinf( 0x1F, 1, 1, "numaux4ent" ),
	varinf( 0x20, 1,157,"" ),
	varinf( 0xBD, 1, 1, "numaux5" ),
	varinf( 0xBE, 1,12, "" ),
	varinf( 0xCA, 2, 1, "firstyear" ),
	varinf( 0xCC, 2, 1, "lastyear" ),
	varinf( 0xCE, 1, 1, "" ),
	varinf( 0xCF, 1, 1, "costind" ),
	varinf( 0xD0,-2, 1, "costfactor1" ),
	varinf( 0xD2, 1, 18, "" ),
	varinf( 0xE4, 4, 1, "flags", None, industryflags ),
	varinf( 0xE8, 1, 12, "" ),
]

indaux = [
	auxdesc( "", None ),
	auxdesc( "", None ),
	auxdesc( "", None ),
	auxdesc( "", None ),
	auxdesc( "", None ),
	auxdesc( "", None ),
]

inddesc = [
	objdesc( 'desc_objdata' ),
	objdesc( 'desc_lang', [ 0 ] ),
	objdesc( 'desc_lang', [ 1 ] ),
	objdesc( 'desc_lang', [ 2 ] ),
	objdesc( 'desc_lang', [ 3 ] ),
	objdesc( 'desc_lang', [ 4 ] ),
	objdesc( 'desc_lang', [ 5 ] ),
	objdesc( 'desc_lang', [ 6 ] ),
	objdesc( 'desc_lang', [ 7 ] ),
	objdesc( 'desc_auxdata',    [ 0, 0, 1, 0xFFFFFFE2 ] ),
	objdesc( 'desc_auxdata',    [ 1, 0, 2, 0xFFFFFFE2 ] ),
	objdesc( 'desc_auxdatafix', [ 2, 4, 1, 1 ] ),
	objdesc( 'desc_auxdatavar', [ 3, 0, 2, 1 ] ),
	objdesc( 'desc_auxdatavar', [ 4, 0xFFFFFFE1, 1, 1 ] ),
	objdesc( 'desc_auxdata',    [ 5, 0, 1, 0xFFFFFF43 ] ),
	objdesc( 'desc_useobj', [ 2, 'produces', 0x08, 0xFF, 0xFFFFFFFF ] ),
	objdesc( 'desc_useobj', [ 3, 'accepts', 0x08, 0xFF, 0xFFFFFFFF ] ),
	objdesc( 'desc_useobj', [ 6, 'fence', 0x09, 0xFF, 0xFFFFFFFF ] ),
	objdesc( 'desc_sprites' ),
]


# ***********************
# Class 1F:   REGIONS
# ***********************

regionvars = [
	varinf( 0x00, 1, 18, "" ),
]

regiondesc = [
	objdesc( 'desc_objdata' ),
	objdesc( 'desc_lang', [ 0 ] ),
	objdesc( 'desc_useobj', [ [ -1, -1, -8 ], 'cargo', 0x08 ] ),
	objdesc( 'desc_useobj', [ [ 1, 0, 0 ], 'default', 0x100 ] ),
	objdesc( 'desc_sprites' ),
]


# ***********************
# Class 20:  COMPANIES
# ***********************

comp_sprites = [
]

compvars = [
	varinf( 0x00, 1,12, "" ),
	varinf( 0x0C, 1, 2, "spritesets", None, comp_sprites ),
	varinf( 0x0E, 1,38, "" ),
	varinf( 0x34, 1, 1, "intelligence" ),
	varinf( 0x35, 1, 1, "aggressiveness" ),
	varinf( 0x36, 1, 1, "competitiveness" ),
	varinf( 0x37, 1, 1, "" ),
]

compdesc = [
	objdesc( 'desc_objdata' ),
	objdesc( 'desc_lang', [ 0 ] ),
	objdesc( 'desc_lang', [ 1 ] ),
	objdesc( 'desc_sprites' ),
]


# ***********************
# Class 21:   TEXTS
# ***********************

# (uses simple vars)

textdesc = [
	objdesc( 'desc_objdata' ),
	objdesc( 'desc_lang', [ 0 ] ),
	objdesc( 'desc_lang', [ 1 ] ),
]

# ***********************
#  END OF CLASS HANDLERS
# ***********************

#
# Array defining object class-specific data structures and descriptions
#
objclasses = [
	# structure	size auxdef	description
	objclass( interfacevars, 24, None, simpledesc ),	# 00 Interfaces
	objclass( sfxvars,	 	 12, None, sfxdesc ),		# 01 Sound effects
	objclass( currvars,	 	 12, None, currdesc ),		# 02 Currencies
	objclass( exhfxvars,	 40, exhfxaux, exhfxdesc ),	# 03 Exhaust effects
	objclass( simplevars,	  6, None,	simpledesc ),	# 04 Cliff faces
	objclass( watervars,	 14, None,	simpledesc ),	# 05 Water
	objclass( groundvars,	 30, None,	grounddesc ),	# 06 Ground
	objclass( townvars,	 	 26, None,	towndesc ),		# 07 Town names
	objclass( cargovars,	 31, None,	cargodesc ),	# 08 Cargos
	objclass( fencevars,	 10, None,	simpledesc ),	# 09 Fences
	objclass( signalvars,	 30, None,	signaldesc ),	# 0A Signals
	objclass( crossingvars,	 18, None,	simpledesc ),	# 0B Crossings
	objclass( lightvars,	 12, None,	simpledesc ),	# 0C Street lights
	objclass( simplevars,	  6, None,	simpledesc ),	# 0D Tunnels
	objclass( bridgevars,	 44, None,	simpledesc ),	# 0E Bridges
	objclass( trnstatvars,	174, trnstataux,trnstatdesc ),	# 0F Train stations
	objclass( trkmodvars,	 18, None,	simpledesc ),	# 10 Track modifications
	objclass( trackvars,	 54, None,	trackdesc ),	# 11 Tracks
	objclass( roadstvars,	110, roadstaux,	roadstdesc ),	# 12 Road stations
	objclass( trkmodvars,	 18, None,	simpledesc ),	# 13 Road modifications
	objclass( roadvars,	 	 48, None,	roaddesc ),		# 14 Roads
	objclass( airportvars,	186, airportaux,airportdesc ),	# 15 Airports
	objclass( dockvars,	 	 40, dockaux,	dockdesc ),	# 16 Docks
	objclass( vehvars, 		350, None, vehdesc ),		# 17 Vehicles
	objclass( treevars,	 	 76, None,	simpledesc ),	# 18 Trees
	objclass( simplevars,	  6, None,	simpledesc ),	# 19 Snow
	objclass( climvars,	 	 10, None,	climdesc ),		# 1A Climates
	objclass( shapevars,	 14, None,	simpledesc ),	# 1B Shapes
	objclass( bldngvars,	190, bldngaux,	bldngdesc ),# 1C bldngs
	objclass( scaffvars,	 18, None,	simpledesc ),	# 1D Scaffolding
	objclass( indvars,		244, indaux,	inddesc ),	# 1E Industries
	objclass( regionvars,	 18, None,	regiondesc ),	# 1F Regions
	objclass( compvars,	 	 56, None,	compdesc ),		# 20 Companies
	objclass( simplevars,	  6, None,	textdesc ),		# 21 Texts
]

objclassnames = [
	'Interfaces', 'Sound effects', 'Currencies',
	'Exhaust effects', 'Cliff faces', 'Water',
	'Ground', 'Town names',  'Cargos', 'Fences',
	'Signals', 'Crossings', 'Street lights',
	'Tunnels', 'Bridges', 'Train stations',
	'Track modifications', 'Tracks', 'Road stations',
	'Road modifications', 'Roads', 'Airports',
	'Docks', 'Vehicles', 'Trees', 
	'Snow', 'Climates', 'Shapes', 
	'Buildings', 'Scaffolding', 'Industries',
	'Regions', 'Companies', 'Texts'
]

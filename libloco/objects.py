import struct
from .varinf import varinf
from .objdesc import objdesc
from .objclass import objclass
from .helper import *


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
	objdesc( 'desc_lang', [ 0 ] ),
	objdesc( 'desc_useobj', [ descnumspec(0), 'tracktype', 0x11, 0x14 ] ),
	objdesc( 'desc_useobj', [ 0xFFFFFFFA, 'trackmod', 0x10, 0x13 ] ), # 0xFFFFFFFA = -6
	objdesc( 'desc_cargo', [ 2 ] ),
	objdesc( 'desc_useobj', [ descnumif(0x10f), 'visualeffect', 0x03 ] ),
	objdesc( 'desc_useobj', [ descnumif(0x112), 'wakeeffect', 0x03 ] ),
	objdesc( 'desc_useobj', [ descnumspec(1), 'rackrail', 0x10 ] ),
	objdesc( 'desc_useobj', [ 0xFFFFFFF1, 'compatible', 0x17 ] ), # 0xFFFFFFF1 = -15
	objdesc( 'desc_useobj', [ descnumif(0x119), 'startsnd', 0x01 ] ),
	objdesc( 'desc_useobj', [ descnumand(0x15a,0x7f), 'soundeffect', 0x01 ] ),
	objdesc( 'desc_sprites' ),
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
0,#	objclass( exhfxvars,	 40, exhfxaux, exhfxdesc ),	# 03 Exhaust effects
0,#	objclass( simplevars,	  6, None,	simpledesc ),	# 04 Cliff faces
0,#	objclass( watervars,	 14, None,	simpledesc ),	# 05 Water
0,#	objclass( groundvars,	 30, None,	grounddesc ),	# 06 Ground
0,#	objclass( townvars,	 	 26, None,	towndesc ),		# 07 Town names
0,#	objclass( cargovars,	 31, None,	cargodesc ),	# 08 Cargos
0,#	objclass( fencevars,	 10, None,	simpledesc ),	# 09 Fences
0,#	objclass( signalvars,	 30, None,	signaldesc ),	# 0A Signals
0,#	objclass( crossingvars,	 18, None,	simpledesc ),	# 0B Crossings
0,#	objclass( lightvars,	 12, None,	simpledesc ),	# 0C Street lights
0,#	objclass( simplevars,	  6, None,	simpledesc ),	# 0D Tunnels
0,#	objclass( bridgevars,	 44, None,	simpledesc ),	# 0E Bridges
0,#	objclass( trnstatvars,	174, trnstataux,trnstatdesc ),	# 0F Train stations
0,#	objclass( trkmodvars,	 18, None,	simpledesc ),	# 10 Track modifications
0,#	objclass( trackvars,	 54, None,	trackdesc ),	# 11 Tracks
0,#	objclass( roadstvars,	110, roadstaux,	roadstdesc ),	# 12 Road stations
0,#	objclass( trkmodvars,	 18, None,	simpledesc ),	# 13 Road modifications
0,#	objclass( roadvars,	 	 48, None,	roaddesc ),		# 14 Roads
0,#	objclass( airportvars,	186, airportaux,airportdesc ),	# 15 Airports
0,#	objclass( dockvars,	 	 40, dockaux,	dockdesc ),	# 16 Docks
	objclass( vehvars, 		350, None, vehdesc ),		# 17 Vehicles
0,#	objclass( treevars,	 	 76, None,	simpledesc ),	# 18 Trees
0,#	objclass( simplevars,	  6, None,	simpledesc ),	# 19 Snow
0,#	objclass( climvars,	 	 10, None,	climdesc ),		# 1A Climates
0,#	objclass( shapevars,	 14, None,	simpledesc ),	# 1B Shapes
0,#	objclass( bldngvars,	190, bldngaux,	bldngdesc ),# 1C bldngs
0,#	objclass( scaffvars,	 18, None,	simpledesc ),	# 1D Scaffolding
0,#	objclass( indvars,		244, indaux,	inddesc ),	# 1E Industries
0,#	objclass( regionvars,	 18, None,	regiondesc ),	# 1F Regions
0,#	objclass( compvars,	 	 56, None,	compdesc ),		# 20 Companies
0 #	objclass( simplevars,	  6, None,	textdesc ),		# 21 Texts

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
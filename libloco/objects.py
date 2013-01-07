

vehunk = []
vehsprites = []
vehflags = []

vehvars = [
    # ofs, size, num (array_length), name, structvars
	[ 0x000, 1, 2, "" ],
	[ 0x002, 1, 1, "class" ],
	[ 0x003, 1, 1, "type" ],
	[ 0x004, 1, 1, "" ],
	[ 0x005, 1, 1, "" ],
	[ 0x006, 1, 1, "nummods" ],
	[ 0x007, 1, 1, "costind" ],
	[ 0x008,-2, 1, "costfact" ],	# size -2 means signed word
	[ 0x00A, 1, 1, "reliability" ],
	[ 0x00B, 1, 1, "runcostind" ],
	[ 0x00C,-2, 1, "runcostfact" ],
	[ 0x00E, 1, 1, "colourtype" ],
	[ 0x00F, 1, 1, "numcompat" ],
	[ 0x010, 1,20, "" ],
	[ 0x024, 6, 4, "", vehunk ],
	[ 0x03C,30, 4, "sprites", vehsprites ],
	[ 0x0B4, 1,36, "" ],
	[ 0x0D8, 2, 1, "power" ],
	[ 0x0DA, 2, 1, "speed" ],
	[ 0x0DC, 2, 1, "rackspeed" ],
	[ 0x0DE, 2, 1, "weight" ],
	[ 0x0E0, 2, 1, "flags", None, vehflags ],
	[ 0x0E2, 1,44, "" ],
	[ 0x10E, 1, 1, "visfxheight" ],
	[ 0x10F, 1, 1, "visfxtype" ],
	[ 0x110, 1, 1, "" ],
	[ 0x111, 1, 1, "" ],
	[ 0x112, 1, 1, "wakefxtype" ],
	[ 0x113, 1, 1, "" ],
	[ 0x114, 2, 1, "designed" ],
	[ 0x116, 2, 1, "obsolete" ],
	[ 0x118, 1, 1, "" ],
	[ 0x119, 1, 1, "startsndtype" ],
	[ 0x11A, 1,64, "" ],
	[ 0x15A, 1, 1, "numsnd" ],
	[ 0x15B, 1, 3, "" ]
]
vehdesc = [
	[ 'objdata' ]
]

objclasses = [
#	// structure	size auxdef	description
0,#	{ interfacevars, 24, None,	simpledesc },	// 00 Interfaces
0,#	{ sfxvars,	 12, None,	sfxdesc },	// 01 Sound effects
0,#	{ currvars,	 12, None,	currdesc },	// 02 Currencies
0,#	{ exhfxvars,	 40, exhfxaux,	exhfxdesc },	// 03 Exhaust effects
0,#	{ simplevars,	  6, None,	simpledesc },	// 04 Cliff faces
0,#	{ watervars,	 14, None,	simpledesc },	// 05 Water
0,#	{ groundvars,	 30, None,	grounddesc },	// 06 Ground
0,#	{ townvars,	 26, None,	towndesc },	// 07 Town names
0,#	{ cargovars,	 31, None,	cargodesc },	// 08 Cargos
0,#	{ fencevars,	 10, None,	simpledesc },	// 09 Fences
0,#	{ signalvars,	 30, None,	signaldesc },	// 0A Signals
0,#	{ crossingvars,	 18, None,	simpledesc },	// 0B Crossings
0,#	{ lightvars,	 12, None,	simpledesc },	// 0C Street lights
0,#	{ simplevars,	  6, None,	simpledesc },	// 0D Tunnels
0,#	{ bridgevars,	 44, None,	simpledesc },	// 0E Bridges
0,#	{ trnstatvars,	174, trnstataux,trnstatdesc },	// 0F Train stations
0,#	{ trkmodvars,	 18, None,	simpledesc },	// 10 Track modifications
0,#	{ trackvars,	 54, None,	trackdesc },	// 11 Tracks
0,#	{ roadstvars,	110, roadstaux,	roadstdesc },	// 12 Road stations
0,#	{ trkmodvars,	 18, None,	simpledesc },	// 13 Road modifications
0,#	{ roadvars,	 48, None,	roaddesc },	// 14 Roads
0,#	{ airportvars,	186, airportaux,airportdesc },	// 15 Airports
0,#	{ dockvars,	 40, dockaux,	dockdesc },	// 16 Docks
	[ vehvars,	350, None,	vehdesc ],	# 17 Vehicles
0,#	{ treevars,	 76, None,	simpledesc },	// 18 Trees
0,#	{ simplevars,	  6, None,	simpledesc },	// 19 Snow
0,#	{ climvars,	 10, None,	climdesc },	// 1A Climates
0,#	{ shapevars,	 14, None,	simpledesc },	// 1B Shapes
0,#	{ bldngvars,	190, bldngaux,	bldngdesc },	// 1C bldngs
0,#	{ scaffvars,	 18, None,	simpledesc },	// 1D Scaffolding
0,#	{ indvars,	244, indaux,	inddesc },	// 1E Industries
0,#	{ regionvars,	 18, None,	regiondesc },	// 1F Regions
0,#	{ compvars,	 56, None,	compdesc },	// 20 Companies
0 #	{ simplevars,	  6, None,	textdesc },	// 21 Texts

]


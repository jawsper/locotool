#!/usr/bin/env python

import libloco.LocoDecoder

import sys
import os

if __name__ == '__main__':
	path = None
	test = None
	if len( sys.argv ) > 1:
		if sys.argv[1][0:2] == '-t':
			test = int( sys.argv[1][2:], 16 if sys.argv[1][3] == 'x' else 10 )
			if len( sys.argv ) > 2 and os.path.isdir( sys.argv[2] ):
				path = os.path.realpath( sys.argv[2] )
			else:
				path = os.path.realpath( '.' )
		elif os.path.isdir( sys.argv[1] ):
			path = os.path.realpath( sys.argv[1] )
	else:
		path = os.path.realpath( '.' )
	if path != None:
		for filename in os.listdir( path ):
			if filename.lower().endswith( '.dat' ):
				f = libloco.LocoDecoder( os.path.join( path, filename ) )
				if test:
					if f.get_header()[0] == test:
						open( os.path.join( '.', filename ), 'wb' ).write( open( os.path.join( path, filename ), 'rb' ).read() )
						print( '{2} class: 0x{0:02X} {3}'.format( *f.get_header() ) )
						break
				else:
					print( '{2} class: 0x{0:02X} {3}'.format( *f.get_header() ) )
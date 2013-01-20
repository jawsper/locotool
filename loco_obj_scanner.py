#!/usr/bin/env python
from __future__ import print_function

from libloco.LocoDecoder import LocoDecoder

import os
import argparse

if __name__ == '__main__':
	path = None
	test = None
	parser = argparse.ArgumentParser( description='Loco obj scanner' )
	parser.add_argument( 'path', nargs = '?', default = '.' )
	parser.add_argument( '-t', '--type', type=int )
	parser.add_argument( '--all', action="store_true" )
	args = parser.parse_args()
	
	if os.path.isdir( args.path ):
		path = os.path.realpath( args.path )
		for filename in sorted( os.listdir( path ), cmp=lambda x,y: cmp( x.lower(), y.lower() ) ):
			if filename.lower().endswith( '.dat' ):
				f = LocoDecoder( os.path.join( path, filename ) )
				if args.type:
					if f.get_header()[0] == args.type:
						open( os.path.join( '.', filename ), 'wb' ).write( open( os.path.join( path, filename ), 'rb' ).read() )
						print( '{2} class: {0:02} {3}'.format( *f.get_header() ) )
						if not args.all:
							break
				else:
					print( '{2} class: {0:02} {3}'.format( *f.get_header() ) )
	else:
		print( 'Invalid path: {0}'.format( args.path ) )
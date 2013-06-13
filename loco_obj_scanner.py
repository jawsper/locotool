#!/usr/bin/env python
from __future__ import print_function

from libloco.LocoDecoder import LocoDecoder

import sys
import os
import argparse

if __name__ == '__main__':
	path = None
	test = None
	parser = argparse.ArgumentParser( description='Loco obj scanner' )
	parser.add_argument( 'path', nargs = '?', default = '.' )
	group = parser.add_mutually_exclusive_group()
	group.add_argument( '--show-classes', action='store_true', help='Show known Locomotion object classes' )
	group.add_argument( '-f', '--find', type=int, default=None, help='Only show objects of class FIND' )
	group_type = group.add_argument_group()
	group_type.add_argument( '-t', '--type', type=int, default=None, help='Copy the first object of class TYPE to the current dir' )
	group_type.add_argument( '--all', action="store_true", help='In combination with type: copy all the objects of class TYPE' )
	args = parser.parse_args()
	
	if args.show_classes:
		from libloco.objects import objclassnames
		cls = 0
		for name in objclassnames:
			print( 'Class {0:02} (0x{0:02X}): {1}'.format( cls, name ) )
			cls += 1
		sys.exit( 0 )
	
	if os.path.isdir( args.path ):
		path = os.path.realpath( args.path )
		for filename in sorted( os.listdir( path ), cmp=lambda x,y: cmp( x.lower(), y.lower() ) ):
			if filename.lower().endswith( '.dat' ):
				f = LocoDecoder( os.path.join( path, filename ) )
				if args.type != None or args.find != None:
					cls = args.type or args.find
					if f.get_header()[0] == cls:
						print( '{2} class: {0:02} {3}'.format( *f.get_header() ) )
						if args.type != None:
							open( os.path.join( '.', filename ), 'wb' ).write( open( os.path.join( path, filename ), 'rb' ).read() )
							if not args.all:
								break
				else:
					print( '{2} class: {0:02} {3}'.format( *f.get_header() ) )
	else:
		print( 'Invalid path: {0}'.format( args.path ) )

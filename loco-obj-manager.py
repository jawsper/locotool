#!/usr/bin/env python

from libloco import LocoFile

import sys
import os

if __name__ == '__main__':
	path = None
	if len( sys.argv ) > 1:
		if os.path.isdir( sys.argv[1] ):
			path = os.path.realpath( sys.argv[1] )
		else:
			f = LocoFile( sys.argv[1] )
			f.decode( sys.argv[1] )
	else:
		path = os.path.realpath( '.' )
	if path != None:
		for filename in os.listdir( path ):
			if filename.lower().endswith( '.dat' ):
				f = LocoFile( filename )
				print( '{2} class: 0x{0:02X}, subclass: 0x{1:06X}'.format( *f.get_header() ) )
	pass

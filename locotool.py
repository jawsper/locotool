#!/usr/bin/env python

import libloco.LocoDecoder
import libloco.LocoEncoder

import sys

if __name__ == '__main__':
	if len( sys.argv ) > 1:
		if sys.argv[1].lower().endswith( '.xml' ):
			f = libloco.LocoEncoder( sys.argv[1] )
			f.encode()
		else:
			f = libloco.LocoDecoder( sys.argv[1] )
			f.decode()

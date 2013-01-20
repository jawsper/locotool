#!/usr/bin/env python

from libloco.LocoDecoder import LocoDecoder
from libloco.LocoEncoder import LocoEncoder

import sys

if __name__ == '__main__':
	if len( sys.argv ) > 1:
		if sys.argv[1].lower().endswith( '.xml' ):
			f = LocoEncoder( sys.argv[1] )
			f.encode()
		else:
			f = LocoDecoder( sys.argv[1] )
			f.decode()

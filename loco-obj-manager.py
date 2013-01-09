#!/usr/bin/env python

from libloco import LocoFile

import sys


if __name__ == '__main__':
	f = LocoFile()
	f.decode( sys.argv[1] )
	pass

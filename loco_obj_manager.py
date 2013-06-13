#!/usr/bin/env python

from __future__ import print_function

import os
import argparse

class LocoObjManager:
	config = {}
	def __init__( self ):
		parser = argparse.ArgumentParser( description='Locomotion object manager' )
		parser.add_argument( '-v', dest='verbose', type=int, help='verbosity' )
		parser.add_argument( '-c', dest='config', help='Config file' )
		args = parser.parse_args()
	
if __name__ == '__main__':
	LocoObjManager()

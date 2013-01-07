#!/usr/bin/env python

from libloco import Chunk

import sys
import struct

class LocoFile:
	def read_smth( self, spec ):
		return struct.unpack( spec, self.f.read( struct.calcsize( spec ) ) )[0]
	def read_int8( self ):
		return self.read_smth( 'b' )
	def read_uint8( self ):
		return self.read_smth( 'B' )
	def read_uint32( self ):
		return self.read_smth( '<I' )
		
	def decode( self, filename ):
		with open( filename, 'rb' ) as self.f:
			tmp = self.f.read( 4 )	
			self._class = struct.unpack( 'B', tmp[0] )[0]
			self._subclass = struct.unpack( '>I', tmp )[0] & 0x00FFFFFF
			self._name = self.f.read( 8 )
			self.f.read( 4 ) # skip bytes
			print 'Class: 0x{0:02X}'.format( self._class )
			print 'Subclass: 0x{0:06X}'.format( self._subclass )
			print 'Name: {0}'.format( self._name )
			self._class &= 0x7F
			
			chunk = self.read_chunk()
			chunk.dump()
		
	def read_chunk( self ):
		compression = self.read_uint8()
		length = self.read_uint32()
		print "Chunk with compression {0}, length {1}".format( compression, length )
		if compression == 0:   # Raw
			chunk = self.f.read( length )
		elif compression == 1: # RLE
			chunk = self.chunk_rle_decode( length )
		elif compression == 2: # RLE compresses
			pass
		elif compression == 3: # Scrambled?
			pass
		else:
			print "Error! Unknown compression {0}.".format( compression )
			return False
		return Chunk( self._class, chunk )
		
	def chunk_rle_decode( self, length ):
		chunk = []
		while length > 0:
			rle = self.read_int8()
			run = abs( rle ) + 1
			length -= 1
			
			if rle < 0:
				data = self.read_uint8()
				length -= 1
				for i in range( 0, run ):
					chunk.append( data )
				# memset
			else:
				#memcpy
				length -= run
				chunk.extend( self.f.read( run ) )
		return chunk

if __name__ == '__main__':
	f = LocoFile()
	f.decode( sys.argv[1] )
	pass

import struct
import os
from .LocoFile import LocoFile
from .Chunk import Chunk
from objects import objclassnames
from helper import uint8_t

class LocoDecoder(LocoFile):
	xml = None
	pngbase = None
		
	def get_header( self ):
		with open( self.filename, 'rb' ) as f:
			tmp = f.read( 4 )
			_class = struct.unpack( 'B', tmp[0] )[0] & 0x7F
			_subclass = ( struct.unpack( '<I', tmp )[0] & 0xFFFFFF00 ) >> 8
			_name = f.read( 8 )
			return ( _class, _subclass, _name, objclassnames[ _class ] )
	
	def get_class( self ):
		with open( self.filename, 'rb' ) as f:
			_class = struct.unpack( 'B', f.read( 1 ) )[0]
		return _class
		
	def decode( self ):
		with open( self.filename, 'rb' ) as self.f:
			
			tmp = self.f.read( 4 )	
			self._class = struct.unpack( 'B', tmp[0] )[0]
			self._subclass = ( struct.unpack( '<I', tmp )[0] & 0xFFFFFF00 ) >> 8
			self._name = self.f.read( 8 )
			self.f.read( 4 ) # skip bytes
			
			self.xml = open( 'j_{0}.xml'.format( self._name ), 'w' )
			
			self.xml.write( '<?xml version="1.0" encoding="ISO-8859-1"?>\n' )
			self.xml.write( '<object class="0x{0:02X}" subclass="0x{1:06X}" name="{2}">'.format( self._class, self._subclass, self._name ) )
			
			self._class &= 0x7F
			
			while self.read_chunk():
				pass
			self.xml.write( '</object>\n' )
			self.xml.close()
		
	def read_chunk( self ):
		compression = self.read_uint8()
		if compression == False: # EOF
			return False
		length = self.read_uint32()
		self.xml.write( '<chunk compression="{0}">\n'.format( compression ) )
		if compression == 0:   # Raw
			chunk = self.f.read( length )
		elif compression == 1: # RLE
			chunk = self.chunk_rle_decode( length )
		elif compression == 2: # RLE compressed
			chunk = self.chunk_decompress( length )
		#elif compression == 3: # Scrambled?
		#	pass
		else:
			print "Error! Unknown or unsupported compression {0}.".format( compression )
			return False
		#with open( 'chunk.dat', 'wb' ) as wf:
		#	wf.write( chunk )
		if not chunk:
			raise Exception( 'No chunk!' )
		chunk = Chunk( self, chunk )
		chunk.dump()
		self.xml.write( '</chunk>' )
		return True
		
	def chunk_rle_decode( self, length ):
		chunk = r''
		while length > 0:
			rle = self.read_int8()
			run = abs( rle ) + 1
			length -= 1
			
			if rle < 0:
				data = self.read_uint8()
				length -= 1
				for i in range( 0, run ):
					chunk += struct.pack( 'B', data )
			else:
				length -= run
				data = self.f.read( run )
				chunk += data
		return chunk

	def chunk_decompress( self, length ):
		rle = self.chunk_rle_decode( length )
		#return None
		chunk = r''

		chunklen = 0
		rleofs = 0
		while rleofs < len( rle ):
		
			code = uint8_t( rle[ rleofs ] )
			rleofs += 1

			if code == 0xff:
				chunk += rle[rleofs]
				chunklen += 1
				rleofs += 1
			else:
				length = (code & 7) + 1
				ofs = 32 - ( code >> 3 )
				for i in range( length ):
					chunk += chunk[ chunklen - ofs + i ]
				chunklen += length

		return chunk
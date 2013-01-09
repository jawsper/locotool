import struct
import os
from .Chunk import Chunk

class LocoFile:
	file = None
	xml = None
	pngbase = None
	
	def makefilename( self, ext ):
		return os.path.relpath( 'j_{0}{1}'.format( self._name, ext ), os.path.dirname( self.file ) )
	def makepngname( self, num ):
		pngbase = self.pngbase if self.pngbase != None else 'j_{0}'.format( self._name )
		pngbase = os.path.relpath( pngbase, os.path.dirname( self.file ) )
		if not os.path.isdir( pngbase ):
			os.mkdir( pngbase )
		return '{0}{1}{2:03}.png'.format( pngbase, os.sep, num )

	def read_smth( self, spec ):
		return struct.unpack( spec, self.f.read( struct.calcsize( spec ) ) )[0]
	def read_int8( self ):
		return self.read_smth( 'b' )
	def read_uint8( self ):
		return self.read_smth( 'B' )
	def read_uint32( self ):
		return self.read_smth( '<I' )
		
	def decode( self, filename ):
		self.file = os.path.realpath( filename )
		with open( filename, 'rb' ) as self.f:
			
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
				break
			self.xml.write( '</object>\n' )
			self.xml.close()
		
	def read_chunk( self ):
		compression = self.read_uint8()
		length = self.read_uint32()
		self.xml.write( '<chunk compression="{0}">\n'.format( compression ) )
		if compression == 0:   # Raw
			chunk = self.f.read( length )
		elif compression == 1: # RLE
			chunk = self.chunk_rle_decode( length )
		#elif compression == 2: # RLE compresses
		#	pass
		#elif compression == 3: # Scrambled?
		#	pass
		else:
			print "Error! Unknown or unsupported compression {0}.".format( compression )
			return False
		#with open( 'chunk.dat', 'wb' ) as wf:
		#	wf.write( chunk )
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
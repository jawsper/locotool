import struct
import os

class LocoFile:
	filename = None
		
	def __init__( self, filename ):
		self.filename = os.path.realpath( filename )
	
	def makefilename( self, ext ):
		return os.path.relpath( 'j_{0}{1}'.format( self._name.rstrip(), ext ), os.path.dirname( self.filename ) )
	def makepngname( self, num ):
		pngbase = self.pngbase if self.pngbase != None else 'j_{0}'.format( self._name.rstrip() )
		pngbase = os.path.relpath( pngbase, os.path.dirname( self.filename ) )
		if not os.path.isdir( pngbase ):
			os.mkdir( pngbase )
		return os.path.join( pngbase, '{0:03}.png'.format( num ) )

	def read_smth( self, spec ):
		r = self.f.read( struct.calcsize( spec ) )
		if len( r ) == 0:
			return False
		return struct.unpack( spec, r )[0]
	def read_int8( self ):
		return self.read_smth( 'b' )
	def read_uint8( self ):
		return self.read_smth( 'B' )
	def read_uint32( self ):
		return self.read_smth( '<I' )

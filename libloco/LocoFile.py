import struct
import os

class LocoFile:
	filename = None
		
	def __init__( self, filename, **kwargs ):
		self.filename = os.path.realpath( filename )
		self.output_dir = kwargs['output_dir'] if 'output_dir' in kwargs else '.'
		#print self.filename
	
	def get_basedir(self):
		return os.path.realpath('.')
	def makefilename( self, ext ):
		filename = 'j_{}{}'.format( self._name.rstrip(), ext )
		return os.path.join(self.output_dir, filename) if self.output_dir != '.' else filename
		#return os.path.relpath( 'j_{0}{1}'.format( self._name.rstrip(), ext ), os.path.dirname( self.filename ) )
	def makepngname( self, num ):
		#pngbase = self.pngbase if self.pngbase != None else 'j_{0}'.format( self._name.rstrip() )
		#print pngbase
		#pngbase = os.path.relpath( pngbase, os.path.dirname( self.filename ) )
		#print pngbase
		pngbase = self.makefilename('')
		#print pngbase
		if not os.path.isdir( pngbase ):
			os.mkdir( pngbase )
		return os.path.join( pngbase, '{0:03}.png'.format( num ) )

	def read_smth( self, spec ):
		r = self.f.read( struct.calcsize( spec ) )
		if len( r ) == 0:
			return None
		return struct.unpack( spec, r )[0]
	def read_int8( self ):
		return self.read_smth( 'b' )
	def read_uint8( self ):
		return self.read_smth( 'B' )
	def read_uint32( self ):
		return self.read_smth( '<I' )

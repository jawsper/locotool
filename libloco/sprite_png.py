from __future__ import print_function

def putspriterow( data, flags, y, width ):
	row = None
	offset = 0
	
	if ( flags & 4 ) == 0: # not chunked
		
	
	return ( row, offset )

def makepng( fp, data, width, height, flags ):
	print( 'makepng( {0}, {1}, {2}, {3}, {4} )'.format( '{png}', '{data}', width, height, flags ) )
	
	dumped = 0
	
	png = pngfile( fp )
	
	for y in range( 0, height ):
		( row, offset ) = putspriterow( data, flags, y, width )
		if offset > dumped:
			dumped = offset
		
		png.write_row( row )
	
	return dumped

class pngfile:
	fp = None
	def __init__( self, fp ):
		self.fp = fp
		
	def write_row( self, row ):
		pass

from __future__ import print_function
import png
from .helper import uint8_t, getvalue, pack
from .locopal import locopalette, companycolours, MASKOUT

bgcol = 255
palettetype = 27

def putspriterow( data, data_offset, flags, y, width ):
	row = [bgcol] * width
	
	if ( flags & 4 ) == 0: # not chunked
		for i in range( width ):
			row[i] = uint8_t( data[ ( y * width ) + i ] )
		return ( row, ( y + 1 ) * width )
	
	offset = getvalue( data, 2 * y, 2 )
	
	last = False
	while not last:
		x = uint8_t( data[ offset ] )
		last = x & 0x80
		row_len = x & 0x7F
		offset += 1
		ofs = uint8_t( data[ offset ] )
		offset += 1
		
		for i in range( row_len ):
			row[ ofs + i ] = uint8_t( data[ offset ] )
			offset += 1
	
	return ( row, offset )

def makepng( fname, data, width, height, flags ):
	#print( 'makepng( {0}, {1}, {2}, {3}, {4} )'.format( fname, '{data}', width, height, flags ) )
	
	dumped = 0
	
	png = PNGWriter( fname, width, height )
	
	rows = []
	for y in range( height ):
		( row, offset ) = putspriterow( data, dumped, flags, y, width )
		if offset > dumped:
			dumped = offset
		rows.append( row )
	png.write_rows( rows )
	
	png.close()
	return dumped
	
def getspriterow( row, flags ):
	if not flags & 4:
		return row
	x1 = x2 = 0
	data = []
	width = len( row )
	offset = len( data )
	while x1 < width:
		while x1 < width and row[x1] == bgcol:
			x1 += 1
		if x1 < width:
			length = 1
			x2 = x1 + length
			while x2 < width and length < 127 and row[x2] != bgcol:
				x2 += 1
				length += 1
			offset = len( data )
			data.append( length )
			data.append( x1 )
			for i in range( length ):
				data.append( row[ x1 + i ] )
		else: # transparent to end of line
			if x2 == 0: # totally empty line
				data.append( 0 )
				data.append( 0 )
			x2 = x1
		x1 = x2
	data[ offset ] |= 0x80
	return data

def readpng( fname, flags ):
	r = png.Reader( filename = fname )
	data = []
	( width, height, pixels, ) = r.read()
	sprite_data = []
	if flags & 4:
		size = height * 2
		y = 0
	for row in pixels:
		sprite_row = getspriterow( row, flags )
		if flags & 4:
			data.extend( pack( '<H', size + y ) )
			y += len( sprite_row )
		sprite_data.extend( sprite_row )
	data.extend( sprite_data )
	return ( data, width, height )

class PNGWriter:
	fp = None
	w  = None
	def __init__( self, fname, w, h ):
		self.fp = open( fname, 'wb' )
		pal = list( locopalette )
		ccolind = ( palettetype & ~1 ) * 6 - 2
		if ccolind > 0:
			for i in range( 12 ):
				pal[ companycolours[i] ] = locopalette[ ccolind + i ]
			if palettetype & 1:
				for i in range( 12 ):
					pal[ ccolind + i ] = MASKOUT
		self.w = png.Writer( w, h, palette = pal, background = ( 0x70, ), gamma = 1.4 )
	def close( self ):
		self.fp.close()
		self.fp = None
		self.w = None
		
	def write_rows( self, rows ):
		self.w.write( self.fp, rows )

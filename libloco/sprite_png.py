from __future__ import print_function
import png
from helper import uint8_t, getvalue

from locopal import *

bgcol = 255
palettetype = 27

def putspriterow( data, data_offset, flags, y, width ):
	
	offset = 0
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
		self.w = png.Writer( w, h, palette = pal, background = ( 0, ), gamma = 1.4 )
	def close( self ):
		self.fp.close()
		self.fp = None
		self.w = None
		
	def write_rows( self, rows ):
		self.w.write( self.fp, rows )

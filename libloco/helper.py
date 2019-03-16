import struct
import sys
PY2 = sys.version_info[0] < 3

def ROR(x, n, bits = 32):
	mask = (2**n) - 1
	mask_bits = x & mask
	return (x >> n) | (mask_bits << (bits - n))

def ROL(x, n, bits = 32):
	return ROR(x, bits - n, bits)

def die(error_message):
	raise Exception(error_message)

def getstr( data ):
	s = r''
	for x in data:
		if x == '\x00' or x == 0:
			break
		s += chr(x) if not PY2 else x
	return s

def xml_str( inp ):
	inp = inp.replace( '&', '&amp;' )
	return inp
	
def a_to_b( a, b, inp ):
	return struct.unpack( b, struct.pack( a, inp ) )[0]
def uint8_to_int8( inp ):
	return a_to_b( 'B', 'b', inp )
def int8_to_uint8( inp ):
	return a_to_b( 'b', 'B', inp )
def uint16_to_int16( inp ):
	return a_to_b( 'H', 'h', inp )
def uint32_to_int32( inp ):
	return a_to_b( 'I', 'i', inp )

def uint8_t( inp ):
	if PY2:
		return struct.unpack( 'B', inp )[0]
	return struct.unpack( 'B', struct.pack('B', inp) )[0]

def raw_str_to_uint8_list( raw ):
	return map( lambda x: uint8_t( x ), raw )
	data = []
	for x in raw:
		data.append( uint8_t( x ) )
	return data
def uint8_list_to_raw_str( lst ):
	return bytes(lst)

def xml_hex_to_val( inp ):
	return inp

def vehnumtrack( data ):
	# 0x02 = class, 0xE0-0xE1 = vehflags (0xE1 & 2 == anytrack)
	# thus
	# if class < 2 and not anytrack:
	#	return 0
	# else:
	# return -1
	return 0 if ( uint8_t( data[2] ) < 2 ) and not ( uint8_t( data[0xE1] ) & 2 ) else -1
def vehnumrackrail( data ):
	return 0 if ( uint8_t( data[2] ) < 2 ) and ( uint8_t( data[0xE0] ) & 0x40 ) else -1

calcdescnum = [ vehnumtrack, vehnumrackrail ]

# code to test whether j is in the range allowed by num
# num < 0: no range
# num == 0: 0..0
# num > 0: 0..num-1
def loopescape(j,num):
	return ( (num < 0) or ( (num == 0) and (j > 0) ) or ( (num > 0) and (j >= num) ) )

def makenum( numdef ):
	ntype = uint8_to_int8( numdef >> 24 )
	arg = uint8_to_int8( ( numdef & 0xFF0000 ) >> 16 )
	num = uint16_to_int16( numdef & 0xFFFF )
	return ( ntype, arg, num )

def getnum( data, ofs, numdef ):
	#print 'getnum( {0}, {1}, {2} )'.format( '{data}', ofs, numdef )
	try:
		( ntype, arg, num ) = numdef
	except TypeError:	
		( ntype, arg, num ) = makenum( numdef )
	#print 'type, arg, num: {0}, {1}, {2}'.format( type, arg, num )

	if ntype == 0:
		return ( num, ofs )
	elif ntype == 1:
		if uint8_t( data[ ofs ] ) != 0xFF:
			return ( 0xffffff, ofs ) # return big number to not break the loop
		ofs += 1  # we just read a byte, so increment 1
		return ( -1, ofs ) # return -1 to guarantee loop break
	elif ntype == 2:
		num = uint8_t( data[ -num ] ) & arg
		return ( num if num != 0 else -1, ofs )
	elif ntype == 3:
		return ( 0 if uint8_t( data[ -num ] ) != 0 else -1, ofs )
	elif ntype == 4:
		return ( calcdescnum[ num ]( data ), ofs )
	elif ntype == -1:
		if num < 0:
			num = uint8_t( data[ -num ] )
			return ( num if num != 0 else -1, ofs )

	die( 'Invalid description count {0}'.format( ntype ) )

# return [ ntype, arg, num ]
def descnumuntil():
	#return [ 0x01, 0x00, 0x0000 ]
	return ( 0x01000000 )
def descnumand(x,y):
	#return [ 0x02, y & 0xFF, ( -x ) * 0xFF ]
	return ( 0x02000000 | ( ( ( y ) & 0xff ) << 16 ) | ( ( -x ) & 0xffff ) )
def descnumif(x):
	#return [ 0x03, 0x00, ( -x ) & 0xFFFF ]
	return ( 0x03000000 | ( ( -x ) & 0xffff ) )
def descnumspec( x ):
	#return [ 0x04, 0x00, x & 0xFFFF ]
	return ( 0x04000000 | ( ( x ) & 0xffff ) )


def getsvalue( data, ofs, size ):
	return getvalue( data, ofs, -size )
def getvalue( data, ofs, size ):
	sizes = { 1: 'b', 2: '<h', 4: '<i', 8: '<q' }
	if size > 0:
		return struct.unpack_from( sizes[ size ].upper(), data, ofs )[0]
	else:
		return struct.unpack_from( sizes[ abs( size ) ], data, ofs )[0]

def encodevalue( raw, size ):
	sizes = { 1: 'b', 2: '<h', 4: '<i', 8: '<q' }
	if size > 0:
		return raw_str_to_uint8_list( struct.pack( sizes[ size ].upper(), raw ) )
	else:
		return raw_str_to_uint8_list( struct.pack( sizes[ abs( size ) ], raw ) )

def pack( f, d ):
	return raw_str_to_uint8_list( struct.pack( f, d ) )
	
def structsize( a_vars ):
	return reduce( lambda t, v: t + ( abs( v.size ) * v.num ), a_vars, 0 )

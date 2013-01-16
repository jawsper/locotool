import xml.etree.ElementTree as ET
import struct

from .LocoFile import LocoFile
from helper import raw_str_to_uint8_list, uint8_list_to_raw_str
from helper import uint8_t, int8_to_uint8
from objects import *

def pack( f, d ):
	return raw_str_to_uint8_list( struct.pack( f, d ) )

class LocoEncoder(LocoFile):
	def encode( self ):
		xml_data = ET.parse( self.filename )
		root = xml_data.getroot()
		
		_name = root.attrib['name']
		
		output = open( 'j_{0}.dat'.format( _name.rstrip() ), 'wb' )
		output.write( self.parsexml( root ) )
		output.close()
		
	def parsexml( self, root ):
		_class    = int( root.attrib['class'], 16 )
		_subclass = int( root.attrib['subclass'], 16 )
		_name     = root.attrib['name']
		
		obj = objclasses[ _class & 0x7F ]
		
		raw = []
		
		print( _class, _subclass, _name )
		raw.append( _class )
		raw.append( _subclass & 0xFF )
		raw.append( ( _subclass >> 8 ) & 0xFF )
		raw.append( ( _subclass >> 16 ) & 0xFF )
		for i in range( 8 ):
			raw.append( uint8_t( _name[i] ) )
		for i in range( 4 ):
			raw.append( 0xFF ) # checksum todo
		
		for _chunk in root:
			if _chunk.tag != 'chunk':
				raise Exception( 'Expecting chunk, got {0}!'.format( _chunk.tag ) )
			compression = int( _chunk.attrib['compression'] )
			
			# steal the compression cheating from the c code :)
			if compression == 2:
				compression = 1
			
			raw.append( compression )
			
			chunk_data = self.chunk_encode( _chunk, obj )
			print chunk_data
			if compression == 0:
				pass
			elif compression == 1:
				chunk_data = self.chunk_rle_encode( chunk_data )
			else:
				raise Exception( 'Cannot encode chunk compression {0}!'.format( compression ) )
			
			#length!
			raw.extend( pack( '<I', len( chunk_data ) ) )
			raw.extend( chunk_data )
		return uint8_list_to_raw_str( raw )
		
	def chunk_encode( self, chunk, obj ):
		raw = []
		
		for cls in obj.desc:
			if cls.type == 'desc_objdata':
				print( 'desc_objdata' )
				raw.extend( self._encode_desc_objdata( chunk, obj.vars ) )
				
			elif cls.type == 'desc_lang':
				print( 'desc_lang' )
				raw.extend( self._encode_desc_lang( chunk, cls.param[0] ) )
				
			elif cls.type == 'desc_useobj':
				print( 'desc_useobj' )
				#j = 0
				#while True:
				#	( num, dumped ) = getnum( self.data, dumped, cls.param[0] )
				#	if loopescape( j, num ):
				#		break
				#	dumped += self._dumpuseobj( self.data[ dumped: ], j, num, cls.param[1], cls.param[2:] )
				#	j += 1
					
			elif cls.type == 'desc_auxdata':
				print( 'desc_auxdata' )
			elif cls.type == 'desc_auxdatafix':
				print( 'desc_auxdatafix' )
			elif cls.type == 'desc_auxdatavar':
				print( 'desc_auxdatavar' )
			elif cls.type == 'desc_strtable':
				print( 'desc_strtable' )
			elif cls.type == 'desc_cargo':
				print( 'desc_cargo' )
				#( num, dumped ) = getnum( self.data, dumped, cls.param[0] )
				#j = 0
				#while not loopescape( j, num ):
				#	dumped += self._dumpcap( self.data[ dumped: ], j, num )
				#	j += 1
			elif cls.type == 'desc_sprites':
				print( 'desc_sprites' )
				raw.extend( self._encode_desc_sprites( chunk ) )
				#dumped += self._dumpsprites( self.data[ dumped: ] )
			elif cls.type == 'desc_sounds':
				print( 'desc_sounds' )
				#dumped += self._dumpsounds( self.data[ dumped: ] )
			else:
				die( "Unknown obj description: {0}".format( cls.type ) )
		
		return raw
	#def test( self ):
	#	with open( self.filename, 'rb' ) as c:
	#		d = self.chunk_rle_encode( raw_str_to_uint8_list( c.read() ) )
	#		with open( self.filename + '.re-encoded', 'wb' ) as w:
	#			w.write( uint8_list_to_raw_str( d ) )
	def _encode_flags( self, bits, flags, size ):
		if size > 4:
			raise Exception( "Can't encode flags with {0} bytes".format( size ) )		
		value = 0		
		for i in range( size * 8 ):
			defname = None
			if i < len( flags ):
				name = flags[ i ]
			else:
				name = ""
			if len( name ) == 0:
				name = defname = 'bit_{0:X}'.format( i )
			print name
			state = 0
			for b in bits:
				if b.attrib['name'] == name:
					state = int( b.text )
					break
			value |= state << i
		return pack( '<I', value )
		
	def _encode_desc_objdata( self, chunk, vars ):
		data = []
		for v in vars:
			fname = v.name
			if len( fname ) == 0:
				fname = 'field_{0:X}'.format( v.ofs )
			for j in range( v.num ):
				name = fname
				if v.num > 1:
					name = '{0}[{1}]'.format( fname, j )
				size = v.size
				if size == 0:
					pass
				if v.flags != None:
					#value = chunk.find( 
					#data.extend( self._encode_flags( int( 
					print 'v.flags!'
					pass
				elif v.structvars != None:
					print 'v.structvars!'
				else:
					value = 0
					tag = 'variable' if len( v.name ) > 0 else 'unknown'
					for c in chunk.findall( tag ):
						if c.attrib['name'] == name:
							value = int( c.text )
							break
					data.extend( raw_str_to_uint8_list( v.encode( value ) ) )
		return data
		
	def _encode_desc_lang( self, chunk, num ):
		data = []
		
		for c in chunk.findall( 'description' ):
			if int( c.attrib['num'] ) == num:
				language = int( c.attrib['language'] )
				data.append( language )
				langstr = c.text
				if langstr:
					for x in langstr:
						data.append( ord( x ) )
				data.append( 0x00 )
		data.append( 0xFF )
		return data
		
	def _encode_desc_sprites( self, chunk ):
		data = [ 0x00 ] * 8
		
		num = len( chunk.findall( 'sprite' ) )
		size = 0
		spritedataoffset = 8 + 16 * num
		
		for c in chunk.findall( 'sprite' ):
			id = c.attrib['id']
			xofs = c.attrib['xofs']
			yofs = c.attrib['yofs']
			
			data.extend( [0xFE] * 4 ) # ofs
			data.extend( [0xFE] * 2 ) # width
			data.extend( [0xFE] * 2 ) # height
			data.extend( [0xFE] * 2 ) # xofs
			data.extend( [0xFE] * 2 ) # yofs
			data.extend( self._encode_flags( c.findall( 'bit' ), spriteflags, 4 ) ) # flags
			
		data[0:4] = pack( '<I', num )  # replace 0 TOT 4 met nieuwe data
		data[4:8] = pack( '<I', size ) # replace 4 TOT 8 met nieuwe data
		
		return data
		
	def chunk_rle_encode( self, data ):
		out = []
		length = len( data )
		ofs = 0
		while length > 0:
			start = ofs
			
			byte = data[ ofs ]
			ofs += 1
			length -= 1
			
			run = 1
			if length and byte == data[ ofs ]:
				while length and byte == data[ofs] and run < 127:
					run += 1
					ofs += 1
					length -= 1
				rle = -( run - 1 )
				out.append( int8_to_uint8( rle ) )
				out.append( byte )
			else:
				while length and byte != data[ofs] and run < 126:
					byte = data[ ofs ]
					run += 1
					ofs += 1
					length -= 1
				if length:
					run -= 1
					ofs -= 1
					length += 1
				rle = run - 1
				out.append( int8_to_uint8( rle ) )
				for i in range( start, start + run ):
					out.append( data[ i ] )
		return out
	
	def chunk_rle_compress( self, data ):
		pass

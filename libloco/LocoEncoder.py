import xml.etree.ElementTree as ET
import struct
import re

from .LocoFile import LocoFile
from helper import uint8_list_to_raw_str, raw_str_to_uint8_list
from helper import uint8_t, int8_to_uint8, pack
from objects import *
from .sprite_png import readpng

def ROR(x, n, bits = 32):
	mask = (2L**n) - 1
	mask_bits = x & mask
	return (x >> n) | (mask_bits << (bits - n))

def ROL(x, n, bits = 32):
	return ROR(x, bits - n, bits)

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

		#print( _class, _subclass, _name )
		raw.append( _class )
		raw.append( _subclass & 0xFF )
		raw.append( ( _subclass >> 8 ) & 0xFF )
		raw.append( ( _subclass >> 16 ) & 0xFF )
		for i in range( 8 ):
			raw.append( uint8_t( _name[i] ) )
		raw.extend( [ 0xFF ] * 4 ) # checksum gets calculated later

		c = 0xF369A75B
		c = ROL( c ^ raw[0], 11 )
		for i in range( 4, 12 ):
			c = ROL( c ^ raw[i], 11 )

		for _chunk in root:
			if _chunk.tag != 'chunk':
				raise Exception( 'Expecting chunk, got {0}!'.format( _chunk.tag ) )
			compression = int( _chunk.attrib['compression'] )

			# steal the compression cheating from the c code :)
			if compression == 2:
				compression = 1

			raw.append( compression )

			chunk_data = self.chunk_encode( _chunk, obj )

			for x in chunk_data:
				c = ROL( c ^ x, 11 )

			if compression == 0:
				pass
			elif compression == 1:
				chunk_data = self.chunk_rle_encode( chunk_data )
			else:
				raise Exception( 'Cannot encode chunk compression {0}!'.format( compression ) )

			raw.extend( pack( '<I', len( chunk_data ) ) )
			raw.extend( chunk_data )

		raw[ 0x0C : 0x10 ] = pack( '<I', c )
		return uint8_list_to_raw_str( raw )

	def chunk_encode( self, chunk, obj ):
		raw = []

		for cls in obj.desc:
			if cls.type == 'desc_objdata':
				raw.extend( self._encode_desc_objdata( chunk, obj.vars ) )

			elif cls.type == 'desc_lang':
				raw.extend( self._encode_desc_lang( chunk, cls.param[0] ) )

			elif cls.type == 'desc_useobj':
				for c in chunk.findall( 'useobject' ):
					if re.search( '^{0}(\\[\\d+\\])?$'.format( cls.param[1] ), c.attrib['desc'] ):
						raw.extend( pack( '<I', int( c.attrib['class'] ) ) )
						for i in range( 8 ):
							raw.append( uint8_t( c.text[i] ) )
						raw.extend( [0x00] * 4 )

			elif cls.type == 'desc_auxdata':
				print( 'desc_auxdata' )
				
			elif cls.type == 'desc_auxdatafix':
				print( 'desc_auxdatafix' )
				
			elif cls.type == 'desc_auxdatavar':
				raw.extend( self._encode_auxdata( chunk, obj.aux, cls.param[0], cls.param[2], -cls.param[3] ) )
			
			elif cls.type == 'desc_strtable':
				print( 'desc_strtable' )
				
			elif cls.type == 'desc_cargo':
				for c in chunk.findall( 'cargo' ):
					num = int( c.attrib['num'] )
					capacity = int( c.attrib['capacity'] )
					raw.extend( pack( 'B', capacity ) )
					for ct in c.findall( 'cargotype' ):
						cargotype = int( ct.attrib['id'] )
						refcap = int( ct.text )
						raw.extend( pack( 'B', cargotype ) )
						raw.extend( pack( '<H', refcap ) )
					raw.extend( [ 0xFF, 0xFF ] )
			elif cls.type == 'desc_sprites':
				raw.extend( self._encode_desc_sprites( chunk ) )
				
			elif cls.type == 'desc_sounds':
				print( 'desc_sounds' )
				raw.extend( self._encode_desc_sounds( chunk ) )
				
			else:
				die( "Unknown obj description: {0}".format( cls.type ) )

		return raw

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
			#print name
			state = 0
			for b in bits:
				if b.attrib['name'] == name:
					state = int( b.text )
					break
			value |= state << i
		return value

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
					for c in chunk.findall( 'bitmask' ):
						if c.attrib['name'] == name:
							data.extend( v.encode( self._encode_flags( c.findall( 'bit' ), v.flags, v.size ) ) )
							break
					pass
				elif v.structvars != None:
					for c in chunk.findall( 'structure' ):
						if c.attrib['name'] == name:
							data.extend( self._encode_desc_objdata( c, v.structvars ) )
							break
				else:
					value = 0
					tag = 'variable' if len( v.name ) > 0 else 'unknown'
					for c in chunk.findall( tag ):
						if c.attrib['name'] == name:
							value = int( c.text )
							break
					data.extend( v.encode( value ) )
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

	def _encode_auxdata( self, chunk, aux, nameind, size, num ):
		data = []
		
		basename = 'aux_{0}'.format( nameind )
		auxname = aux[nameind].name
		if len( auxname ) == 0:
			auxname = basename
		
		for c in chunk.findall( 'auxdata' ):
			a_name = c.attrib['name']
			if re.search( '^{0}\\[?'.format( auxname ), a_name ):
				size = int( c.attrib['size'] )
				num = int( c.attrib['num'] )
				type = int( c.attrib['type'] )
				if size < 0:
					num *= -size
					size = 1
				
				vars = aux[nameind].vars
				if not vars:
					vars = [ varinf( 0x00, size, 0, '' ) ]
				siz = structsize( vars )
				if siz != num * size:
					vars[0].num = 1
					siz = structsize( vars )
					vars[0].num = num * size / siz
					if vars[0].num * siz != size * num:
						raise Exception( "{0} size {1}*{2} != {3}*{4}".format( name, siz, vars[0].num, size, num ) )
		
				data.extend( self._encode_desc_objdata( c, vars ) )
		data.extend( [ 0xFF ] )
		return data

	def _encode_desc_sprites( self, chunk ):
		data = [ 0x00 ] * 8

		num = len( chunk.findall( 'sprite' ) )
		size = 0
		spritedata = []
		spritedataoffset = 8 + 16 * num

		ofs = 0
		for c in chunk.findall( 'sprite' ):
			fname = c.find( 'pngfile' ).text
			id = c.attrib['id']
			xofs = int(c.attrib['xofs'])
			yofs = int(c.attrib['yofs'])
			flags = self._encode_flags( c.findall( 'bit' ), spriteflags, 4 )
			( pixels, width, height ) = readpng( fname, flags )

			data.extend( pack( '<I', ofs ) ) # ofs
			data.extend( pack( '<H', width ) ) # width
			data.extend( pack( '<H', height ) ) # height
			data.extend( pack( '<h', xofs ) ) # xofs
			data.extend( pack( '<h', yofs ) ) # yofs
			data.extend( pack( '<I', flags ) ) # flags

			spritedata.extend( pixels )
			ofs += len( pixels )

		data[0:4] = pack( '<I', num ) # replace 0 TOT 4 met nieuwe data
		data[4:8] = pack( '<I', len( spritedata ) ) # replace 4 TOT 8 met nieuwe data
		data.extend( spritedata )
		return data

	def _encode_desc_sounds( self, chunk ):
		data = []
		for c in chunk.findall( 'wavfile' ):
			with open( c.text, 'rb' ) as wf:
				raw_wav = raw_str_to_uint8_list( wf.read() )
			length = len( raw_wav ) - 0x2C
			data.extend( pack( '<I', 1 ) )
			data.extend( pack( '<I', length + 16 + 8 + 4 ) )
			data.extend( [ 0x00 ] * 16 )
			data.extend( pack( '<I', 1 ) )
			data.extend( pack( '<I', 8 ) )
			data.extend( pack( '<I', length - int( c.attrib['size'] ) ) )
			for i in range( 16 ):
				data.append( raw_wav[0x14 + i] )
			for i in range( length ):
				data.append( raw_wav[0x2c + i] )

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

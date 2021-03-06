from __future__ import print_function
import xml.etree.ElementTree as ET
import re

from .LocoFile import LocoFile
from .helper import uint8_list_to_raw_str, raw_str_to_uint8_list
from .helper import uint8_t, int8_to_uint8, pack, ROL, structsize, makenum
from .objects import objclasses, spriteflags
from .sprite_png import readpng, getspriterow
from .structs import varinf


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
			raw.append( ord( _name[i] ) )
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
			elif compression == 3:
				chunk_data = self.chunk_scramble( chunk_data )
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
				is_array = False
				for c in chunk.findall( 'useobject' ):
					if cls.param[1] == c.attrib['desc']:
						raw.extend( pack( '<I', int( c.attrib['class'] ) ) )
						for i in range( 8 ):
							raw.append( ord( c.text[i] ) )
						raw.extend( [0x00] * 4 )
						break
					m = re.search( '^{0}\\[(\\d+)\\]$'.format( cls.param[1] ), c.attrib['desc'] )
					if m:
						is_array = True
						raw.extend( pack( '<I', int( c.attrib['class'] ) ) )
						for i in range( 8 ):
							raw.append( ord( c.text[i] ) )
						raw.extend( [0x00] * 4 )
				if is_array:
					raw.append( 0xFF )

			elif cls.type == 'desc_auxdata': # param: nameind numaux* size num*
				raw.extend( self._encode_auxdata( chunk, obj.aux, cls ) )
				
			elif cls.type == 'desc_auxdatafix': # param: nameind numaux* size numsize
				raw.extend( self._encode_auxdata( chunk, obj.aux, cls ) )
				
			elif cls.type == 'desc_auxdatavar': # param: nameind numaux* size type
				raw.extend( self._encode_auxdata( chunk, obj.aux, cls ) )
			
			elif cls.type == 'desc_strtable':
				raw.extend( self._encode_strtable( chunk, cls.param[0], cls.param[1] ) )
				
			elif cls.type == 'desc_cargo':
				for c in chunk.findall( 'cargo' ):
					#num = int( c.attrib['num'] )
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
				raise Exception( "Unknown obj description: {0}".format( cls.type ) )

		return raw

	def _encode_flags( self, bits, flags, size ):
		if size > 4:
			raise Exception( "Can't encode flags with {0} bytes".format( size ) )
		value = 0
		for i in range( size * 8 ):
			if i < len( flags ):
				name = flags[ i ]
			else:
				name = ""
			if len( name ) == 0:
				name = 'bit_{0:X}'.format( i )
			#print name
			state = 0
			for b in bits:
				if b.attrib['name'] == name:
					state = int( b.text )
					break
			value |= state << i
		return value

	def _encode_desc_objdata( self, chunk, a_vars ):
		data = []
		for v in a_vars:
			fname = v.name
			if len( fname ) == 0:
				fname = 'field_{0:X}'.format( v.ofs )
			#print( 'fname: {0}; v.size: {1}; v.num: {2}'.format( fname, v.size, v.num ) )
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

	def _encode_auxdata( self, chunk, aux, cls ):
		data = []
		nameind = cls.param[0]
		size = cls.param[2]
		
		basename = 'aux_{0}'.format( nameind )
		auxname = aux[nameind].name
		if len( auxname ) == 0:
			auxname = basename
		
		a_id = 0
		is_array = False
		for c in chunk.findall( 'auxdata' ):
			ok = False
			a_name = c.attrib['name']
			s = re.search( '^{0}\\[(\d+)\\]$'.format( auxname ), a_name )
			if s:
				is_array = True
				if int( s.group(1) ) == a_id:
					ok = True
				a_id += 1
			elif auxname == a_name:
				ok = True
			if ok:
				#size = int( c.attrib['size'] )
				num = int( c.attrib['num'] )
				#type = int( c.attrib['type'] )
				if size < 0:
					num *= -size
					size = 1
				
				aux_vars = aux[nameind].vars
				if not aux_vars:
					aux_vars = [ varinf( 0x00, size, 0, '' ) ]
				siz = structsize( aux_vars )
				if siz != num * size:
					aux_vars[0].num = 1
					siz = structsize( aux_vars )
					aux_vars[0].num = num * size / siz
					if aux_vars[0].num * siz != size * num:
						name = ''
						raise Exception( "{0} size {1}*{2} != {3}*{4}".format( name, siz, aux_vars[0].num, size, num ) )
				data.extend( self._encode_desc_objdata( c, aux_vars ) )
				if cls.type == 'desc_auxdatavar' and is_array:
					data.append( 0xFF )
		
		if cls.type == 'desc_auxdatavar' and not is_array:
			data.append( 0xFF )
		#return map( lambda x: 0xFA, data )
		return data
		
	def _encode_strtable( self, chunk, a_id, num_offset ):
		data = []
		for c in chunk.findall( 'stringtable' ):
			if int( c.attrib['id'] ) == a_id:
				num = int( c.attrib['num'] )
				str_data = []
				for s in c:
					#str_id = int( s.attrib['id'] )
					data.extend( pack( '<H', num * 2 + len( str_data ) ) )
					str_type = int( s.attrib['type'] )
					str_text = s.text
					for char in str_text:
						str_data.append( uint8_t( char ) )
					str_data.append( 0x00 )
					str_data.append( str_type )
				data.extend( str_data )
		return data
		
	def _encode_desc_sprites( self, chunk ):
		data = [ 0x00 ] * 8

		num = len( chunk.findall( 'sprite' ) )
		size = 0
		spritedata = []
		#spritedataoffset = 8 + 16 * num

		ofs = 0
		old = []
		for c in chunk.findall( 'sprite' ):
			#id = c.attrib['id']
			xofs = int( c.attrib['xofs'] )
			yofs = int( c.attrib['yofs'] )
			flags = self._encode_flags( c.findall( 'bit' ), spriteflags, 4 )
			
			wr_ofs = ofs
			if c.find( 'stub' ) != None:
				width = 1
				height = 1
				pixels = []
				if flags & 4:
					size = height * 2
					pixels.extend( pack( '<H', size ) )
				pixels.extend( getspriterow( [ int( c.find( 'stub' ).text ) ], flags ) )
			elif c.find( 'pngfile' ) != None:
				( pixels, width, height ) = readpng( c.find( 'pngfile' ).text, flags )
			elif flags & 0x40:
				pixels = []
				( wr_ofs, width, height ) = old
			else:
				pixels = []
				width = 0
				height = 0

			data.extend( pack( '<I', wr_ofs ) ) # ofs
			data.extend( pack( '<H', width ) ) # width
			data.extend( pack( '<H', height ) ) # height
			data.extend( pack( '<h', xofs ) ) # xofs
			data.extend( pack( '<h', yofs ) ) # yofs
			data.extend( pack( '<I', flags ) ) # flags

			if len( pixels ) > 0:
				old = ( ofs, width, height )
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
				while length and byte == data[ ofs ] and run < 127:
					run += 1
					ofs += 1
					length -= 1
				rle = -( run - 1 )
				out.append( int8_to_uint8( rle ) )
				out.append( byte )
			else:
				while length and byte != data[ ofs ] and run < 126:
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
		
	def chunk_scramble( self, data ):
		out = []
		bits = 1
		for b in data:
			out.append( ROL( b, bits, 8 ) )
			bits = ( bits + 2 ) & 7
		return out

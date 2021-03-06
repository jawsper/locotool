from __future__ import print_function
import struct

from .objects import objclasses, spriteflags
from .sprite_png import makepng, putspriterow
from .structs import varinf
from .helper import structsize, xml_str, die, getnum, loopescape
from .helper import uint32_to_int32, getstr
from .helper import getvalue, getsvalue, uint8_t

import sys
PY2 = sys.version_info[0] < 3

pos_struct = 0
pos_desc = 3

pos_desc_type = 0
pos_desc_params = 1

class Chunk:
	allunknown = False
	onlysetbits = False

	def __init__( self, data, locofile = None ):
		if locofile:
			self.loco = locofile
			self._class = locofile._class
		self.data = data
		
	def decode( self, xml ):
		self.xml = xml
		indent = 1
		obj = objclasses[ self._class ]
		dumped = 0
		
		for cls in obj.desc:
			if cls.type == 'desc_objdata': # params: -
				dumped += self._dumpobjdata( self.data[ dumped: ], obj.vars, indent )
			
			elif cls.type == 'desc_lang': # params: langid
				dumped += self._dumplang( self.data[ dumped: ], cls.param[0] ) 
			
			elif cls.type == 'desc_useobj': # params: num*, type, classes...
				j = 0
				while True:
					( num, dumped ) = getnum( self.data, dumped, cls.param[0] )
					if loopescape( j, num ):
						break
					dumped += self._dumpuseobj( self.data[ dumped: ], j, num, cls.param[1], cls.param[2:] )
					j += 1
			
			elif cls.type == 'desc_auxdata': # params: nameind, numaux*, size, num*
				( num,  dumped ) = getnum( self.data, dumped, cls.param[1] )
				( num2, dumped ) = getnum( self.data, dumped, cls.param[3] )
				num  = uint32_to_int32( num )
				num2 = uint32_to_int32( num2 )
				j = 0
				while not loopescape( j, num ):
					dumped += self._dumpaux( self.data[ dumped: ], obj.aux, cls.param[0], j, num, cls.param[2], num2 )
					j += 1
			
			elif cls.type == 'desc_auxdatafix': # params: nameind, numaux*, size, numsize
				( num,  dumped ) = getnum( self.data, dumped, cls.param[1] )
				j = 0
				while not loopescape( j, num ):
					num2 = getvalue( self.data, dumped, cls.param[3] )
					dumped += cls.param[3]
					dumped += self._dumpaux( self.data[ dumped: ], obj.aux, cls.param[0], j, num, cls.param[2], num2 )
					j += 1
			
			elif cls.type == 'desc_auxdatavar': # params: nameind, numaux*, size, type
				( num, dumped ) = getnum( self.data, dumped, cls.param[1] )
				j = 0
				while not loopescape( j, num ):
					dumped += self._dumpaux( self.data[ dumped: ], obj.aux, cls.param[0], j, num, cls.param[2], -cls.param[3] )
					j += 1
			
			elif cls.type == 'desc_strtable': # params: id, num*, ofs*
				dumped += self._dumpstrtable( self.data[ dumped: ], cls.param[0], uint8_t( self.data[cls.param[1]] ) )
			
			elif cls.type == 'desc_cargo': # params: num*
				( num, dumped ) = getnum( self.data, dumped, cls.param[0] )
				j = 0
				while not loopescape( j, num ):
					dumped += self._dumpcap( self.data[ dumped: ], j, num )
					j += 1
			
			elif cls.type == 'desc_sprites': # params: -
				dumped += self._dumpsprites( self.data[ dumped: ] )
			
			elif cls.type == 'desc_sounds': # params: -
				dumped += self._dumpsounds( self.data[ dumped: ] )
			
			else:
				die( "Unknown obj description: {0}".format( cls.type ) )

	def _printxml( self, indent, s ):
		self.xml.write( '{0}{1}\n'.format( '\t' * indent, s ) )
		pass
		
	# write a bit field
	def _dumpflags( self, value, flags, size, indent ):
		if size > 4:
			die( "Can't dump flags with {0} bytes".format( size ) )
		
		for i in range( size * 8 ):
			defname = None
			if i < len( flags ):
				name = flags[ i ]
			else:
				name = ""
			if len( name ) == 0:
				name = defname = 'bit_{0:X}'.format( i )
			state = ( value & ( 1 << i ) ) >> i
			if ( ( ( not self.onlysetbits ) and name != defname ) or state ):
				self._printxml( indent, '<bit name="{0}">{1}</bit>'.format( name, state ) )
		return size
		
	# dump a structure to the xml file, structure definition in the vars parameter
	def _dumpobjdata( self, data, a_vars, indent ):
		totaldumped = 0
		ofs = 0
		for v in a_vars:
			fname = v.name
			if len( fname ) == 0:
				fname = 'field_{0:X}'.format( v.ofs )
			if ofs != v.ofs:
				die( 'Structure is invalid, ofs={0:X} but next field is {1:X}'.format( ofs, v.ofs ) )
			
			for j in range( v.num ):
				name = fname
				if v.num > 1:
					name = '{0}[{1}]'.format( fname, j )
				
				size = v.size
				if size == 0:
					pass
				
				if v.flags != None:
					self._printxml( indent, '<bitmask name="{0}" size="{1}">'.format( name, size ) )
					dumped = self._dumpflags( v.getvalue( data, j ), v.flags, size, indent + 1 )
					self._printxml( indent,  '</bitmask>' )
				elif v.structvars != None:
					self._printxml( indent, '<structure name="{0}" size="{1}">'.format( name, size ) )
					dumped = self._dumpobjdata( data[ ofs: ], v.structvars, indent + 1 )
					self._printxml( indent, '</structure>' )
				else:
					value = v.getvalue( data, j )
					size = abs( size )
					tag = 'variable'
					if len( v.name ) == 0:
						tag = 'unknown' if value != 0 or self.allunknown else None # don't print unset unknown variables
					if tag != None:
						self._printxml( indent, '<{0} name="{1}" size="{2:X}">{3}</{0}>'.format( tag, name, size, value ) )
					dumped = size
				ofs += dumped
				totaldumped += dumped
		return totaldumped
		
	# dump the language/description info
	# those are a bunch of zero-terminated strings preceeded by the language byte
	def _dumplang( self, data, num ):
		ofs = 0
		
		language = uint8_t( data[ ofs ] )
		ofs += 1 # lang
		while language != 0xFF:
			lang_str = ''
			while uint8_t( data[ ofs ] ) != 0x00:
				lang_str += chr(data[ ofs ]) if not PY2 else data[ofs]
				ofs += 1 # char
			ofs += 1 # 0
			lang_str = xml_str( lang_str )
			self._printxml( 1, '<description num="{0}" language="{1}">{2}</description>'.format( num, language, lang_str ) )
			language = uint8_t( data[ ofs ] )
			ofs += 1 # lang
		
		return ofs
		
	# dump an object dependence (i.e. an outside object that this object depends on)
	def _dumpuseobj( self, data, num, total, typename, classes ):
		#print '_dumpuseobj( {0}, {1}, {2}, {3} )'.format( num, total, typename, classes )
		if total > 1:
			typename = '{0}[{1}]'.format( typename, num )
		
		classok = False
		
		for c in classes:
			if c == uint8_t( data[0] ) or c == 0x100:
				classok = True
		
		if not classok:
			die( 'Not correct class for {0}: {1:02X}'.format( typename, uint8_t( data[0] ) ) )
		
		self._printxml( 1, '<useobject desc="{0}" class="{1}">{2}</useobject>'.format( typename, uint8_t( data[0] ), getstr( data[4:] ) ) )
		
		return 16
	
	# dump a cargo capacity entry with various cargo types
	def _dumpcap( self, data, num, total ):
		capacity = uint8_t( data[0] )
		dumped = 1
		if capacity != 0:
			self._printxml( 1, '<cargo num="{0}" capacity="{1}">'.format( num, capacity ) )
			while getvalue( data, dumped, 2 ) != 0xFFFF:
				cargotype = uint8_t( data[ dumped ] )
				dumped += 1
				refcap = getvalue( data, dumped, 2 )
				dumped += 2
				self._printxml( 2, '<cargotype id="{0}">{1}</cargotype>'.format( cargotype, refcap ) )
			dumped += 2
			self._printxml( 1, '</cargo>' )
		return dumped
	
	# dump the list of sprites plus their contents
	def _dumpsprites( self, data ):
		
		num = getvalue( data, 0, 4 )
		size = getvalue( data, 4, 4 )
		dumped = 8
		spritedataoffset = 8 + 16 * num
		totalsize = 0
		
		for i in range( 0, num ):
			ofs = getvalue( data, dumped, 4 )
			dumped += 4
			width = getvalue( data, dumped, 2 )
			dumped += 2
			height = getvalue( data, dumped, 2 )
			dumped += 2
			xofs = getsvalue( data, dumped, 2 )
			dumped += 2
			yofs = getsvalue( data, dumped, 2 )
			dumped += 2
			flags = getvalue( data, dumped, 4 )
			dumped += 4
			
			self._printxml( 1, '<sprite id="{0}" xofs="{1}" yofs="{2}">'.format( i, xofs, yofs ) )
			self._dumpflags( flags, spriteflags, 4, 2 )
			
			spritesize = 0
			if width == 1 and height == 1:
				( row, ofs ) = putspriterow( data[ spritedataoffset + ofs: ], 0, flags, 0, width )
				self._printxml( 2, '<stub>{0}</stub>'.format( row[0] ) )
			elif flags & 0x40:
				spritesize = 0
			else:
				pngname = self.loco.makepngname( i )
				spritesize = makepng( pngname, data[ spritedataoffset + ofs: ], width, height, flags )
				self._printxml( 2, '<pngfile>{0}</pngfile>'.format( pngname ) )
			
			totalsize += spritesize
			self._printxml( 1, '</sprite>' )
		return size
		dumped += totalsize
		return dumped
		
	def _dumpaux( self, data, aux, nameind, a_id, numid, size, num ):
		basename = 'aux_{0}'.format( nameind )
		auxname = aux[nameind].name
		if len( auxname ) == 0:
			auxname = basename
		
		if numid:
			name = '{0}[{1}]'.format( auxname, a_id )
		else:
			name = auxname
			
		atype = 0
		dumped = 0
		siz = abs( size )
		if num < 0:
			atype = -num
			num = 0
			i = 0
			while getsvalue( data, i, atype ) != -1:
				num += 1
				i += siz
			dumped += atype
		
		self._printxml( 1, '<auxdata name="{0}" size="{1}" num="{2}" type="{3}">'.format( name, siz, num, atype ) )
		
		if size < 0:
			num *= -size
			size = 1
		
		
		avars = aux[nameind].vars
		if not avars:
			avars = [ varinf( 0x00, size, 0, '' ) ]
		
		siz = structsize( avars )
		if siz != num * size:
			avars[0].num = 1
			siz = structsize( avars )
			avars[0].num = num * size / siz
			if avars[0].num * siz != size * num:
				raise Exception( "{0} size {1}*{2} != {3}*{4}".format( name, siz, avars[0].num, size, num ) )
		
		dumped += self._dumpobjdata( data, avars, 2 )
		
		self._printxml( 1, '</auxdata>' )
		
		return dumped
	
	def _dumpstrtable( self, data, a_id, num ):
		dumped = num * 2
		self._printxml( 1, '<stringtable id="{0}" num="{1}">'.format( a_id, num ) )
		for i in range( num ):
			dumped = getvalue( data, i * 2, 2 )
			curr_str = getstr( data[ dumped: ] )
			self._printxml( 2, '<string id="{0}" type="{1}">{2}</string>'.format( i, uint8_t( data[ dumped + len( curr_str ) + 1 ] ), curr_str ) )
			dumped += len( curr_str ) + 2
		self._printxml( 1, '</stringtable>' )
		return dumped
	
	def _dumpsounds( self, data ):
		dumped = 0
		
		if getvalue( data, dumped, 4 ) != 1:
			die( 'Unsupported number of samples' )
		dumped += 4
		
		length = getvalue( data, dumped, 4 )
		dumped += 4
		
		for i in range( 0, 4 ):
			if getvalue( data, dumped, 4 ) != 0:
				die( 'Unsupported aux data in sample header' )
			dumped += 4
		
		if getvalue( data, dumped, 4 ) != 1:
			die( 'Unsupported number of samples' )
		dumped += 4
		
		if getvalue( data, dumped, 4 ) != 8:
			die( 'Unsupported sample header size' )
		dumped += 4
		
		wavlen = getvalue( data, dumped, 4 )
		dumped += 4
		
		# extra bytes which I do not understand
		extra = length - ( 16 + 8 + 4 + wavlen )
		wavlen += extra
		
		wavname = self.loco.makefilename( '.wav' )
		
		self._printxml( 1, '<wavfile size="{0}">{1}</wavfile>'.format( extra, wavname ) )
		
		with open( wavname, 'wb' ) as wf:
			wf.write( r'RIFF' )
			
			length = 8+4+16+4+4+wavlen	# "WAVEfmt "+len+header+"data"+len+wavedata
			wf.write( struct.pack( '<I', length ) )
			
			wf.write( r'WAVEfmt ' )
			
			length = 16
			wf.write( struct.pack( '<I', length ) )
			for i in range( length ):
				wf.write( data[ dumped + i ] )
			dumped += length
			
			wf.write( r'data' )
			
			wf.write( struct.pack( '<I', wavlen ) )
			for i in range( wavlen ):
				wf.write( data[ dumped + i ] )
			dumped += wavlen
		
		return dumped


from __future__ import print_function
from objects import *
from sprite_png import *
import struct

pos_struct = 0
pos_desc = 3

pos_desc_type = 0
pos_desc_params = 1

class Chunk:
	allunknown = False
	onlysetbits = True

	def __init__( self, locofile, data ):
		self.loco = locofile
		self.xml = locofile.xml
		self._class = locofile._class
		self.data = data

	def dump( self ):
		indent = 1
		obj = objclasses[ self._class ]
		dumped = 0
		if obj  == 0:
			die( 'Objclass 0x{0:02X} not implemented yet'.format( self._class ) )
		for cls in obj.desc:
			if cls.type == 'desc_objdata':
				dumped += self._dumpobjdata( self.data[ dumped: ], obj.vars, indent )
				
			elif cls.type == 'desc_lang':
				dumped += self._dumplang( self.data[ dumped: ], cls.param[0] ) 
				
			elif cls.type == 'desc_useobj':
				#print 'desc_useobj'
				#print cls.param
				j = 0
				while True:
					( num, dumped ) = getnum( self.data, dumped, cls.param[0] )
					if loopescape( j, num ):
						break
					dumped += self._dumpuseobj( self.data[ dumped: ], j, num, cls.param[1], cls.param[2:] )
					j += 1
					
			elif cls.type == 'desc_auxdata':
				print( 'desc_auxdata' )
				pass
			elif cls.type == 'desc_auxdatafix':
				print( 'desc_auxdatafix' )
				pass
			elif cls.type == 'desc_auxdatavar':
				print( 'desc_auxdatavar' )
				pass
			elif cls.type == 'desc_strtable':
				print( 'desc_strtable' )
				pass
			elif cls.type == 'desc_cargo':
				( num, dumped ) = getnum( self.data, dumped, cls.param[0] )
				j = 0
				while not loopescape( j, num ):
					dumped += self._dumpcap( self.data[ dumped: ], j, num )
					j += 1
			elif cls.type == 'desc_sprites':
				dumped += self._dumpsprites( self.data[ dumped: ] )
			elif cls.type == 'desc_sounds':
				dumped += self._dumpsounds( self.data[ dumped: ] )
			else:
				die( "Unknown obj description: {0}".format( cls.type ) )

	def _printxml( self, indent, str ):
		self.xml.write( '{0}{1}\n'.format( '\t' * indent, str ) )
		pass
		
	# write a bit field
	def _dumpflags( self, value, flags, size, indent ):
		for i in range( 0, size * 8 ):
			if i < len( flags ):
				name = flags[ i ]
			else:
				name = ""
			defname = None
			if len( name ) == 0:
				name = defname = 'bit_{0:X}'.format( i )
			state = ( value & ( 1 << i ) ) >> i
			#print state, defname, name, value, i
			if ( ( ( not self.onlysetbits ) and ( defname != name ) ) or state != 0 ):
				self._printxml( indent, '<bit name="{0}">{1}</bit>'.format( name, state ) )
		return size
		
	# dump a structure to the xml file, structure definition in the vars parameter
	def _dumpobjdata( self, data, vars, indent ):
		totaldumped = 0
		ofs = 0
		for v in vars:
			fname = v.name
			if len( fname ) == 0:
				fname = 'field_{0:X}'.format( v.ofs )
			if ofs != v.ofs:
				die( 'Structure is invalid, ofs={0:X} but next field is {1:X}'.format( ofs, v.ofs ) )
			for j in range( 0, v.num ):
				name = fname
				if v.num > 1:
					name = '{0}[{1}]'.format( fname, j )
				
				size = v.size
				if size == 0:
					pass
				
				if v.flags != None:
					self._printxml( indent, '<bitmask name="{0}" size="{1}">'.format( name, size ) )
					dumped = self._dumpflags( v.getvalue( data ), v.flags, size, indent + 1 )
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
		
		language = struct.unpack( 'B', data[ ofs ] )[0]
		ofs += 1
		while language != 0xFF:
			lang_str = ''
			while data[ ofs ] != '\x00':
				#print ofs, data[ ofs ]
				lang_str += data[ ofs ]
				ofs += 1
			ofs += 1
			self._printxml( 1, '<description num="{0}" language="{1}">{2}</description>'.format( num, language, lang_str ) )
			language = struct.unpack( 'B', data[ ofs ] )[0]
			ofs += 1
		
		return ofs
		
	# dump an object dependence (i.e. an outside object that this object depends on)
	def _dumpuseobj( self, data, num, total, type, classes ):
		#print '_dumpuseobj( {0}, {1}, {2}, {3} )'.format( num, total, type, classes )
		typename = type
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
				self._printxml( 2, '<stub>{0}</stub>' )
			elif flags & 0x40:
				pass
			else:
				pngname = self.loco.makepngname( i )
				with open( pngname, 'w' ) as png:
					spritesize = makepng( png, data[ spritedataoffset + ofs: ], width, height, flags )
				self._printxml( 2, '<pngfile>{0}</pngfile>'.format( pngname ) )
			
			totalsize += spritesize
			self._printxml( 1, '</sprite>' )
		return size
		dumped += totalsize
		return dumped
		
	def _dumpaux( self ):
		pass
	def _dumpstrtable( self ):
		pass
		
	def _dumpsounds( self, data ):
		dumped = 0
		
		if getvalue( data, dumped, 4 ) != 1:
			die( 'Unsupported number of samples' )
		dumped += 4
		
		len = getvalue( data, dumped, 4 )
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
		extra = len - ( 16 + 8 + 4 + wavlen )
		wavlen += extra
		
		wavname = self.loco.makefilename( '.wav' )
		
		self._printxml( 1, '<wavfile size="{0}">{1}</wavfile>'.format( extra, wavname ) )
		
		dumped += len
		dumped += wavlen
		
		return dumped
	
from .helper import getvalue, encodevalue

class varinf:
	ofs = 0
	size = 0
	num = 0
	name = ""
	structvars = None
	flags = None
	
	def __init__( self, ofs, size, num, name, structvars = None, flags = None ):
		self.ofs = ofs
		self.size = size
		self.num = num
		self.name = name
		self.structvars = structvars
		self.flags = flags
	def __str__( self ):
		return 'varinf( {0}, {1}, {2}, "{3}" )'.format( self.ofs, self.size, self.num, self.name )
	def __repr__( self ):
		return self.__str__()
		
	def getvalue( self, data, n = 0 ):
		return getvalue( data, self.ofs + ( n * self.size ), self.size )
	def encode( self, raw ):
		return encodevalue( raw, self.size )
class objdesc:
	type = None
	param = None
	
	def __init__( self, type, param = None ):
		self.type = type
		self.param = param
	def __str__( self ):
		return 'objdesc( {0}, {1} )'.format( self.type, self.param )
	def __repr__( self ):
		return self.__str__()
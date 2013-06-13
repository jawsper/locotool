class auxdesc:
	name = None
	vars = None
	
	def __init__( self, name, vars ):
		self.name = name
		self.vars = vars
	def __str__( self ):
		return 'auxdesc( "{0}", {1} )'.format( self.name, self.vars )
	def __repr__( self ):
		return self.__str__()

class objclass:
	vars = None
	size = 0
	aux = None
	desc = None
	
	def __init__( self, vars, size, aux, desc ):
		self.vars = vars
		self.size = size
		self.aux = aux
		self.desc = desc
	def __str__( self ):
		return 'objclass( {0}, {1}, {2}, {3} )'.format( self.vars, self.size, self.aux, self.desc )
	def __repr__( self ):
		return self.__str__()
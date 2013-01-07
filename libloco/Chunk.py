from objects import *

pos_struct = 0
pos_desc = 3

pos_desc_type = 0
pos_desc_params = 1

class Chunk:
	def __init__( self, _class, data ):
		self._class = _class
		self.data = data
		print 'Chunk! {0} Bytes'.format( len( data ) )
		pass
	def dump( self ):
		
		for cls in objclasses[ self._class ][ pos_desc ]:
			print 'objclass:'
			print cls[ pos_desc_type ]



class auxdesc:
    name = None
    vars = None
    
    def __init__( self, name, a_vars ):
        self.name = name
        self.vars = a_vars
    def __str__( self ):
        return 'auxdesc( "{0}", {1} )'.format( self.name, self.vars )
    def __repr__( self ):
        return self.__str__()

class objclass:
    vars = None
    size = 0
    aux = None
    desc = None
    
    def __init__( self, a_vars, size, aux, desc ):
        self.vars = a_vars
        self.size = size
        self.aux = aux
        self.desc = desc
    def __str__( self ):
        return 'objclass( {0}, {1}, {2}, {3} )'.format( self.vars, self.size, self.aux, self.desc )
    def __repr__( self ):
        return self.__str__()
    
class objdesc:
    type = None
    param = None
    
    def __init__( self, a_type, param = None ):
        self.type = a_type
        self.param = param
    def __str__( self ):
        return 'objdesc( {0}, {1} )'.format( self.type, self.param )
    def __repr__( self ):
        return self.__str__()
    
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
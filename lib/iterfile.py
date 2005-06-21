import pyfits

__version__ = '0.1 (20-June-2005)'



class IterFitsFile(object):
    """ This class defines an object which can be used to
        access the data from a FITS file without leaving
        the file-handle open between reads. 

    """
    def __init__(self,name):
        self.name = name
        self.fname = None
        self.extn = None
        
        self.handle = None
        
        if not self.fname:
            self.fname,self.extn = parseFilename(name)

            
    def _shape(self):
        """ Returns the shape of the data array associated with this file."""
        hdu = self.open()
        _shape = hdu.data.shape
        self.close()
        del hdu
        return _shape

    def _data(self):
        """ Returns the data array associated with this file/extenstion."""
        hdu = self.open()
        _data = hdu.data
        self.close()
        del hdu
        return _data
        

    def type(self):
        """ Returns the shape of the data array associated with this file."""
        hdu = self.open()
        _type = hdu.data.type()
        self.close()
        del hdu
        return _type
        
    def open(self):
        """ Opens the file for subsequent access. """

        if self.handle == None:
            self.handle = pyfits.open(self.fname,mode='readonly')

        if self.extn:
            if len(self.extn) == 1:
                hdu = self.handle[self.extn]
            else:
                hdu = self.handle[self.extn[0],self.extn[1]]        
        else:
            hdu = self.handle[0]

        return hdu
    

    def close(self):
        """ Closes file handle for this FITS object."""
        if self.handle != None:
            self.handle.close()
        self.handle = None
                            
    def __getslice__(self,i,j):
        """ Returns a PyFITS section for the rows specified. """
        # All I/O must be done here, starting with open
        hdu = self.open()        
        _data = hdu.section[i:j,:]
        self.close()
        del hdu
        
        return _data
        
    def __getattribute__(self,name):
        if name == 'data':
            return self._data()
        elif name == 'shape':
            return self._shape()
        else:
            return object.__getattribute__(self,name)


def parseFilename(filename):
    """
        Parse out filename from any specified extensions.
        Returns rootname and string version of extension name.

        Modified from 'pydrizzle.fileutil' to allow this
        module to be independent of PyDrizzle/MultiDrizzle.

    """
    # Parse out any extension specified in filename
    _indx = filename.find('[')
    if _indx > 0:
        # Read extension name provided
        _fname = filename[:_indx]
        extn = filename[_indx+1:-1]

        # An extension was provided, so parse it out...
        if repr(extn).find(',') > 1:
            _extns = extn.split(',')
            # Two values given for extension:
            #    for example, 'sci,1' or 'dq,1'
            _extn = [_extns[0],int(_extns[1])]
        elif repr(extn).find('/') > 1:
            # We are working with GEIS group syntax
            _indx = str(extn[:extn.find('/')])
            _extn = [int(_indx)]
        elif type(extn) == types.StringType:
            # Only one extension value specified...
            if extn.isdigit():
                # We only have an extension number specified as a string...
                _nextn = [int(extn)]
            else:
                # We only have EXTNAME specified...
                _nextn = extn
            _extn = [_nextn]
        else:
            # Only integer extension number given, or default of 0 is used.
            _extn = [int(extn)]
        
    else:
        _fname = filename
        _extn = None
    return _fname,_extn

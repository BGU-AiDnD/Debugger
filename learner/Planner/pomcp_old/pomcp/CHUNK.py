__author__ = 'amir'

Size = 256

class CHUNK(object):
    def __init__(self,objectType):
        self.Objects=[objectType() for o in range(Size)]


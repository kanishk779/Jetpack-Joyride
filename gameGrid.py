import numpy as np

class LargeGrid:
    
    def __init__(self,externalFile):
        self.__externalFile = externalFile
        self.currentRightColumn = configs.GridWidth


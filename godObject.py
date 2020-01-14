from colorama import Fore, Back, Style
import numpy as np
class Location:
    
    def __init__(self,x_len=0,y_len=0):
        # These coordinates are of the lower left corner
        self.__x_loc = 0
        self.__y_loc = 0
        self.__x_length = x_len
        self.__y_length = y_len
        
    def setLocation(self,x_loc,y_loc):
        self.__x_loc = x_loc
        self.__y_loc = y_loc
    
    def getLocation(self):
        return self.__x_loc,self.__y_loc



class GodObject:
    
    def __init__(self,identifier, obj_location=None):
        self.obj_location = obj_location
        self.__identifier = identifier


    def setIdentifier(identifier):
        self.__identifier = identifier

    def getIdentifier():
        return self.__identifier
    

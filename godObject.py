from colorama import Fore, Back, Style
import numpy as np
class location:
    
    def __init__(self,x_len=0,y_len=0,x_loc=0,y_loc=0):
        self.__x_loc = x_loc
        self.__y_loc = y_loc
        self.__x_length = x_len
        self.__y_length = y_len



class GodObject:
    
    def __init__(self,identifier, obj_location=None):
        self.obj_location = obj_location
        self.__identifier = identifier


    def setIdentifier(identifier):
        self.__identifier = identifier

    def getIdentifier():
        return self.__identifier
    

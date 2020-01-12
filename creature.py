import numpy as np
from godObject import *
'''
Class which describes all the persons in the game.
'''
class Person(GodObject):
    # strength means lives for Mandalorian
    def __init__(self, strength,identifier):
        super().__init__(identifier)
        self.__strength = strength

    def getStrength(self):
        return self.__strength

    def setStrength(self, strength):
        self.__strength = strength

'''
Hero of the game
'''
class Mandalorian(Person):

    def __init__(self, shield_present=False, shield_active=False):
        super().__init__(configs.MandaInitialLives, configs.MandaId)
        self.shield_present = shield_present
        self.shield_active = shield_active

    def fireBullet(self):
        pass

    def moveForward(self):
        pass

    def moveBackward(self):
        pass

    def jump(self):
        pass
    
    def move(self, keyPressed):
        pass
'''
Boss enemy of the game
'''
class Viserion(Person):

    def __init__(self):
        super().__init__(configs.ViserionInitialStrength, configs.ViserionId)

    def fireIceBalls(self):
        pass



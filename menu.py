'''
Keeps the data of the game
'''
class GameData:

    def __init__(self):
        self.lives = configs.MandaInitialLives
        self.score = 0
        self.time_remaining = configs.gameDuration
        # keeps account of how much time has been passed
        self.time_past = 0

'''
Keeps the data of the game
'''
class GameData:

    def __init__(self):
        self.lives = configs.MandaInitialLives
        self.score = 0
        self.time_remaining = configs.gameDuration
        self.time_past = 0

import sys
import subprocess as sp
import select
import termios
import tty


def clear():
    '''
    function to clear the terminal screen
    '''
    sp.call('clear', shell=True)


def keypress(keyin):
    '''
    Identifies which key was pressed
    '''

    if keyin in ('B', 'b', 'D', 'd', 'A', 'a', 'W', 'w', ' ', 'q', 'v', 'V'):
        return keyin
    else:
        return None


class NonBlockingInput:
    '''
    class to deal with non-blocking input
    '''
    def __init__(self):
        '''
        Initializes the object to be used for non-blocking input.
         - Saves original state at time of function call
         - Conversion to new mode has to be manual
        '''
        self.old_settings = termios.tcgetattr(sys.stdin)

    @classmethod
    def nonBlockingTerm(cls):
        '''
        Sets up the terminal for non-blocking input
        '''
        tty.setcbreak(sys.stdin.fileno())

    def originalTerm(self):
        '''
        Sets terminal back to original state
        '''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)

    @classmethod
    def keyboardHit(cls):
        '''
        returns True if keypress has occured
        '''
        return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

    @classmethod
    def getChar(cls):
        '''
        returns input character
        '''
        return sys.stdin.read(1)

    @classmethod
    def flush(cls):
        '''
        clears input buffer
        '''
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)

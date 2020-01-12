from colorama import Fore, Back, Style
from screen import Screen

print(Style.RESET_ALL)
if __name__ == "__main__":
    my_screen = Screen(10,10,2)
    my_screen.generate()


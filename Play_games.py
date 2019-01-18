#from photo_touch import *
#from photo_rocket import *
#import os
#print os.path.abspath("photo_touch.py")

import runpy

def choose_game():
    print('Do you want to play photo touch or photo rocket?')
    game_choice = input()

    if 'touch' in game_choice:
        print('touch accepted')
        runpy.run_path('photo_touch.py')
        #run(Phototouch())
    
    elif 'rocket' in game_choice:
        print('rocket accepted')
        runpy.run_path('photo_rocket.py')
        #run(Photorocket())

    else:
        print('last error')
        choose_game()
        
choose_game()


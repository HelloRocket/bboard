import ui
import runpy
import time

def choose_game():
    '''Prompts player to choose and start a game with boards.'''
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
        
def button_tapped(sender):
    #'@type sender: ui.Button'
    
    t = sender.title
    
    button = sender.superview['button1']
    button2 = sender.superview['button2']
    
    if t == 'Photo Touch':
        runpy.run_path('photo_touch.py')
        
    
    if t == 'Photo Rocket':
        runpy.run_path('photo_rocket.py')
    
    
v = ui.load_view()
v.present('sheet')
#choose_game()


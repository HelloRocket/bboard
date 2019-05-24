import ui
from plistlib import *
from random import randrange
import speech
import sound
from time import sleep

'''fileName is the plist to import'''
fileName = 'Bitsboard.plist'
#fileName = 'LPDB00/Bitsboard.plist'

class Phototouch (ui.View):
    def __init__(self):    
        self.name = 'Photo Touch'                                    
        self.background_color = 'lightblue'
        self.setup()

    def did_load(self):
        pass
        
    def draw(self):
        
        pass
    
    def setup(self):
        '''This extracts the items from playlist'''
        with open(fileName, 'rb') as fp:
            pl = load(fp)       
        self.originlist = pl['Bits']
        self.buttons = []
        self.playTouch(self.originlist)

    def button_tapped(self, sender):
        '''Checks if sender is the winning bit'''
        if str(sender.name) == self.winTex:
            sender.image = ui.Image.named('emj:Checkmark_3').with_rendering_mode(ui.RENDERING_MODE_ORIGINAL)
            sound.play_effect('game:Ding_3', 0.2)    
            def animation():
                button.alpha = 0.0 # fade out
        
            for button in self.buttons:            
                ui.animate(animation, duration=1.5)
            ui.delay(self.restart, 2)
                                            
        else:
            sender.image = ui.Image.named('emj:Cross_Mark').with_rendering_mode(ui.RENDERING_MODE_ORIGINAL)
            sound.play_effect('game:Error', 0.2)            

                        
    def playTouch(self, importList):    
        '''Items selection and setup'''
        bitlist = importList.copy()
        showlist = []
        for i in range(3):
            
            a=i+1
            bnum = len(bitlist)
                     
            targetBit = bitlist[randrange(bnum)]
            bitname = str(targetBit)
            #print('bit '+bitname)
            targetPic = str(targetBit)+'.jpg'
            picname = targetPic.lower()
            print('pic '+picname)
            self.button = ui.Button(bitname)                   # [4]
            (screenX, screenY) = ui.get_screen_size()   
            self.button.frame = (0, 0, 200, 200)
            self.button.name = bitname
            self.button.background_image=ui.Image.named(picname).with_rendering_mode(ui.RENDERING_MODE_ORIGINAL)
            self.button.border_width =4
            self.button.border_color ='white'
            self.button.corner_radius = 15
            self.button.center = ((screenX/4)* (i+1), (screenY/4) * 3)
            #button.flex = 'TR'                                               
            self.add_subview(self.button)  
               
            self.button.action = self.button_tapped 
            self.buttons.append(self.button)
            
            bitlist.remove(targetBit)
            showlist.append(targetBit)
            
        snum = len(showlist)
        #print(snum, showlist)    
        winbit = showlist[randrange(snum)]
        sound.play_effect(winbit.lower()+'.mp3')
        sound.play_effect(winbit.lower()+'.caf')
        self.winTex = str(winbit)  
        
    def restart(self):
        '''This removes all sibviews and then restarts game'''
        for button in self.buttons:
            
            self.remove_subview(button)
        self.buttons.clear()
        #print(self.buttons, self.subviews, 'done')
        self.playTouch(self.originlist)
    

v = Phototouch()                                                
v.present('Landscape Large')                                 


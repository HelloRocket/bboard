from scene import *
from sys import argv
from plistlib import *
from random import randrange
import speech
import sound
import time
from math import pi
A = Action


#script, fileName = argv
'''fileName is the plist to import'''
fileName = 'Bitsboard.plist'

class Bit (SpriteNode):
    '''This is the image object called Bit with placeholder snowflake image'''
    def __init__(self, **kwargs):
        
        SpriteNode.__init__(self, 'emj:Snowflake', **kwargs)
        
class Band (ShapeNode):
    def __init__(self, **kwargs):        
        band_rect = ui.Path.rect (0, 0, 200, 300)                
        super().__init__(band_rect, stroke_color='clear', shadow=None, **kwargs)   
        
class Message (LabelNode):
    def __init__(self, **kwargs):        
        
        super().__init__( **kwargs)   


class Photorocket (Scene):
    '''This is the main class as a scene where events take place'''
    def setup(self):
        '''This is the starting point'''
        
        self.background_color = (.93, .93, .93)
        self.items = []
        with open(fileName, 'rb') as fp:
            pl = load(fp)
            
        self.originlist = pl['Bits']
        self.bitlist = self.originlist.copy()
        
        self.showlist = []
        self.orient = 'portrait'
        self.game_touch = True
        self.playRocket()
        
        self.red_band = Band(fill_color= 'red', position =(self.size.w/2, self.size.h - self.size.h/4), parent = self)
        self.red_band.size = self.size.w, self.size.h/3
        self.red_band.z_position = -1.0
        self.red_band.anchor_point = 0.5, 0.25
        
        self.blue_band = Band(fill_color= (.33, .74, 1.0), position =(self.size.w/2, 0),  parent = self)
        self.blue_band.size = self.size.w, self.size.h/3
        self.blue_band.z_position = -1.0
        self.blue_band.anchor_point = 0.5, 0.0
        
        self.myMessage = Message(text='Game On', font=('Helvetica', 80), position = self.size/2, color = 'black', parent=self)
        
        self.redMessage = Message(text='Go Red!', font=('Helvetica', 40), position = (self.size.w/2,(self.size.h/5)*3), color = 'red', parent=self)
        self.redMessage.rotation = pi
        self.red_point = 0
        
        self.blueMessage = Message(text='Go Blue!', font=('Helvetica', 40), position = (self.size.w/2,(self.size.h/5)*2), color = 'blue',  parent=self)
        self.blue_point = 0

    def restart(self):
        '''Checks to reset after each touch'''
        
        if self.red_point > 9:
            self.endgame('red')
               
        elif self.blue_point > 9:
            self.endgame('blue')
                        
        else:
            self.bitlist = self.originlist.copy()
            self.showlist = []        
            self.game_touch = True
            self.playRocket()   
    
    def check_item_collisions(self, choiceX, choiceY):
        '''Checks what items are touched if any'''
        player_hitbox = Rect(choiceX, choiceY, 1, 1)
        for item in list(self.items):
            if item.frame.intersects(player_hitbox):
                if isinstance(item, Bit):                  
                    self.changeImage(item, choiceY)
                
                
    def changeImage(self, bit, choiceY):
        '''On correct choice'''
        if bit.name == self.winTex:          
            bit.texture = Texture('emj:Checkmark_3')
            sound.play_effect('game:Ding_3', 0.2)
            
            if choiceY < self.size.h/3:
                self.center_message('blue wins', 0)
                self.blue_point+=1
                self.blueMessage.text = str(self.blue_point)
                                
            elif choiceY > self.size.h - self.size.h/4:
                self.center_message('red wins', pi)
                self.red_point+=1
                self.redMessage.text = str(self.red_point)
                                
            else:
                self.center_message('touch the screen!')
            
            bit.run_action(A.sequence(A.wait(2), A.call(self.restart)))
            #self.restart()
            
        else:
            '''On mistaken choice'''
            bit.texture = Texture('emj:Cross_Mark')
            sound.play_effect('game:Error', 0.2)
            self.game_touch = True
   
    def center_message(self, message, orientation):
        self.myMessage.text = message
        self.myMessage.rotation = (orientation)
    
    def check_potrait(self):
        '''Checks if changes from portrait. Clears screen on landscape'''
        xSize, ySize = self.size
        #print(xSize)
        if xSize != 768.00:
            for item in list(self.items):
                '''This remove previous items from the screen'''
                item.remove_from_parent()
                self.items.remove(item)
            
                               
        elif xSize == 768.00:
            self.restart()
        else:
            pass
    
    def did_change_size(self):
        xSize, ySize = self.size
        #print(xSize)
        #print("Hello")
        self.check_potrait()                                                         
                                                                                                                                                                                 
                                                                                                                                                     
    def playRocket(self):
        '''Items selection and setup'''
        for item in list(self.items):
            '''This remove previous items from the screen'''
            item.remove_from_parent()
            self.items.remove(item)
            
                
        for i in range(3):
            '''Lays out the bits'''
            
            a=i*2+1
            bnum = len(self.bitlist)
            targetBit = self.bitlist[randrange(bnum)]
            targetPic = (str(targetBit)+'.jpg').lower()
            
            
            bit = Bit(parent=self)            
            self.items.append(bit)                         
            bit.name = str(targetBit)
            bit.texture = Texture(targetPic)
            bit.size = (200,200)
            bit.position = self.size.x/6*a, self.size.y/6  
            
            bit = Bit(parent=self)            
            self.items.append(bit)                         
            bit.name = str(targetBit)
            bit.texture = Texture(targetPic)
            bit.size = (200,200)
            bit.position = self.size.x - self.size.x/6*a, self.size.y - self.size.y/6  
            bit.rotation = (pi)
                                    
            self.bitlist.remove(targetBit)
            self.showlist.append(targetBit)
            
        self.winbit()
            
    def winbit(self):
        '''Chooses winning bit and play the corresponding sound file.'''
        snum = len(self.showlist)     
        winbit = self.showlist[randrange(snum)]
        #print(winbit)
        #speech.say(winbit, 'en-GB')
        sound.play_effect(winbit.lower()+'.mp3')
        sound.play_effect(winbit.lower()+'.caf')
        self.winTex = str(winbit)
        
    
    def update(self):
        pass
    
    def touch_began(self, touch):
        '''Input from device screen'''
            
        if self.game_touch == True:
            self.game_touch = False
            choiceX = touch.location.x
            choiceY = touch.location.y        
            self.check_item_collisions(choiceX, choiceY)
            
        else:
            pass
      
    def touch_moved(self, touch):
        pass
    
    def touch_ended(self, touch):
        pass
        
    def endgame(self, color):
        self.blue_band.remove_from_parent()
        self.blueMessage.remove_from_parent()
        self.red_band.remove_from_parent()
        self.redMessage.remove_from_parent()
        self.background_color = color
        self.myMessage.color = 'pink'
        self.myMessage.run_action(A.sequence(A.wait(1), A.rotate_by(pi*2, 1), A.fade_to(0,2)))
        

#if __name__ == '__main__':
run(Photorocket(), show_fps=False)

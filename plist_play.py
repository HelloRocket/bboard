from scene import *
from sys import argv
from plistlib import *
from random import randrange
import speech
import sound
A = Action


script, fileName = argv
'''fileName is the plist to import'''


class Bit (SpriteNode):
    '''This is the image object called Bit with placeholder snowflake image'''
    def __init__(self, **kwargs):
        
        SpriteNode.__init__(self, 'emj:Snowflake', **kwargs)


class Phototouch (Scene):
    '''This is the main class as a scene where events take place'''
    def setup(self):
        '''This is the starting point'''
        self.background_color = '#78c1f0'
        self.items = []
        with open(fileName, 'rb') as fp:
            pl = load(fp)
            
        self.originlist = pl['Bits']
        self.bitlist = self.originlist.copy()
        
        self.showlist = []
        
        self.playTouch()

    def restart(self):
        '''Resets after each touch'''
        
        self.bitlist = self.originlist.copy()
        self.showlist = []        
        self.playTouch()   
    
    def check_item_collisions(self, choiceX, choiceY):
        '''Checks what items are touched if any'''
        player_hitbox = Rect(choiceX, choiceY, 1, 1)
        for item in list(self.items):
            if item.frame.intersects(player_hitbox):
                if isinstance(item, Bit):                  
                    self.changeImage(item)
                
                
    def changeImage(self, bit):
        '''On correct choice'''
        if bit.name == self.winTex:          
            bit.texture = Texture('emj:Checkmark_3')
            sound.play_effect('game:Ding_3', 0.2)
            bit.run_action(A.sequence(A.wait(2), A.call(self.restart)))
            #self.restart()
            
        else:
            '''On mistaken choice'''
            bit.texture = Texture('emj:Cross_Mark')
            sound.play_effect('game:Error', 0.2)
                                                               
                                                                                                                                                     
    def playTouch(self):
        '''Items selection and setup'''
        for item in list(self.items):
            '''This remove previous items from the screen'''
            item.remove_from_parent()
            self.items.remove(item)
        
        for i in range(3):
            
            a=i+1
            bnum = len(self.bitlist)
            bit = Bit(parent=self)            
            self.items.append(bit)
            bit.position = self.size.x/4*a, self.size.y/2  
            bit.size = (200,200)
             
            targetBit = self.bitlist[randrange(bnum)]
            bit.name = str(targetBit)
            targetPic = str(targetBit)+'.jpg'
            targetPic = targetPic.lower()
            bit.texture = Texture(targetPic)
            bit.size = (200,200)
            self.bitlist.remove(targetBit)
            self.showlist.append(targetBit)
            snum = len(self.showlist)
            
        winbit = self.showlist[randrange(snum)]
        speech.say(winbit)
        self.winTex = str(winbit)
        
    
    def did_change_size(self):
        pass
    
    def update(self):
        pass
    
    def touch_began(self, touch):
        '''Input from device screen'''
        choiceX = touch.location.x
        choiceY = touch.location.y        
        self.check_item_collisions(choiceX, choiceY)
      
    def touch_moved(self, touch):
        pass
    
    def touch_ended(self, touch):
        pass

if __name__ == '__main__':
    run(Phototouch(), show_fps=False)

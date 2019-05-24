import ui
import os
from plistlib import *
from random import randrange
import speech
import sound
from time import sleep
from math import pi

'''fileName is the plist to import'''
fileName = 'Bitsboard.plist'

class Photorocket (ui.View):
    def __init__(self):    
        self.name = 'Photorocket'                                    
        self.background_color = 'lightblue'

        self.setup()

    def did_load(self):
        pass
        
    def draw(self):
        
        path = ui.Path.rect(0, (self.height-self.height/3), self.width, self.height/3)
        ui.set_color('red')
        path.fill()
        
        path = ui.Path.rect(0, 0, self.width, self.height/3)
        ui.set_color('#2b74ff')
        path.fill()
    
    def setup(self):
        '''This extracts the items from playlist'''
        with open(fileName, 'rb') as fp:
            pl = load(fp)       
        self.originlist = pl['Bits']
        self.red_points = ui.Label()
        self.red_points.text = 'Go Red'
        self.red_points.font = ('Helvetica-bold', 60)
        self.red_points.text_color = 'red'
        self.add_subview(self.red_points)
        self.blue_points = ui.Label()
        self.blue_points.text = 'Go Blue'
        self.blue_points.font = ('Helvetica-bold', 60)
        self.blue_points.text_color = '#2b74ff'
        self.add_subview(self.blue_points)
        self.buttons = []
        self.buttons2 = []
        self.redPoint = 0
        self.bluePoint = 0
        self.multitouch_enabled=False
        self.end_game = False
        self.playTouch(self.originlist) 
        
        
        
    def button_tapped(self, sender):
        '''Checks if sender is the winning bit'''
        
        if str(sender.name) == self.winTex:
            self.touch_enabled=False
            self.count_points(sender.y)
            sender.image = ui.Image.named('emj:Checkmark_3').with_rendering_mode(ui.RENDERING_MODE_ORIGINAL)
            sound.play_effect('game:Ding_3', 0.2)    
            
            if self.winTap == False:
                self.winTap = True
                def animation():
                    button.alpha = 0.0 # fade out
        
                for button in self.buttons:            
                    ui.animate(animation, duration=1.5)
                for button in self.buttons2:            
                    ui.animate(animation, duration=1.5)
                ui.delay(self.restart, 2)
                                            
        else:
            sender.image = ui.Image.named('emj:Cross_Mark').with_rendering_mode(ui.RENDERING_MODE_ORIGINAL)
            sound.play_effect('game:Error', 0.2)    
            
    def count_points(self, Ypos):
        if Ypos>384:
            self.redPoint+=1
            if self.redPoint==1:
                self.red_points.text = (f'Red has 1 point!')
                
            elif self.redPoint>4:
                self.red_points.text = ('Red Wins!')
                self.end_game = True
                
            elif self.redPoint>1:
                self.red_points.text = (f'Red has {self.redPoint} points!')
            
            else:
                self.red_points.text = ('Something went wrong.')
                
        else:
            self.bluePoint+=1
            if self.bluePoint==1:
                self.blue_points.text = (f'Blue has 1 point!')
                
            elif self.bluePoint>4:
                self.blue_points.text = ('Blue Wins!')
                self.end_game = True
                
            elif self.bluePoint>1:
                self.blue_points.text = (f'Blue has {self.bluePoint} points!')
            
            else:
                self.blue_points.text = ('Something went wrong.')
            
                               
    def playTouch(self, importList):    
        '''Items selection and setup'''
        bitlist = importList.copy()
        showlist = []
        self.winTap = False
        self.touch_enabled=True
        
        for i in range(3):
            
            a=i+1
            bnum = len(bitlist)                     
            targetBit = bitlist[randrange(bnum)]
            bitname = str(targetBit)
            targetPic = str(targetBit)+'.jpg'
            picname =  targetPic.lower()
            

            self.button = ui.Button(bitname)                   
            self.button.name = bitname
            self.button.background_image=ui.Image.named(picname).with_rendering_mode(ui.RENDERING_MODE_ORIGINAL)
            self.button.border_width =4
            self.button.border_color ='white'
            self.button.corner_radius = 15
            #button.flex = 'TR'                                               
            self.button.action = self.button_tapped 
            self.add_subview(self.button)  
            
            self.buttons.append(self.button)
            self.button = ui.Button(bitname)
            self.button.name = bitname
            self.button.background_image=ui.Image.named(picname).with_rendering_mode(ui.RENDERING_MODE_ORIGINAL)
            self.button.border_width =4
            self.button.border_color ='white'
            self.button.corner_radius = 15
            self.button.action = self.button_tapped 
            self.add_subview(self.button)  
            self.buttons2.append(self.button)
                
            bitlist.remove(targetBit)
            showlist.append(targetBit)            
            
        snum = len(showlist)
        #print(snum, showlist)    
        winbit = showlist[randrange(snum)]
        sound.play_effect(winbit.lower()+'.mp3')
        sound.play_effect(winbit.lower()+'.caf')
        self.winTex = str(winbit)  
        
    def layout(self):
        (screenX, screenY) = ui.get_screen_size()   
        i=0
        
        for button in self.buttons:
            i+=1
            button.bounds = (0, 0, screenX/5, screenX/5)
            button.center = ((screenX/4)* (i), (screenY/4) * 3.05)
            
        
        self.red_points.frame = (0, 0, 600, 100)
        self.red_points.center = screenX/2, ((screenY/4) * 2.3)
        self.red_points.alignment=1
        
        
        i=0    
        for button in self.buttons2:
            i+=1
            button.bounds = (0, 0, screenX/5, screenX/5)
            button.center = ((screenX/4)* (i), (screenY/4) * .6)
            def animation():
                button.transform=ui.Transform.rotation(pi)
            ui.animate(animation, duration = 0.0)
        
        self.blue_points.frame = (0, 0, 600, 100)
        self.blue_points.center = screenX/2, ((screenY/4) * 1.4)
        def label_flip():
            self.blue_points.transform=ui.Transform.rotation(pi)
        ui.animate(label_flip, duration = 0.0)
        self.blue_points.alignment=1
        
        

    
    def restart(self):
        '''This removes all sibviews and then restarts game'''
        for button in self.buttons:            
            self.remove_subview(button)
        self.buttons.clear()
        
        for button in self.buttons2:            
            self.remove_subview(button)
        self.buttons2.clear()
        
        if self.end_game == False:
            self.playTouch(self.originlist)
    
    

v = Photorocket()                             
v.present('Landscape Large')        


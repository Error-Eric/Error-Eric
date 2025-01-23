"确保你在使用英文输入法!!!"

'author: zhouchanghuieric@qq.com'

import pygame as pyg
#import time
import random
from openpyxl import load_workbook

# Initialize the names
sheet = load_workbook(filename= './0.xlsx')['Sheet1']


# Initialize the window
pyg.init()
window = pyg.display.set_mode( size= (720, 480))
pyg.display.set_caption('Fun mini-game')
bgcol = (255,114//2,118//2)
window.fill(color= bgcol) # light red 

# time.sleep(2)
image1 = pyg.image.load('./bg.png')
image1 = pyg.transform.scale( image1, (720, 480) )
window.blit(source= image1, dest = (0, 0))
pyg.display.flip() 

# Initialize the font
#font = pyg.font.SysFont('SimHei', 60)
fonts = [ pyg.font.SysFont('SimHei', 60),pyg.font.SysFont('SimHei', 36) ]# 黑体

imgcood = (720 // 4, 480 // 4)
on_going, rotating = True, False
while on_going:
    for event in pyg.event.get():
        print(event)
        if event.type == pyg.QUIT: on_going = False ; break; 
        elif event.type == pyg.KEYDOWN:
            rotating = not rotating
            print('keydown event detected')

    if rotating : 
        window.blit(source= image1, dest = (0, 0)) # remove all except for the background
        ys = [pyg.display.Info().current_h // 2 + disp for disp in [-180, -90, 0, 90, 180]]
        used = set()
        for id, com in enumerate("ABCDE"):
            row = list(sheet[com])
            while row[-1].value == None or len(row[-1].value) <= 1: row.pop(-1)
            conc = row[int(random.random() * len(row))].value
            text = fonts[0 if len(conc)<12 else 1].render(conc, True, (0, 0, 0))
            textrect = text.get_rect()
            textrect.centerx = pyg.display.Info().current_w // 2
            textrect.centery = ys[id]
            window.blit(source = text, dest = textrect)
    
    pyg.display.update()
    #print('test')
    pyg.time.Clock().tick(20)
pyg.quit()
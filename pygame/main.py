"确保你在使用英文输入法!!!"

'author: zhouchanghuieric@qq.com'

import pygame as pyg
#import time
import random
from openpyxl import load_workbook

# Initialize the names
sheet = load_workbook(filename= './Book1.xlsx')['Sheet1']
names = [cell.value for cell in sheet['A']]
print(names)


# Initialize the window
pyg.init()
window = pyg.display.set_mode( size= (720, 480))
pyg.display.set_caption('抽奖')
bgcol = (255,114//2,118//2)
window.fill(color= bgcol) # light red 

# time.sleep(2)
image1 = pyg.image.load('./bg.png')
image1 = pyg.transform.scale( image1, (720, 480) )
window.blit(source= image1, dest = (0, 0))
pyg.display.flip() 

# Initialize the font
fonts = [ pyg.font.SysFont('SimHei', 96),pyg.font.SysFont('SimHei', 72) ]# 黑体

imgcood = (720 // 4, 480 // 4)
on_going, rotating, number = True, False, 1
while on_going:
    for event in pyg.event.get():
        print(event)
        if event.type == pyg.QUIT: on_going = False ; break; 
        elif event.type == pyg.KEYDOWN:
            if event.key == pyg.K_1:
                number = 1
            elif event.key == pyg.K_5:
                number = 5
            else :
                rotating = not rotating
                print('keydown event detected')

    if rotating : 
        window.blit(source= image1, dest = (0, 0)) # remove all except for the background
        ys = [pyg.display.Info().current_h // 2 + disp for disp in [0, -90, -180, 90, 180]]
        used = set()
        for imgid in range(number):
            i = int(random.random() * len(names)) 
            while i in used: 
                i = int(random.random() * len(names))
            used.add(i)
            text = fonts[0 if number == 1 else 1].render(names[i], True, (255, 215, 0))
            textrect = text.get_rect()
            textrect.centerx = pyg.display.Info().current_w // 2
            textrect.centery = ys[imgid]
            window.blit(source = text, dest = textrect)
    
    pyg.display.update()
    #print('test')
    pyg.time.Clock().tick(20)
pyg.quit()
import pygame, random
import cv2
from PIL import Image
import numpy as np
from os import listdir

mypath="/part/data/dataset/data.v22/bitmask/"
OUT_DIR = "/part/data/dataset/data.v22/out/"
from os.path import isfile, join
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
print(onlyfiles)

fileno=0
file=onlyfiles[fileno]
filename = join(mypath,file)
img = pygame.image.load(filename)
screen = pygame.display.set_mode((800,600))

draw_on = False
last_pos = (0, 0)
radius = 20

def roundline(srf, color, start, end, radius=1):

    if start[0]>224+radius and start[0]<448-radius:
        if end[0]>224+radius and end[0]<448-radius:
            dx = end[0]-start[0]
            dy = end[1]-start[1]
            distance = max(abs(dx), abs(dy))
            for i in range(distance):
                x = int( start[0]+float(i)/distance*dx)
                y = int( start[1]+float(i)/distance*dy)
                pygame.draw.circle(srf, color, (x, y), radius)

try:

    w=672
    h=224
    screen = pygame.display.set_mode((w, h))
    screen.blit(img,(0,0))
    while True:
        imgdata = pygame.surfarray.array3d(img)
        orig = imgdata[0:224,:,:]
        mask = imgdata[224:448,:,:]
        result =orig.copy()
        result[np.where(mask<10)]=0

        imgdata[448:,:,:]=result
        img = pygame.surfarray.make_surface(imgdata)

        screen.blit(img,(0,0))
        e = pygame.event.wait()
        if e.type == pygame.QUIT:
            raise StopIteration
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button==1:
                color = 0
            else:
                color = (255,255,255)
            if e.pos[0]>224+int(radius) and e.pos[0]<448-int(radius):

                pygame.draw.circle(img, color, e.pos, radius)
            draw_on = True
        if e.type == pygame.MOUSEBUTTONUP:
            draw_on = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_d:
                img1=pygame.transform.rotate(img,270)
                img2=pygame.transform.flip(img1,True,False)
                imgdata = pygame.surfarray.array3d(img2)

                fileout=join(OUT_DIR,file)
                print("SAVE :"+fileout)
                cv2.imwrite(fileout,cv2.cvtColor(imgdata, cv2.COLOR_BGR2RGB))

                fileno=fileno+1
                if fileno>len(onlyfiles)-1:
                    fileno=0
                file=onlyfiles[fileno]
                filename = join(mypath,file)
                img = pygame.image.load(filename)

            if e.key == pygame.K_a:
                img1=pygame.transform.rotate(img,270)
                img2=pygame.transform.flip(img1,True,False)
                imgdata = pygame.surfarray.array3d(img2)
                
                fileout=join(OUT_DIR,file)
                print("SAVE :"+fileout)
                cv2.imwrite(fileout,cv2.cvtColor(imgdata, cv2.COLOR_BGR2RGB))

                fileno=fileno-1
                if fileno<0:
                    fileno=len(onlyfiles)-1
                file=onlyfiles[fileno]
                filename = join(mypath,file)
                img = pygame.image.load(filename)


        if e.type == pygame.MOUSEMOTION:
            if draw_on:
                if e.pos[0]>224+int(radius) and e.pos[0]<448-int(radius):
                    pygame.draw.circle(img, color, e.pos, radius)
                    roundline(img, color, e.pos, last_pos,  radius)
            last_pos = e.pos
        pygame.display.flip()

except StopIteration:
    pass

pygame.quit()

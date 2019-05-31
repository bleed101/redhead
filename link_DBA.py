score=0
global n
import sqlite3

from tkinter import *
#from link_DBA import score
con=sqlite3.Connection('Game')
cur=con.cursor()
root=Tk()
root.title('Entry')
root.geometry("760x400+290+167")
fr1=Frame()
img3=PhotoImage(file='C:/Users/nephilim/Desktop/game/thank-you.gif')
Label(root,image=img3).pack()
Label(root,text='Enter your name',font='times 24 bold ',fg='#900C3F').place(x=250,y=200)


name=Entry(root,relief=SUNKEN,bd=6)
name.place(x=300,y=250)

n=name.get()
cur.execute("create table IF NOT EXISTS Highest(NAME varchar(12) NOT NULL ,SCORE number(3))")
def players():

        cur.execute("insert into Highest values(?,?)",(name.get(),score))
        root4=Tk()
        root4.title('Score Board')
        root4.geometry("380x200+490+270")
        Label(root4,text='NAME             SCORE      ').pack()
        Label(root4,text='---------------------+-------------------').pack()
        cur.execute("select * from Highest order by score DESC")
        obj=cur.fetchall()
        con.commit()
        objl=len(obj)
        for i in range(0,objl):
            Label(root4,text=obj[i]).pack()
        #root.destroy()
        root4.mainloop()

def reset():
        cur.execute("delete from Highest")
        con.commit()
        #root.destroy()

Button(root,text='RESET',command=reset,relief=RAISED,bd=5,bg='red').place(x=375,y=300)
Button(root,text='SCORE',command=players,relief=RAISED,bd=5,bg='red').place(x=315,y=300)

import pygame,os
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
win=pygame.display.set_mode((700,400))
pygame.display.set_caption("GAME")

walkRight = [pygame.image.load('sprites/Transparent PNG/right/R1.png'), pygame.image.load('sprites/Transparent PNG/right/R2.png'), pygame.image.load('sprites/Transparent PNG/right/R3.png'), pygame.image.load('sprites/Transparent PNG/right/R4.png'), pygame.image.load('sprites/Transparent PNG/right/R5.png'), pygame.image.load('sprites/Transparent PNG/right/R6.png')]
walkLeft = [pygame.image.load('sprites/Transparent PNG/left/L1.png'), pygame.image.load('sprites/Transparent PNG/left/L2.png'), pygame.image.load('sprites/Transparent PNG/left/L3.png'), pygame.image.load('sprites/Transparent PNG/left/L4.png'), pygame.image.load('sprites/Transparent PNG/left/L5.png'), pygame.image.load('sprites/Transparent PNG/left/L6.png')]
bg=pygame.image.load('sprites/bg.png')
still=[pygame.image.load('sprites/Transparent PNG/idle/frame-1.png'),pygame.image.load('sprites/Transparent PNG/idle/frame-2.png'),pygame.image.load('sprites/Transparent PNG/idle/frame-1.png'),pygame.image.load('sprites/Transparent PNG/idle/frame-2.png'),pygame.image.load('sprites/Transparent PNG/idle/frame-1.png'),pygame.image.load('sprites/Transparent PNG/idle/frame-2.png')]
clock=pygame.time.Clock()

bulletSound=pygame.mixer.Sound("sounds/bullet.wav")
hitSound=pygame.mixer.Sound('sounds/hit.wav')
bs=pygame.mixer.music.load('sounds/Drowning.wav')
pygame.mixer.music.play(-1)



class player(object):
    def __init__(self,x,y,w,h):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.vel=7
        self.isjump=False
        self.jump=10
        self.left=False
        self.right=False
        self.walkcount=0
        self.standing=True
        self.hitbox=(self.x+.8,self.y+3.7,40,64)

    def draw(self,win):
        if self.walkcount +1>18:
            self.walkcount=0

        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkcount//5],(self.x,self.y))
                self.walkcount+=1
            elif self.right:
                win.blit(walkRight[self.walkcount//5],(self.x,self.y))
                self.walkcount+=1
        else:
            if self.right:
                win.blit(walkRight[0],(self.x,self.y))
            else:
                win.blit(walkLeft[0],(self.x,self.y))
        self.hitbox=(self.x+.8,self.y-1,40,64)
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)

    def hit(self):
        self.isjump=False
        self.jump=10
        self.x=655
        self.y=214
        self.walfcount = 0
        font1=pygame.font.SysFont('comicsansms',100)
        text=font1.render('-5',1,(255,0,0))
        win.blit(text,(350-(text.get_width()/2),350-(text.get_height()/2)))
        pygame.display.update()
        i=0
        while i<100:
            pygame.time.delay(10)      #10 is in sec always
            i +=1
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    i=301
                    pygame.quit()

class enemy(object):
    walkRight=[pygame.image.load("Enemy_sprites/right/R1.png"),pygame.image.load("Enemy_sprites/right/R2.png"),pygame.image.load("Enemy_sprites/right/R3.png"),pygame.image.load("Enemy_sprites/right/R4.png"),pygame.image.load("Enemy_sprites/right/R5.png"),pygame.image.load("Enemy_sprites/right/R6.png"),pygame.image.load("Enemy_sprites/right/R7.png"),pygame.image.load("Enemy_sprites/right/R8.png")]
    walkLeft=[pygame.image.load("Enemy_sprites/left/L1.png"),pygame.image.load("Enemy_sprites/left/L2.png"),pygame.image.load("Enemy_sprites/left/L3.png"),pygame.image.load("Enemy_sprites/left/L4.png"),pygame.image.load("Enemy_sprites/left/L5.png"),pygame.image.load("Enemy_sprites/left/L6.png"),pygame.image.load("Enemy_sprites/left/L7.png"),pygame.image.load("Enemy_sprites/left/L8.png"),]

    def __init__(self,x,y,w,h,end):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.end=end
        self.path=[self.x,self.end]
        self.walkcount=0
        self.vel=3
        self.hitbox=(self.x+20,self.y,88,114)
        self.health=20
        self.visible=True

    def draw(self,win):
        self.move()
        if self.visible:
            if self.walkcount+1>=40:
                self.walkcount=0

            if self.vel>0:
                win.blit(self.walkRight[self.walkcount//5],(self.x,self.y))
                self.walkcount +=1
            else:
                win.blit(self.walkLeft[self.walkcount//5],(self.x,self.y))
                self.walkcount +=1
            pygame.draw.rect(win,(128,0,0),(self.hitbox[0],self.hitbox[1]-20,80,10))
            pygame.draw.rect(win,(124,252,0),(self.hitbox[0],self.hitbox[1]-20,80-(4*(20-self.health)),10))
            self.hitbox=(self.x+.7,self.y-1.4,88,114)
           # pygame.draw.rect(win,(255,0,0),self.hitbox,2)


    def move(self):
        if self.vel>0:
            if self.x+self.vel<self.path[1]:
                self.x +=self.vel
            else:
                self.vel=self.vel*-1
                self.walkcount=0
        else:
            if self.x-self.vel>self.path[0]:
                self.x +=self.vel
            else:
                self.vel=self.vel*-1
                self.walkcount=0
    def hit(self):
        if(self.health>0):
            self.health-=1
            '''print ("hit")'''
        else:
            self.visible=False


class bullet1(object):
    def __init__(self,x,y,radius,color,facing):
        self.x=x
        self.y=y
        self.color=color
        self.radius=radius
        self.facing=facing
        self.vel=8*facing

    def draw(self,win):
        pygame.draw.circle(win,self.color,(self.x,self.y),self.radius)


def redrawGameWindow():

    win.blit(bg,(0,0))
    if enm.visible==True:
        text=font.render('SCORE : ' +str(score),1,(0,0,0))
        win.blit(text,(490,5))
    else:
        win1=font.render('Congratulation...!  ',1,(255,20,147))
        win.blit(win1,(250,120))
        win1=font.render('Your score :   '+str(score),1,(0,255,255))
        win.blit(win1,(250,150))
        win1=font.render('Press Q to QUIT',1,(255,20,2))
        win.blit(win1,(250,178))
       #'''win1=font.render('Press A to play again',1,(0,255,127))'''
       #'''win.blit(win1,(220,206))'''
        root.mainloop()

    bleed.draw(win)
    enm.draw(win)
    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update()
#mainloop

font=pygame.font.SysFont("comicsansms",30,True)
bleed=player(347,214,45,64)
enm=enemy(5,169.4,64,64,540)
shoot_correct=1
bullets=[]
run=True
while run:
    clock.tick(30)

    if bleed.hitbox[1]<enm.hitbox[1]+enm.hitbox[3] and bleed.hitbox[1]+bleed.hitbox[3]>enm.hitbox[1]:       #this is for our player to
        if bleed.hitbox[0]+bleed.hitbox[2] >enm.hitbox[0] and bleed.hitbox[0]<enm.hitbox[0]+enm.hitbox[2]:
            if enm.visible:
                bleed.hit()
                score -=5

    if shoot_correct>0:
        shoot_correct+=0.6
    if shoot_correct>3:
        shoot_correct=0

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False

    for bullet in bullets:
        if bullet.y-bullet.radius<enm.hitbox[1]+enm.hitbox[3] and bullet.y+bullet.radius>enm.hitbox[1]:
            if bullet.x+bullet.radius>enm.hitbox[0] and bullet.x-bullet.radius<enm.hitbox[0]+enm.hitbox[2]:
                enm.hit()
                if enm.visible:
                    score+=1
                    bullets.pop(bullets.index(bullet))
                    hitSound.play()


        if bullet.x<700 and bullet.x>0:
            bullet.x +=bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys=pygame.key.get_pressed()

    if keys[pygame.K_s] and shoot_correct==0:
        bulletSound.play()
        if bleed.left:
            facing = -1
        else:
            facing = 1
        if len(bullets)<5:
            bullets.append(bullet1(round(bleed.x+bleed.w//1.4),round(bleed.y+bleed.h//1.4),7,(0,0,0),facing))
        shoot_correct=1
    if keys[pygame.K_q]:
        run=False
        enm.visible=False

    if keys[pygame.K_LEFT] and bleed.x>5:
        bleed.x-=bleed.vel
        bleed.left=True
        bleed.right=False
        bleed.standing=False
    elif keys[pygame.K_RIGHT] and bleed.x<649:
        bleed.x+=bleed.vel
        bleed.left=False
        bleed.right=True
        bleed.standing=False
    else:
        bleed.standing=True
        bleed.walkcount=0

    if not (bleed.isjump):
        if keys[pygame.K_SPACE] :
            bleed.isjump=True
            bleed.walkcount=0
    else:
        if bleed.jump>=-10:
            neg=1
            if bleed.jump<0:
                neg=-1
            bleed.y-=(bleed.jump**2)*0.5*neg
            bleed.jump -=1
        else:
            bleed.isjump=False
            bleed.jump=10
    redrawGameWindow()


pygame.quit()

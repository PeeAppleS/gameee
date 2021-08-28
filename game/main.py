#main.py

import pygame
import math
import random


pygame.init()
WIDTH = 1000
HEIGHT = 800

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Meow vs Covid-19')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

background = pygame.image.load('bg.png')

#################CAT###################
# 1 - player - cat.png

psize = 128

pimg = pygame.image.load('cat.png')
px = 100
py = HEIGHT - psize
pxchange = 0

def Player(x,y):
	screen.blit(pimg,(x,y))




#################ENMY###################
# 2 - enmy - virus.png
esize = 64
eimg = pygame.image.load('virus.png')
ex = 50
ey = 0
eychange = 1
def Enemy(x,y):
	screen.blit(eimg,(x,y))

#################MUTI ENMY###################

exlist = [] #ตำเเหน่งvirus
eylist = []
ey_change_list = [] #ความเร็วenmy
allenemy = 3 #จำนวนvirus

for i in range(allenemy):

	exlist.append(random.randint(50,WIDTH - esize))
	eylist.append(random.randint(0,100))
	#ey_change_list.append(random.randint(1,5)) #สุ่มความเร็ว
	ey_change_list.append(1) #กำหนดความเร็วเป็น 1 เเล้วเพิ่ม



#################MASK################
# 3 - mask - mask.png
msize = 32
mimg = pygame.image.load('mask.png')
mx = 100
my = HEIGHT - psize
mychange = 30  #ความเร็วmask
mstate = 'ready'

def fire_mask(x,y):
	global mstate
	mstate = 'fire'
	screen.blit(mimg,(x,y))
###################COLLISION##############
def isCollision(ecx,ecy,mcx,mcy):
	distance = math.sqrt(math.pow(ecx - mcx,2)+math.pow(ecy - mcy,2))
	print(distance)
	if distance < (esize / 2)+(msize / 2):
		return True
	else:
		return False

###################SCORE######################

allscore = 0
font = pygame.font.Font('angsana.ttc',36)

def showscore():
	score = font.render('คะเเนน: {} คะเเนน'.format(allscore),True,(255,255,255))
	screen.blit(score,(30,30))


###################SOUND######################
pygame.mixer.music.load('bgs.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

sound = pygame.mixer.Sound('intro.wav')
sound.play()


###################GAME OVER######################
fontover = pygame.font.Font('angsana.ttc',120)
fontover2 = pygame.font.Font('angsana.ttc',80)
playsound = False
gameover = False
def GameOver():
	global playsound
	global gameover
	overtext = fontover.render('เเย่จังเเพ้เเล้วหล่ะ',True,(255,0,0))
	screen.blit(overtext,(225,275))
	overtext2 = fontover2.render('รีบกด [N] เพื่อเริ่มใหม่สิ',True,(0,255,64))
	screen.blit(overtext2,(225,425))
	if playsound == False:
		gsound = pygame.mixer.Sound('Fail.mp3')
		gsound.play()
		playsound = True
	#if gameover == False:
	#	gameover = True


###################GAME LOOP######################

running = True 
clock = pygame.time.Clock()
FPS = 60
while running:

	screen.blit(background,(0,0))
	clock.tick(FPS)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				pxchange = -15
			if event.key == pygame.K_RIGHT:
				pxchange = 15

			if event.key == pygame.K_SPACE:
				if mstate == 'ready':
					sound = pygame.mixer.Sound('lazer.wav')
					sound.play()
					mx = px + 32
					fire_mask(mx,my)

			if event.key == pygame.K_n:
				#gameover = False
				playsound = False
				allscore = 0
				for i in range(allenemy):
					eylist[i] = random.randint(0,100)
					exlist[i] = random.randint(50,WIDTH - esize)

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				pxchange = 0
			


#################RUN PLAYER######################

	Player(px,py) #จุดเริ่ม
	
	if px <= 0:
			px = 0
			px += pxchange
	elif px >= WIDTH - psize:
			px = WIDTH - psize
			px += pxchange
	else:
			px += pxchange


#########################RUN ENMY SINGLE############
	#Enemy(ex,ey)
	#ey += eychange 

#########################RUN MULTI ENMY############
	
	for i in range(allenemy):

		if eylist[i] > HEIGHT - esize and gameover == False:
			for i in range(allenemy):
				eylist[i] = 1000
			GameOver()
			break

		eylist[i] += ey_change_list[i]
		colissionmulti = isCollision(exlist[i], eylist[i],mx,my)
		if colissionmulti:
			my = HEIGHT - psize
			mstate = 'ready'
			eylist[i] = 0
			exlist[i] = random.randint(50,WIDTH - esize)
			allscore += 1
			ey_change_list[i] += 1
			sound = pygame.mixer.Sound('coin.wav')
			sound.play()

		Enemy(exlist[i], eylist[i])



		Enemy(exlist[i], eylist[i])

#########################FIRE MASK############
	if mstate == 'fire':
		fire_mask(mx,my)
		my = my - mychange

	if my <= 0: #เช็คว่าเเมสชนขอบบนยังเเล้วเปลี่ยนstate
		my = HEIGHT - psize
		mstate = 'ready'


	collision = isCollision(ex,ey,mx,my) #เช็คว่าชนมั้ย
	if collision:
		my = HEIGHT - psize
		mstate = 'ready'
		ey = 0
		ex = random.randint(50,WIDTH - esize) #สุ่มเลขขนาดความกว้างหน้าจอ - ขนาดไวรัส
		allscore += 1

	showscore()
	print(px)
	pygame.display.update()
	pygame.display.flip()
	pygame.event.pump()
	screen.fill((0,0,0))



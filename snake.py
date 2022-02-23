import pygame
import random

# global vars
screenWidth = 800
screenHeight = 600
speed = blockSize = 10
FPS = 20

white = (255, 255, 255)
black = (0, 0, 0)
grey = (140, 140, 140)
red = (255, 0, 0)
orange = (255, 0xc9, 0x66) 
snakeGreen = (0, 216, 0)
green = (0, 255, 0)
yellow = (200, 200, 0)
brown = (0x8B, 0x45, 0x13)

# initialize pygame
pygame.init()
# game surface
gameDisplay = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Snake")
# get images
snakeHeadImg = pygame.image.load("images/snake_head.png")
snakeHeadImg = pygame.transform.scale(snakeHeadImg, (blockSize, blockSize))
appleImg = pygame.image.load("images/apple.png")
appleImg = pygame.transform.scale(appleImg, (blockSize, blockSize))
# sounds
crunchSound = pygame.mixer.Sound("sounds/crunch.wav")


clock = pygame.time.Clock()
direction = "right"

def pause():
	""" Pauses the game """
	
	paused = True
	
	while paused:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					paused = False
				elif event.key == pygame.K_q:
					pygame.quit()
					quit()
	
		gameDisplay.fill(grey)
		printToScreen("Paused", black, -40, "huge")
		printToScreen("Press C to continue, or Q to quit", green, 80, "medium")
		pygame.display.update()
		clock.tick(2)

def displayScoreBoard(score):
	""" Displays Scoreboard """
	
	pygame.display.set_caption("Slither - Score: " + str(score))
	#printToScreen(str(score), black, - screenHeight / 2 + 10)

def start():
	""" Displays a friendly splash screen """
	
	intro = True
	
	global FPS
	
	while intro:
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			
			#elif event.type == pygame.MOUSEBUTTONDOWN:
				
			
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					pygame.quit()
					quit()
				elif event.key == pygame.K_1:
					intro = False
					FPS = 10
					gameLoop()
				elif event.key == pygame.K_2:
					intro = False
					FPS = 20
					gameLoop()
				elif event.key == pygame.K_3:
					intro = False
					FPS = 30
					gameLoop()
				elif event.key == pygame.K_4:
					intro = False
					FPS = 40
					gameLoop()
				elif event.key == pygame.K_5:
					intro = False
					FPS = 50
					gameLoop()
				elif event.key == pygame.K_6:
					intro = False
					FPS = 60
					gameLoop()
		
		gameDisplay.fill(white)
		printToScreen("Welcome to Slither", green, -100, "large")
		printToScreen("Objective: Eat as many red apples as possible", black, -20, "medium")
		printToScreen("\t\t\t\tThe more you eat the longer you become", black, 0, "medium")
		printToScreen("\t\t\t\tIf you run into yourself or the edges you Die", black, 20, "medium")
		printToScreen("Press 1, 2, 3, 4, 5 or 6 to choose difficulty", orange, 60, "medium")
		printToScreen("higher # => higher difficulty ", orange, 90, "medium")
		printToScreen("or press Q to quit ", orange, 120, "medium")
		
		# create / simulate a button
		buttonWidth = 100; buttonHeight = 50
		buttonX = screenWidth / 2 - buttonWidth / 2
		buttonY = screenHeight - screenHeight / 6
		pygame.draw.rect(gameDisplay, yellow, (buttonX, buttonY, 
											   buttonWidth, buttonHeight))
		printToScreen("Play", brown, 220, "large")
		# hovering over the button:
		#cursor = pygame.mouse.get_pos()
		# if within button bounds make the button change color draw.rect()
		# if clicking within bounds execute action...
		pygame.display.update()
		clock.tick(2)

def moveSnake(snakeList, size):
	""" Draw snake onto the screen """
	
	if direction == "up":
		head = snakeHeadImg
	elif direction == "left":
		head = pygame.transform.rotate(snakeHeadImg, 90)
	elif direction == "down":
		head = pygame.transform.rotate(snakeHeadImg, 180)
	elif direction == "right":
		head = pygame.transform.rotate(snakeHeadImg, 270)
	
	gameDisplay.blit(head, (snakeList[-1][0], snakeList[-1][1]))
		
	for XnY in snakeList[:-1]:
		# the fill method is preffered, because it is GPU accelerated
		gameDisplay.fill(snakeGreen, rect=[XnY[0], XnY[1], size, size])

def createFont(msg, color, textSize):
	if textSize == "small":
		smallFont = pygame.font.SysFont("None", 12)
		textSurface = smallFont.render(msg, True, color)
		return textSurface, textSurface.get_rect()
	elif textSize == "medium":
		mediumFont = pygame.font.SysFont("comicsansms", 24)
		textSurface = mediumFont.render(msg, True, color)
		return textSurface, textSurface.get_rect()
	elif textSize == "large":
		largeFont = pygame.font.Font("fonts/CloisterBlack.ttf", 40)
		textSurface = largeFont.render(msg, True, color)
		return textSurface, textSurface.get_rect()
	elif textSize == "huge":
		hugeFont = pygame.font.SysFont("comicsansms", 80)
		textSurface = hugeFont.render(msg, True, color)
		return textSurface, textSurface.get_rect()

def printToScreen(msg, color, displaceY=0, textSize = "medium"):
	textSurface, textRect = createFont(msg, color, textSize)
	textRect.center = (screenWidth / 2), (screenHeight / 2) + displaceY
	gameDisplay.blit(textSurface, textRect)


def gameLoop():
	""" Main Game loop """
	
	global direction
	direction = "right"
	gameExit = False
	gameOver = False
	
	leadX = screenWidth / 2
	leadY = screenHeight / 2
	xChange = blockSize
	yChange = 0
	snakeList = []
	snakeLength = 1
	
	# placing the apple and rounding
	appleX = round(random.randrange(0, 
					screenWidth - blockSize) / blockSize) * blockSize
	appleY = round(random.randrange(0, 
					screenHeight - blockSize) / blockSize) * blockSize
	
	# Loop Enter #
	while not gameExit:
	
		while gameOver == True:
			gameDisplay.fill(white)
			printToScreen("Game Over.", red, -50, "large")
			printToScreen("Press C to play again, or Q to quit.", black, 50)
			pygame.display.update()
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameExit = True
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						gameExit = True
						gameOver = False
					if event.key == pygame.K_c:
						gameLoop()
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameExit = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT or event.key == pygame.K_a:
					direction = "left"
					xChange = -speed
					yChange = 0
				elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
					direction = "right"
					xChange = speed
					yChange = 0
				elif event.key == pygame.K_UP or event.key == pygame.K_w:
					direction = "up"
					yChange = -speed
					xChange = 0
				elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
					direction = "down"
					yChange = speed
					xChange = 0
				elif event.key == pygame.K_SPACE:
					pause()
				elif event.key == pygame.K_q:
					gameExit = True
		
		# recognizing borders
		if (leadX >= screenWidth or leadX < 0 or 
			leadY >= screenHeight or leadY < 0):
			gameOver = True
		
		leadX += xChange 
		leadY += yChange
		
		# set bg color
		gameDisplay.fill(white)
		# draw apple
		gameDisplay.blit(appleImg, (appleX, appleY))
		
		snakeHead = []
		snakeHead.append(leadX)
		snakeHead.append(leadY)
		snakeList.append(snakeHead) # a list of pairs
		
		if len(snakeList) > snakeLength:
			del snakeList[0]
		
		# check collision with self
		for eachSegment in snakeList[:-1]:
			if eachSegment == snakeHead:
				gameOver = True
		
		moveSnake(snakeList, blockSize)
		displayScoreBoard(snakeLength - 1)
		pygame.display.update()
		
		# collision detection
		# nesting IFs are equivalent to an AND statement
		if (leadX + blockSize > appleX and leadX < appleX + blockSize):
			if (leadY + blockSize > appleY and leadY < appleY + blockSize):
				crunchSound.play()
				appleX = round(random.randrange(0, screenWidth - blockSize) / blockSize) * blockSize
				appleY = round(random.randrange(0, screenHeight - blockSize) / blockSize) * blockSize
				snakeLength += 1
		
		clock.tick(FPS) # for every second  X frames should pass

	pygame.quit()
	quit()


if __name__ == '__main__':
	start()
import pygame
from pygame.locals import *
import random
import time
from pygame import mixer
pygame.init()
mixer.init()

#initialize screen
width = 600 
height = 600
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("snake")
#pygame.display.set_icon("")

#music
mixer.music.load("song.mp3")
mixer.music.play()

#clock and time 
clock = pygame.time.Clock()

#font
font1 = pygame.font.SysFont(None,40)
font2 = pygame.font.SysFont(None,60)

#color 
white = (255,255,255)
black = (0,0,0)
blue = (0,0,255)
green = (0,255,0)
red = (255,0,0)
final_color = (200,100,140)
screen_col = (200,150,100)

def draw_win():
    screen.fill(screen_col)
#score and print score
score = 0
def draw_score():
    score_txt = "Score : " + str(score)
    score_img = font1.render(score_txt,True,final_color)
    screen.blit(score_img,(0,0))
#snake
cell_size = 10
snake_pos = [[width // 2,height // 2]]
snake_pos.append([width // 2,height // 2 + cell_size * 1])
snake_pos.append([width // 2,height // 2 + cell_size * 2])
snake_pos.append([width // 2,height // 2 + cell_size * 3])

#food
food_size = 10
new_food = True
food_pos = [0,0]
img_food = pygame.image.load("food.png")
img_food = pygame.transform.scale(img_food,(cell_size,cell_size))

#head 
img_head = pygame.image.load("head.png")
#img_head = pygame.transform.scale(img_head,(cell_size,cell_size))

#over 1 -> end
game_over = 0
def check_end():
    global game_over
    x = snake_pos[0][0]
    y = snake_pos[0][1]
    if x < 0 or x > width or y < 0 or y > height:
        game_over = 1
        return True
    head = True
    for pos in snake_pos:
        if pos == [x,y] and head != True:
            game_over = 1
            return True
        head = False
    return False
again_rect = pygame.Rect((width // 2 - 50,height // 2 + 50,200,40))
def conclusion():
    final_text = "Your silly is " + str(score)
    final_text_img = font2.render(final_text,True,final_color)
    screen.blit(final_text_img,(width // 2 - 100,height // 2))
    again_text = "Wanna again ?"
    again_text_img = font1.render(again_text,True,final_color)
    pygame.draw.rect(screen,screen_col,again_rect)
    screen.blit(again_text_img,(width // 2 - 50,height // 2 + 50))
    screen.blit(img_head,(width // 2 - 100,100))

#run 
running = True
clicked = False
# set direction 1 -> up, 2 -> left and 3 -> down and 4 -> right
direction = 1

# frame persec
update_snake = 0

while running :
    #clock.tick(60)
    draw_win()
    draw_score()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False   
        if game_over == 0:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and direction != 3:
                    direction = 1 
                if event.key == pygame.K_a and direction != 4:
                    direction = 2
                if event.key == pygame.K_s and direction != 1:
                    direction = 3
                if event.key == pygame.K_d and direction != 2:
                    direction = 4
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            if event.type == pygame.MOUSEBUTTONUP and clicked == True:
                clicked = False
                pos = pygame.mouse.get_pos()
                if again_rect.collidepoint(pos):
                    game_over = 0
                    score = 0
                    snake_pos = [[width // 2,height // 2]]
                    snake_pos.append([width // 2,height // 2 + cell_size * 1])
                    snake_pos.append([width // 2,height // 2 + cell_size * 2])
                    snake_pos.append([width // 2,height // 2 + cell_size * 3])

    #create food
    if new_food == True:
        new_food = False
        food_pos[0] = cell_size * random.randint(0,(width // cell_size) - 1)
        food_pos[1] = cell_size * random.randint(0,(height // cell_size) - 1)
    pygame.draw.rect(screen,red,(food_pos[0],food_pos[1],cell_size,cell_size))
    #screen.blit(img_food,(food_pos[0],food_pos[1]))
    if snake_pos[0] == food_pos:
        score += 1
        new_food = True
        new_body = list(snake_pos[-1])
        if direction == 1:
            new_body[1] += cell_size
        if direction == 3:
            new_body[1] -= cell_size
        if direction == 2:
            new_body[0] += cell_size
        if direction == 4:
            new_body[0] -= cell_size
        snake_pos.append(new_body)
    
    if check_end() == False:
        if update_snake > 99:
            update_snake = 0
            tail = snake_pos[-1]
            snake_pos = snake_pos[-1:] + snake_pos[:-1]
            if direction == 1: #up
                snake_pos[0][0] = snake_pos[1][0]
                snake_pos[0][1] = snake_pos[1][1] - cell_size
            if direction == 3: #down
                snake_pos[0][0] = snake_pos[1][0]
                snake_pos[0][1] = snake_pos[1][1] + cell_size
            if direction == 2: #left
                snake_pos[0][1] = snake_pos[1][1]
                snake_pos[0][0] = snake_pos[1][0] - cell_size
            if direction == 4: #right
                snake_pos[0][1] = snake_pos[1][1]
                snake_pos[0][0] = snake_pos[1][0] + cell_size
    head = False
    for pos in snake_pos:
        x = pos[0]
        y = pos[1]
        pygame.draw.rect(screen,green,(x,y,cell_size,cell_size))
        if head == False :
            pygame.draw.rect(screen,red,(x+1,y+1,cell_size - 2,cell_size - 2))
            #screen.blit(img_head,(x,y))
            head = True
        else :
            pygame.draw.rect(screen,blue,(x+1,y+1,cell_size - 2,cell_size - 2))
   
    if game_over == 1:
        # running = False
        conclusion()
   
    update_snake += 1
    pygame.display.update()

pygame.quit()
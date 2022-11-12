from asyncio.windows_events import NULL
import os
import pygame, sys, random

#------------------------------Initialising Pygame-------------------------------#

pygame.init()
clock = pygame.time.Clock()

os.chdir('D:\\Programming Projects\\Python Projects\\Pong Game (Pygame)')

#---------------------------------Screen and FPS---------------------------------#

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption('DEFLECT')


#--------------------------------Ball and Players--------------------------------#

ball = pygame.Rect(SCREEN_WIDTH/2 - 8, SCREEN_HEIGHT/2 - 8, 17, 17 )

player1 = pygame.Rect(SCREEN_WIDTH - 30, SCREEN_HEIGHT/2 - 50, 13, 100)
player2 = pygame.Rect(15, SCREEN_HEIGHT/2 - 50, 13, 100)

#--------------------------------Colour Constants--------------------------------#
BACKGROUND_COLOR = (25, 25, 25)
COLOR = [(255, 6, 0), (50, 110, 255), (100, 0, 150), (230, 230, 230)] 
 
#-------------------------Setting up Delta X and Delta Y-------------------------#
dx = 8.5 * random.choice((1, -1))
dy = 6.4 * random.choice((1, -1))

#--------------------------------Player Attributes-------------------------------#

player_attrib_1 = [0, 0] #[0] = position [1] = score
player_attrib_2 = [0, 0] #same as above

#--------------------------------------Fonts-------------------------------------#

GAME_FONT = pygame.font.SysFont('freesansbold.ttf', 56)
END_FONT = pygame.font.SysFont('freesansbold.ttf', 76)

running = False
end = False

#---------------------------Center the Ball After Score--------------------------#

def center():
    global dy, dx
    ball.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

    dx = 8.5 * random.choice((1, -1))
    dy = 6.4 * random.choice((1, -1))

#------------------------------Restarting The Game-------------------------------#

def reset():
    global dy, dx, win_text
    player_attrib_1[1] = 0
    player_attrib_2[1] = 0

    dx = 8.5 * random.choice((1, -1))
    dy = 6.4 * random.choice((1, -1))

    win_text = NULL

#---------------------------------Draw Function----------------------------------#

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 2, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

#------------------------------------Main Menu-----------------------------------#

def main_menu():
    global running
    while True:
        for event in pygame.event.get():
            # Input
            if event.type == pygame.QUIT: # Quit Game
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN: # Play
                if event.key == pygame.K_ESCAPE:
                    running = True
                    game()

        screen.fill(BACKGROUND_COLOR)
        draw_text("DEFLECT", END_FONT, COLOR[1], screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 100)
        draw_text("Press Escape to Begin or Pause", GAME_FONT, COLOR[0], screen, SCREEN_WIDTH/2 , SCREEN_HEIGHT/2 )

        pygame.display.flip()
        clock.tick(FPS)

#-------------------------------------Game-------------------------------------#

def game():
    global dx, dy, COLOR, BACKGROUND_COLOR, running, win_text, end
    while running:
        for event in pygame.event.get():
            # Input
            if event.type == pygame.QUIT: # Quit Game
                pygame.quit()
                sys.exit()

#-------------------------------------Input-------------------------------------#

            if event.type == pygame.KEYDOWN: # Pause 
                if event.key == pygame.K_ESCAPE:
                    running = False
                    main_menu()
            
            if event.type == pygame.KEYDOWN: # Movement
                if event.key == pygame.K_DOWN:
                    player_attrib_1[0] += 10
                if event.key == pygame.K_UP:
                    player_attrib_1[0] -= 10
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player_attrib_1[0] -= 10
                if event.key == pygame.K_UP:
                    player_attrib_1[0] += 10                  
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    player_attrib_2[0] += 10
                if event.key == pygame.K_w:
                    player_attrib_2[0] -= 10
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    player_attrib_2[0] -= 10
                if event.key == pygame.K_w:
                    player_attrib_2[0] += 10

            if end == True and event.type == pygame.KEYDOWN: #Restart
                if event.key == pygame.K_s or event.key == pygame.K_w or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    end = False    
                    reset()                     

#-------------------------------Rendering Stuff------------------------------#     

        screen.fill(BACKGROUND_COLOR)
        
        pygame.draw.rect(screen, COLOR[1], player1)
        pygame.draw.rect(screen, COLOR[0], player2)
        
        pygame.draw.ellipse(screen, COLOR[0], ball)
        
        pygame.draw.aaline(screen, COLOR[2], (SCREEN_WIDTH/2, 0), (SCREEN_WIDTH/2, SCREEN_HEIGHT))
        
        draw_text(f"{player_attrib_1[1]}      {player_attrib_2[1]}", GAME_FONT, COLOR[2], screen, SCREEN_WIDTH/2, 50)
#-------------------------Movement Physics and Score-------------------------# 
        
        ball.x += dx
        ball.y += dy
        
        player1.y += player_attrib_1[0]
        player2.y += player_attrib_2[0]    
        
        if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
            dy = -dy
            
        if ball.left <= -1:
            center()
            player_attrib_2[1] += 1
            
        if ball.right >= SCREEN_WIDTH + 1:
            center()
            player_attrib_1[1] += 1
        
        if ball.colliderect(player1) and dx > 0:
            if abs(ball.right - player1.left) < 10:
                dx = -dx
            elif abs(ball.top - player1.bottom) < 10 and dy < 0:
                dy = -dy

            elif abs(ball.bottom - player1.top) < 10 and dy > 0:
                dy = -dy
        
        if ball.colliderect(player2) and dx < 0:
            if abs(ball.left - player2.right) < 10:
                dx = -dx
            elif abs(ball.top - player2.bottom) < 10 and dy < 0:
                dy = -dy

            elif abs(ball.bottom - player2.bottom) < 10 and dy > 0:
                dy = -dy

        if player1.top <= 5:
            player1.top = 5
            
        if player1.bottom >= SCREEN_HEIGHT - 5:
            player1.bottom = SCREEN_HEIGHT - 5
            
        if player2.top <= 5:
            player2.top = 5
            
        if player2.bottom >= SCREEN_HEIGHT - 5:
            player2.bottom = SCREEN_HEIGHT - 5
#---------------------------------Ending--------------------------------#
        
        if player_attrib_1[1] == 15 or player_attrib_2[1] == 15:
            dx = 0
            dy = 0
            player_attrib_1[0] = 0
            player_attrib_2[0] = 0
            draw_text(f"Game Over : Press Arrow Keys to Restart", GAME_FONT, COLOR[3], screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
            end = True
        
        # FPS
        pygame.display.flip()
        clock.tick(FPS)
    
main_menu()

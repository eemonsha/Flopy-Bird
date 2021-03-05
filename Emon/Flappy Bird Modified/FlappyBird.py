#!/usr/bin/env python

#Importing libraries
import os, sys, pygame, random, math
from pygame.locals import *
from gameFunctions import *
from gameClasses import *
import gameVariables

def main():
    #Initializing pygame & mixer
    screen = initialize_pygame()

    #Setting up some timers 
    clock = pygame.time.Clock()
    pygame.time.set_timer(getNewPipe, pipesAddInterval)
    
    #Loading the images | Creating the bird | Creating the ground | Creating the game list
    gamePipes = []
    gameBird = Bird()
    gameImages = load_images()
    gameVariables.gameScore = 0
    gameGround = Ground(gameImages['ground'])
      
    #Loading the sounds
    jump_sound = pygame.mixer.Sound('sounds/jump.ogg')
    score_sound = pygame.mixer.Sound('sounds/score.ogg')
    dead_sound = pygame.mixer.Sound('sounds/dead.ogg')

    while(gameVariables.waitClick == True):
        #Draw everything and waitClick for the user to click to start the game
        #When we click somewhere, the bird will jump and the game will start
        screen.blit(gameImages['background'], (0, 0))
        draw_text(screen, "Click to start", 285, 20)
        screen.blit(gameImages['ground'], (0, gameHeight - groundHeight))

        #Drawing a "floating" flappy bird
        gameBird.redraw(screen, gameImages['bird'], gameImages['bird2'])

        #Updating the screen
        pygame.display.update()

        #Checking if the user pressed left click or space and start (or not) the game
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN or (e.type == pygame.KEYDOWN and e.key == K_SPACE):
                gameBird.steps_to_jump = 15
                gameVariables.waitClick = False
    jump_sound.play()
    
    #Loop until...we die!
    while True:
        #Drawing the background
        screen.blit(gameImages['background'], (0, 0))

        #Getting the mouse, keyboard or user events and act accordingly
        for e in pygame.event.get():
            if e.type == getNewPipe:
                p = PipePair(gameWidth, False)
                gamePipes.append(p)
            elif e.type == pygame.MOUSEBUTTONDOWN:
                gameBird.steps_to_jump = jumpSteps
                jump_sound.play()
            elif e.type == pygame.KEYDOWN:
                if e.key == K_SPACE:
                    gameBird.steps_to_jump = jumpSteps
                    jump_sound.play()
                elif e.key == K_ESCAPE:
                    exit()

        #Tick! (new frame)
        clock.tick(FPS)

        #Updating the position of the gamePipes and redrawing them; if a pipe is not visible anymore,
        #we remove it from the list
        for p in gamePipes:
            p.x -= pixelsFrame
            if p.x <= - pipeWidth:
                gamePipes.remove(p)
            else:
                screen.blit(gameImages['pipe-up'], (p.x, p.toph))
                screen.blit(gameImages['pipe-down'], (p.x, p.bottomh))

        #Redrawing the ground
        gameGround.move_and_redraw(screen)
        
        #Updating the bird position and redrawing it
        gameBird.update_position()
        gameBird.redraw(screen, gameImages['bird'], gameImages['bird2'])

        #Checks for any collisions between the gamePipes, bird and/or the lower and the
        #upper part of the screen
        if any(p.check_collision((gameBird.bird_x, gameBird.bird_y)) for p in gamePipes) or \
               gameBird.bird_y < 0 or \
               gameBird.bird_y + birdHeight > gameHeight - groundHeight:
            dead_sound.play()
            break

        #There were no collision if we ended up here, so we are checking to see if 
        #the bird went thourgh one half of the pipe's gameWidth; if so, we update the gameScore
        for p in gamePipes:
            if(gameBird.bird_x > p.x and not p.score_counted):
                p.score_counted = True
                gameVariables.gameScore += 1
                score_sound.play()

        #Draws the gameScore on the screen
        draw_text(screen, gameVariables.gameScore, 50, 35)
        
        #Updates the screen
        pygame.display.update()

    #We are dead now, so we make the bird "fall"
    while(gameBird.bird_y + birdHeight < gameHeight - groundHeight):
        #Redraws the background
        screen.blit(gameImages['background'], (0, 0))

        #Redrawing the gamePipes in the same place as when it died
        for p in gamePipes:
            screen.blit(gameImages['pipe-up'], (p.x, p.toph))
            screen.blit(gameImages['pipe-down'], (p.x, p.bottomh))

        #Draws the ground piece to get the rolling effect
        gameGround.move_and_redraw(screen)

        #Makes the bird fall down and rotates it
        gameBird.redraw_dead(screen, gameImages['bird'])

        #Tick!
        clock.tick(FPS * 3)
    
        #Updates the entire screen
        pygame.display.update()

    #Let's end the game!
    if not end_the_game(screen, gameScore):
        main()
    else:
        pygame.display.quit()
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    #- If this module had been imported, __name__ would be 'Flappy Bird';
    #otherwise, if it was executed (by double-clicking the file) we would call main
    main()

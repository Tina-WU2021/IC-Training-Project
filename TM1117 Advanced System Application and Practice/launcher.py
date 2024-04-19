# -*- coding: utf-8 -*-
"""
Created on Sat Jul  2 09:32:14 2022

@author: XiaoTao
"""
import pygame
import data

from pygame.locals import (
    RLEACCEL,
    K_LEFT,
    K_RIGHT,
    K_RETURN
)

resolution = [800, 600]
screen = pygame.display.set_mode(resolution)

pygame.display.set_caption("Menu")
BG = pygame.image.load("image/launcher.png")
background = 0
BackgroundList = []

recording = False

username = ""

difficulties = {
    'Easy': {
    'initial_life': 8,
    'initial_shot': 5,
    'enemy_speed': [4, 8],
    'enemy_add': 900,
    'exp_up': 3000
    },
    
    'Normal': {
    'initial_life': 6,
    'initial_shot': 3,
    'enemy_speed': [6, 12],
    'enemy_add': 700,
    'exp_up': 2000
    },
    
    'Hard': {
    'initial_life': 4,
    'initial_shot': 1,
    'enemy_speed': [8, 15],
    'enemy_add': 500,
    'exp_up': 1200
    },
    
    'Expert': {
    'initial_life': 1,
    'initial_shot': 0,
    'enemy_speed': [10, 20],
    'enemy_add': 300,
    'exp_up': 500
    },
    }

for i in range(0,3):
    BackgroundList += ["image/background/{}_icon.png".format(str(i))]
    BackgroundList += ["image/background/{}.png".format(str(i))]

class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
    	self.image = image
    	self.x_pos = pos[0]
    	self.y_pos = pos[1]
    	self.font = font
    	self.base_color, self.hovering_color = base_color, hovering_color
    	self.text_input = text_input
    	self.text = self.font.render(self.text_input, True, self.base_color)
    	if self.image is None:
    		self.image = self.text
    	self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
    	self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
    
    def update(self, screen):
    	if self.image is not None:
    		screen.blit(self.image, self.rect)
    	screen.blit(self.text, self.text_rect)
    
    def checkForInput(self, position):
    	if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
    		return True
    	return False
    
    def changeColor(self, position, key, key_pressed):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        elif key and pygame.key.get_pressed()[key_pressed]:
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

def get_font(size):
    return pygame.font.Font("font.ttf", size)

def switch(switching):
    global background
    pygame.display.init()
    while switching:
        pygame.display.update()
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        screen.blit(BG, (0, 0))
        switch_text = get_font(25).render("Select the backgorund", True, "White")
        switch_rect = switch_text.get_rect(center=(400,70))
        screen.blit(switch_text, switch_rect)
        
        switch_text = get_font(22).render("press confirm to return to main menu", True, "White")
        switch_rect = switch_text.get_rect(center=(400,100))
        screen.blit(switch_text, switch_rect)
        
        Options_next = Button(image=None, pos=(700, 300),
            text_input="Next", font=get_font(25),
            base_color="White", hovering_color="Green"
            )
        Options_next.changeColor(OPTIONS_MOUSE_POS, True, K_RIGHT)
        Options_next.update(screen)
        
        Options_previous = Button(image=None, pos=(100, 300),
            text_input="Previous", font=get_font(25),
            base_color="White", hovering_color="Green"
            )
        Options_previous.changeColor(OPTIONS_MOUSE_POS, True, K_LEFT)
        Options_previous.update(screen)
        
        Options_confirm = Button(image=None, pos=(400, 500),
            text_input="Confirm", font=get_font(25),
            base_color="White", hovering_color="Green"
            )
        Options_confirm.changeColor(OPTIONS_MOUSE_POS, True, K_RETURN)
        Options_confirm.update(screen)
        
        switch = pygame.image.load(BackgroundList[background]).convert_alpha()
        switch.set_colorkey([255, 255, 255], RLEACCEL)
        switch_rect = switch.get_rect(center = [400,300])
        screen.blit(switch, switch_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Options_next.checkForInput(OPTIONS_MOUSE_POS):
                    background += 2
                    if background == len(BackgroundList):
                        background = 0
                if Options_previous.checkForInput(OPTIONS_MOUSE_POS):
                    background -= 2
                    if background == -2:
                        background = len(BackgroundList) - 2
                if Options_confirm.checkForInput(OPTIONS_MOUSE_POS):
                    switching = False
                    pygame.init()
                    main_menu(True, "main")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    background -= 2
                    if background == -2:
                        background = len(BackgroundList) - 2
                if event.key == pygame.K_RIGHT:
                    background += 2
                    if background == len(BackgroundList):
                        background = 0
                if event.key == pygame.K_RETURN:
                    switching = False
                    pygame.init()
                    main_menu(True, "main")
                    
def options(option):
    record = data.readrecord("record.txt")
    while option:
        pygame.display.update()
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.blit(BG, (0, 0))

        OPTIONS_TEXT = get_font(35).render("Previous game records", True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(400, 40))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)
        
        if record == []:
            NOREC_TEXT = get_font(35).render("No records", True, "White")
            NOREC_RECT = NOREC_TEXT.get_rect(center=(400, 300))
            screen.blit(NOREC_TEXT, NOREC_RECT)
        
        else:
            TITLE0 = get_font(20).render("Ranking", True, "White")
            TITLE0_RECT = TITLE0.get_rect(center=(80, 100))
            screen.blit(TITLE0, TITLE0_RECT)
            TITLE1 = get_font(20).render("Player", True, "White")
            TITLE1_RECT = TITLE1.get_rect(center=(200, 100))
            screen.blit(TITLE1, TITLE1_RECT)
            TITLE2 = get_font(20).render("Time", True, "White")
            TITLE2_RECT = TITLE2.get_rect(center=(400, 100))
            screen.blit(TITLE2, TITLE2_RECT)
            TITLE3 = get_font(20).render("Difficulty", True, "White")
            TITLE3_RECT = TITLE3.get_rect(center=(580, 100))
            screen.blit(TITLE3, TITLE3_RECT)
            TITLE4 = get_font(20).render("Level", True, "White")
            TITLE4_RECT = TITLE4.get_rect(center=(670, 100))
            screen.blit(TITLE4, TITLE4_RECT)
            TITLE5 = get_font(20).render("EXP", True, "White")
            TITLE5_RECT = TITLE5.get_rect(center=(740, 100))
            screen.blit(TITLE5, TITLE5_RECT)
            
            for i in range(0, min(10, len(record))):
                ENTRY0_TEXT = get_font(20).render(str(i + 1), True, "White")
                ENTRY0_RECT = ENTRY0_TEXT.get_rect(center=(80, 140 + 40 * i))
                screen.blit(ENTRY0_TEXT, ENTRY0_RECT)
                ENTRY1_TEXT = get_font(20).render(record[i]['Name'], True, "White")
                ENTRY1_RECT = ENTRY1_TEXT.get_rect(center=(200, 140 + 40 * i))
                screen.blit(ENTRY1_TEXT, ENTRY1_RECT)
                ENTRY2_TEXT = get_font(20).render(record[i]['Time'], True, "White")
                ENTRY2_RECT = ENTRY2_TEXT.get_rect(center=(400, 140 + 40 * i))
                screen.blit(ENTRY2_TEXT, ENTRY2_RECT)
                ENTRY3_TEXT = get_font(20).render(record[i]['Record']['Difficulty'], True, "White")
                ENTRY3_RECT = ENTRY3_TEXT.get_rect(center=(580, 140 + 40 * i))
                screen.blit(ENTRY3_TEXT, ENTRY3_RECT)
                ENTRY4_TEXT = get_font(20).render(str(record[i]['Record']['Level']), True, "White")
                ENTRY4_RECT = ENTRY4_TEXT.get_rect(center=(670, 140 + 40 * i))
                screen.blit(ENTRY4_TEXT, ENTRY4_RECT)
                ENTRY5_TEXT = get_font(20).render(str(record[i]['Record']['EXP']), True, "White")
                ENTRY5_RECT = ENTRY5_TEXT.get_rect(center=(740, 140 + 40 * i))
                screen.blit(ENTRY5_TEXT, ENTRY5_RECT)
            
            if len(record) < 9:
                NOREC_TEXT = get_font(30).render("No more records", True, "White")
                NOREC_RECT = NOREC_TEXT.get_rect(center=(400, 295 + 20 * len(record)))
                screen.blit(NOREC_TEXT, NOREC_RECT)
            
        OPTIONS_BACK = Button(
            image=None, pos=(400, 550),
            text_input="BACK", font=get_font(25),
            base_color="White", hovering_color="Green"
            )

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS, False, 0)
        OPTIONS_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    option = False
                    main_menu(True, "main")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    option = False
                    main_menu(True, "main")
                
def settings(setting):
    global username, difficulty, playing, running, start
    pygame.init()
    
    username_input = True
    
    while setting:
        pygame.display.update()
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        
        MENU_TEXT = get_font(60).render("SETTINGS", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))
        screen.blit(MENU_TEXT, MENU_RECT)
        
        if username_input:
            username_title = get_font(25).render("Please input your name:", True, "White")
            username_title_rect = username_title.get_rect(center=(400,250))
            screen.blit(username_title, username_title_rect)
            
            username_text = get_font(40).render(username, True, "White")
            username_rect = username_text.get_rect(center=(400,300))
            screen.blit(username_text, username_rect)
            
            CONFIRM_BUTTON = Button(image=None, pos=(400, 500),
                text_input="Confirm", font=get_font(25),
                base_color="White", hovering_color="Green"
                )
            CONFIRM_BUTTON.changeColor(MENU_MOUSE_POS, False, 0)
            CONFIRM_BUTTON.update(screen)
        
        else:
            if username == "":
                username = "Default User"
            
            EASY_BUTTON = Button(
                image = None, pos = (400, 200),
                text_input = "EASY", font = get_font(40), 
                base_color = "#d7fcd4", hovering_color = "White"
                )
            NORMAL_BUTTON = Button(
                image = None, pos = (400, 300),
                text_input = "NORMAL", font = get_font(40), 
                base_color = "#d7fcd4", hovering_color = "White"
                )
            HARD_BUTTON = Button(
                image = None, pos = (400, 400),
                text_input = "HARD", font = get_font(40),
                base_color = "#d7fcd4", hovering_color = "White"
                )
            EXPERT_BUTTON = Button(
                image = None, pos = (400, 500),
                text_input = "EXPERT", font = get_font(40),
                base_color = "#d7fcd4", hovering_color = "White"
                )
            
            for button in [EASY_BUTTON, NORMAL_BUTTON, HARD_BUTTON, EXPERT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS, False, 0)
                button.update(screen)
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if username_input:
                    if CONFIRM_BUTTON.checkForInput(MENU_MOUSE_POS):
                        username_input = False
                else:
                    if EASY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        playing = True
                        running = True
                        pygame.init()
                        setting = False
                        difficulty = "Easy"
                        start = pygame.time.get_ticks()
                    if NORMAL_BUTTON.checkForInput(MENU_MOUSE_POS):
                        playing = True
                        running = True
                        pygame.init()
                        setting = False
                        difficulty = "Normal"
                        start = pygame.time.get_ticks()
                    if HARD_BUTTON.checkForInput(MENU_MOUSE_POS):
                        playing = True
                        running = True
                        pygame.init()
                        setting = False
                        difficulty = "Hard"
                        start = pygame.time.get_ticks()
                    if EXPERT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        playing = True
                        running = True
                        pygame.init()
                        setting = False
                        difficulty = "Expert"
                        start = pygame.time.get_ticks()
                           
            if event.type == pygame.KEYDOWN:
                if username_input:
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    elif event.key == K_RETURN:
                        username_input = False
                    else:
                        username += event.unicode

def main_menu(show, mode):   
    global start, running, playing, recording
    pygame.init()
    
    while show:
        pygame.display.update()
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        if mode == "main":
            MENU_TEXT = get_font(60).render("MAIN MENU", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))
            
            PLAY_BUTTON = Button(
                image = None, pos = (400, 200),
                text_input = "START", font = get_font(40), 
                base_color = "#d7fcd4", hovering_color = "White"
                )
            SWITCH_BUTTON = Button(
                image = None, pos = (400, 300),
                text_input = "MAP SELECTION", font = get_font(40), 
                base_color = "#d7fcd4", hovering_color = "White"
                )
            OPTIONS_BUTTON = Button(
                image = None, pos=(400, 400),
                text_input = "RECORD", font = get_font(40),
                base_color = "#d7fcd4", hovering_color = "White"
                )
            QUIT_BUTTON = Button(
                image = None, pos = (400, 500),
                text_input = "QUIT", font = get_font(40),
                base_color = "#d7fcd4", hovering_color = "White"
                )
            
            buttons = [PLAY_BUTTON, SWITCH_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]


        elif mode == "pause":
            pygame.mixer.music.pause()
            MENU_TEXT = get_font(60).render("PAUSED", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))
            
            RESUME_BUTTON = Button(
                image = None, pos=(400, 300),
                text_input = "RESUME", font = get_font(40),
                base_color = "#d7fcd4", hovering_color = "White"
                )
            QUIT_BUTTON = Button(
                image = None, pos = (400, 400),
                text_input = "QUIT", font = get_font(40),
                base_color = "#d7fcd4", hovering_color = "White"
                )

            buttons = [RESUME_BUTTON, QUIT_BUTTON]
            
        elif mode == "over":
            MENU_TEXT = get_font(60).render("GAME OVER", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))
            
            RETRY_BUTTON = Button(
                image = None, pos=(400, 250),
                text_input = "RETRY", font = get_font(40),
                base_color = "#d7fcd4", hovering_color = "White"
                )
            MENU_BUTTON = Button(
                image = None, pos=(400, 350),
                text_input = "MAIN MENU", font = get_font(40),
                base_color = "#d7fcd4", hovering_color = "White"
                )
            QUIT_BUTTON = Button(
                image = None, pos = (400, 450),
                text_input = "QUIT", font = get_font(40),
                base_color = "#d7fcd4", hovering_color = "White"
                )

            buttons = [RETRY_BUTTON, MENU_BUTTON, QUIT_BUTTON]
        
        screen.blit(MENU_TEXT, MENU_RECT)

        for button in buttons:
            button.changeColor(MENU_MOUSE_POS, False, 0)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                show = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mode == "main":
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        show = False
                        settings(True)
                    if SWITCH_BUTTON.checkForInput(MENU_MOUSE_POS):
                        show = False
                        switch(True)
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        show = False
                        options(True)
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        recording = True
                        playing = False
                        show = False

                elif mode == "pause":
                    if RESUME_BUTTON.checkForInput(MENU_MOUSE_POS):
                        show = False
                        pygame.mixer.music.unpause()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        recording = True
                        playing = False
                        show = False

                elif mode == "over":
                    if RETRY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        running = True
                        start = pygame.time.get_ticks()
                        show = False
                    if MENU_BUTTON.checkForInput(MENU_MOUSE_POS):
                        show = False
                        main_menu(True, "main")
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        playing = False
                        show = False
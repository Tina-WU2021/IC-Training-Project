# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 14:41:40 2022

@author: ic2140
"""

import pygame
import random
import launcher
import data

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("image/jet.png").convert_alpha()
        self.surf.set_colorkey([255, 255, 255], RLEACCEL)
        self.rect = self.surf.get_rect(
            center = [0, resolution[1] / 2]
            )
        
    def update(self, pressed_keys):
        if pressed_keys[K_UP] or pressed_keys[pygame.K_w]:
            self.rect.move_ip(0, -5)
            self.surf = pygame.image.load("image/jet_moving.png").convert_alpha()
        elif pressed_keys[K_DOWN] or pressed_keys[pygame.K_s]:
            self.rect.move_ip(0, 5)
            self.surf = pygame.image.load("image/jet.png").convert_alpha()
        elif pressed_keys[K_LEFT] or pressed_keys[pygame.K_a]:
            self.rect.move_ip(-5, 0)
            self.surf = pygame.image.load("image/jet.png").convert_alpha()
        elif pressed_keys[K_RIGHT] or pressed_keys[pygame.K_d]:
            self.rect.move_ip(5, 0)
            self.surf = pygame.image.load("image/jet_moving.png").convert_alpha()
        else:
            self.surf = pygame.image.load("image/jet.png").convert_alpha()
            
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= resolution[0]:
            self.rect.right = resolution[0]
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= resolution[1]:
            self.rect.bottom = resolution[1]

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("image/missile.png").convert_alpha()
        self.surf.set_colorkey([255, 255, 255], RLEACCEL)
        self.rect = self.surf.get_rect(
            center = [
                random.randint(resolution[0] + 20, resolution[0] + 100),
                random.randint(0, resolution[1])
                ]
            )
        self.speed = random.randint(difficulties[difficulty]['enemy_speed'][0],
                                    difficulties[difficulty]['enemy_speed'][1])
        
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
            
class Enemy_slow(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy_slow, self).__init__()
        self.surf = pygame.image.load("image/missile.png").convert_alpha()
        self.surf.set_colorkey([255, 255, 255], RLEACCEL)
        self.rect = self.surf.get_rect(
            center = [
                random.randint(resolution[0] + 20, resolution[0] + 100),
                random.randint(0, resolution[1])
                ]
            )
        self.speed = random.randint(difficulties[difficulty]['enemy_speed'][0]-3,
                                    difficulties[difficulty]['enemy_speed'][1]-3)
        
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
            
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("image/cloud.png").convert_alpha()
        self.surf.set_colorkey([255, 255, 255], RLEACCEL)
        self.rect = self.surf.get_rect(
            center = [
                random.randint(resolution[0] + 20, resolution[0] + 100),
                random.randint(0, resolution[1])
                ]
            )
        
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()
            
class Shot(pygame.sprite.Sprite):
    def __init__(self):
        super(Shot, self).__init__()
        self.surf = pygame.image.load("image/shot.png").convert_alpha()
        self.surf.set_colorkey([255, 255, 255], RLEACCEL)
        self.rect = self.surf.get_rect(
            center = [
                player.rect.right,
                player.rect.bottom
                ]
            )
        
    def update(self):
        self.rect.move_ip(20, 0)
        if self.rect.left > resolution[0]:
            self.kill()

class Explosion_Player(pygame.sprite.Sprite):
    def __init__(self):
        global location
        super(Explosion_Player, self).__init__()
        self.surf = pygame.image.load("image/explosion_big.png").convert_alpha()
        self.surf.set_colorkey([255, 255, 255], RLEACCEL)
        self.rect = self.surf.get_rect(
            center = [
                player.rect.right,
                player.rect.bottom
                ]
            )
        location = player.rect.right
    
    def update(self):
        self.rect.move_ip(-(difficulties[difficulty]['enemy_speed'][0]+difficulties[difficulty]['enemy_speed'][1])/2, 0)
        if self.rect.right < location - 20:
            self.kill()

class Explosion_Shot(pygame.sprite.Sprite):
    def __init__(self):
        global location
        super(Explosion_Shot, self).__init__()
        self.surf = pygame.image.load("image/explosion.png").convert_alpha()
        self.surf.set_colorkey([255, 255, 255], RLEACCEL)
        self.rect = self.surf.get_rect(
            center = [
                shot.rect.right,
                shot.rect.bottom
                ]
            )
        location = shot.rect.right
        
    def update(self):
        self.rect.move_ip(-(difficulties[difficulty]['enemy_speed'][0]+difficulties[difficulty]['enemy_speed'][1])/2, 0)
        if self.rect.right < location - 10:
            self.kill()
            
class Clear(pygame.sprite.Sprite):
    def __init__(self):
        global location
        super(Clear, self).__init__()
        self.surf = pygame.image.load("image/explosion_big.png").convert_alpha()
        self.surf.set_colorkey([255, 255, 255], RLEACCEL)
        self.rect = self.surf.get_rect(
            center = [
                enemy.rect.left,
                enemy.rect.bottom
                ]
            )
        location = enemy.rect.left
        
    def update(self):
        self.rect.move_ip(-(difficulties[difficulty]['enemy_speed'][0]+difficulties[difficulty]['enemy_speed'][1])/2, 0)
        if self.rect.right < location - 10:
            self.kill()

def exp_requirement(level):
    global requirement_total
    requirement_total = (level + 1) * level * 5
    return requirement_total

def record():
    global exp_total

launcher.main_menu(True,"main")
from launcher import playing

while playing:
    from launcher import username, difficulties

    # Initialization
    pygame.mixer.init()
    pygame.init()

    pygame.display.set_caption('Sky Wars')
    font_small = pygame.font.Font('font.ttf', 16)
    font = pygame.font.Font('font.ttf', 36)
    font_nano = pygame.font.Font('font.ttf', 12)
    resolution = [800, 600]
    screen = pygame.display.set_mode(resolution)

    from launcher import start, BackgroundList, background, running, difficulty
    level = 1
    life_total = difficulties[difficulty]['initial_life']
    exp_total = 0
    shot_total = difficulties[difficulty]['initial_shot']
    cdbar_value = 8
    cdtext_value = 0
    
    hit_enemies = 0
    tools = [1, 1, 1, 1]
    speeddown = False
    
    gameover_sound = pygame.mixer.Sound("sound/gameover.mp3")
    explosion_sound = pygame.mixer.Sound("sound/explosion.mp3")

    shooting = True
    lifebar_list = []
    expbar_list = []
    powerbar_list = []
    cdbar_list = []
    for i in range(0, 9):
        lifebar_list += ["image/lifebar/{}.png".format(str(i))]
        expbar_list += ["image/expbar/{}.png".format(str(i))]
        powerbar_list += ["image/powerbar/{}.png".format(str(i))]
        cdbar_list += ["image/cdbar/{}.png".format(str(i))]

    # Sprites Groups
    player = Player()
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    all_sprites.add(player)

    # Events
    ADDENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMY, difficulties[difficulty]['enemy_add'])
    ADDCLOUD = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDCLOUD, 1000)
    SHOOTING = pygame.USEREVENT + 3
    pygame.time.set_timer(SHOOTING, 15000)
    RECOVERING = pygame.USEREVENT + 4
    pygame.time.set_timer(RECOVERING, 10000)
    EXPUP = pygame.USEREVENT + 5
    pygame.time.set_timer(EXPUP, difficulties[difficulty]['exp_up'])
        
    if running:
        # BGM
        pygame.mixer.music.load("sound/bgm.mp3")
        pygame.mixer.music.play(loops=-1)
    
    while running:
        from launcher import playing, recording, running
        
        if recording:
            data.saverecord(username, difficulty, level, exp_total)
        
        if not playing:
            break
        
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    launcher.main_menu(True, "pause")
                    
                if event.key == K_SPACE:
                    if shooting and shot_total >= 1:
                        shot = Shot()
                        all_sprites.add(shot)
                        shot_total -= 1
                        shooting = False
                        exploded = False
                        cd = 5
                        shooting_start = pygame.time.get_ticks()
                    
                if event.key == pygame.K_1 or event.key == pygame.K_z:
                    if shooting and tools[0] >= 1:
                        shot = Shot()
                        all_sprites.add(shot)
                        tools[0] -= 1
                        shooting = False
                        exploded = True
                        cd = 10
                        shooting_start = pygame.time.get_ticks()
                        
                if event.key == pygame.K_2 or event.key == pygame.K_x:
                    if tools[1] >= 1:
                        tools[1] -= 1
                        for enemy in enemies:
                            explosion_sound.play()
                            new_explosion = Clear()
                            explosions.add(new_explosion)
                            all_sprites.add(new_explosion)
                            enemy.kill()
                            exp_total += 2
                            hit_enemies += 1
                            
                if event.key == pygame.K_3 or event.key == pygame.K_c:
                    if tools[2] >= 1:
                        tools[2] -= 1
                        life_total = 8
                
                if event.key == pygame.K_4 or event.key == pygame.K_v:
                    if tools[3] >= 1:
                        tools[3] -= 1
                        speeddown = True
                        speeddown_time = pygame.time.get_ticks()
                        for enemy in enemies:
                            enemy.speed -= 3
                        
            elif event.type == QUIT:
                launcher.main_menu(True, "pause")
            
            elif event.type == ADDENEMY:
                if speeddown:
                    new_enemy = Enemy_slow()
                else:
                    new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
            
            elif event.type == ADDCLOUD:
                new_cloud = Cloud()
                clouds.add(new_cloud)
                all_sprites.add(new_cloud)
            
            elif event.type == SHOOTING:
                if shot_total < 8:
                    shot_total += 1
            
            elif event.type == RECOVERING:
                if life_total < 8:
                    life_total += 1
                    
            elif event.type == EXPUP:
                exp_total += 1
        
        # Clock
        clock = pygame.time.get_ticks()
        survival = (clock - start) // 1000
        pygame.display.flip()
        pygame.time.Clock().tick(30)
        try:
            if speeddown and clock - speeddown_time >= 5000:
                for enemy in enemies:
                    enemy.speed += 3
                speeddown = False
        except:
            pass
        
        # Texts
        display_level = font_small.render("Level", True, [255, 0, 0])
        display_level_Rect = display_level.get_rect(center = [400, 30])
        display_level_value = font.render(str(level), True, [255, 0, 0])
        display_level_value_Rect = display_level_value.get_rect(center = [400, 55])
        hit_no = font_small.render("Enemies Hit:", True, [255, 0, 0])
        hit_no_Rect = display_level.get_rect(center = [60, 540])
        hit_no_value = font.render(str(hit_enemies), True, [255, 0, 0])
        hit_no_value_Rect = display_level_value.get_rect(center = [50, 570])
        
        # Shooting Related
        try:
            shooting_cd = clock - shooting_start
            cdtext_value = 5 - shooting_cd // 1000
            cdbar_value = shooting_cd * 1.6 // 1000
            
            if shooting_cd >= 5000:
                cdtext_value = 0
                cdbar_value = 8
                shooting = True
            
            shot.update()
            
            if pygame.sprite.spritecollideany(shot, enemies):
                if cd == 10 or not exploded:
                    hit = pygame.sprite.spritecollide(shot, enemies, True)
                    explosion_sound.play()
                    new_explosion = Explosion_Shot()
                    explosions.add(new_explosion)
                    all_sprites.add(new_explosion)
                    exp_total += 10
                    hit_enemies += 1
                    if hit_enemies > 0 and hit_enemies % 3 == 0:
                        tools[random.randint(0, 3)] += random.randint(0, 1)                    
                    exploded = True
                    if cd == 5:
                        shot.kill()                    
            
        except:
            pass 
        
        # Tools
        extra_shot = pygame.image.load("image/tools/extra_shot.png").convert_alpha()
        extra_shot.set_colorkey([255, 255, 255], RLEACCEL)
        extra_shot_rect = extra_shot.get_rect(center = [600, 550])
        extra_shot_value = font_nano.render(str(tools[0]), True, [0, 0, 255])
        extra_shot_value_Rect = extra_shot_value.get_rect(center = [615, 535])
        
        clear = pygame.image.load("image/tools/clear.png").convert_alpha()
        clear.set_colorkey([255, 255, 255], RLEACCEL)
        clear_rect = clear.get_rect(center = [650, 550])
        clear_value = font_nano.render(str(tools[1]), True, [0, 0, 255])
        clear_value_Rect = clear_value.get_rect(center = [665, 535])
        
        
        health = pygame.image.load("image/tools/health.png").convert_alpha()
        health.set_colorkey([255, 255, 255], RLEACCEL)
        health_rect = health.get_rect(center = [700, 550])
        health_value = font_nano.render(str(tools[2]), True, [0, 0, 255])
        health_value_Rect = health_value.get_rect(center = [715, 535]) 
        
        speed_down = pygame.image.load("image/tools/speed_down.png").convert_alpha()
        speed_down.set_colorkey([255, 255, 255], RLEACCEL)
        speed_down_rect = speed_down.get_rect(center = [750, 550])
        speed_down_value = font_nano.render(str(tools[3]), True, [0, 0, 255])
        speed_down_value_Rect = speed_down_value.get_rect(center = [765, 535]) 
        
        # Bars
        lifebar = pygame.image.load(lifebar_list[life_total]).convert_alpha()
        lifebar.set_colorkey([255, 255, 255], RLEACCEL)
        lifebar_rect = lifebar.get_rect(center = [700, 30])
        life_text = font_nano.render("Life", True, [255, 255, 255])
        life_text_Rect = life_text.get_rect(center = [650, 30])
        life_value = font_nano.render("{}/8".format(str(life_total)), True, [255, 255, 255])
        life_value_Rect = life_value.get_rect(center = [760, 30])
        
        tmp = level
        level = int((20 * exp_total + 25) ** 0.5 / 10 - 0.5) + 1
        if level > tmp:
            tools[random.randint(0, 3)] += random.randint(0, 1) 
        exp_level = exp_total - exp_requirement(level - 1)
        expbar_value = int(round(exp_level / (level * 10) * 8 + 0.5))
        expbar = pygame.image.load(expbar_list[expbar_value]).convert_alpha()
        expbar.set_colorkey([255, 255, 255], RLEACCEL)
        expbar_rect = expbar.get_rect(center = [700, 50])
        exp_text = font_nano.render("EXP", True, [255, 255, 255])
        exp_text_Rect = exp_text.get_rect(center = [650, 50])
        exp_value = font_nano.render("{}/{}".format(str(exp_total), str(exp_requirement(level))), True, [255, 255, 255])
        exp_value_Rect = exp_value.get_rect(center = [760, 50])
        
        powerbar = pygame.image.load(powerbar_list[shot_total]).convert_alpha()
        powerbar.set_colorkey([255, 255, 255], RLEACCEL)
        powerbar_rect = powerbar.get_rect(center = [80, 30])
        power_text = font_nano.render("Shot", True, [255, 255, 255])
        power_text_Rect = power_text.get_rect(center = [30, 30])
        power_value = font_nano.render("{}/8".format(str(shot_total)), True, [255, 255, 255])
        power_value_Rect = power_value.get_rect(center = [130, 30])
        
        cdbar = pygame.image.load(cdbar_list[int(cdbar_value)]).convert_alpha()
        cdbar.set_colorkey([255, 255, 255], RLEACCEL)
        cdbar_rect = cdbar.get_rect(center = [80, 50])
        cd_text = font_nano.render("CD", True, [255, 255, 255])
        cd_text_Rect = cd_text.get_rect(center = [30, 50])
        cd_value = font_nano.render("{}s".format(str(int(cdtext_value))), True, [255, 255, 255])
        cd_value_Rect = cd_value.get_rect(center = [130, 50])
        
        # Display
        Background = pygame.image.load(BackgroundList[background + 1]).convert()
        screen.blit(Background, (0, 0))
        screen.blit(display_level, display_level_Rect)
        screen.blit(display_level_value, display_level_value_Rect)
        screen.blit(hit_no, hit_no_Rect)
        screen.blit(hit_no_value, hit_no_value_Rect)
        screen.blit(lifebar, lifebar_rect)
        screen.blit(life_text, life_text_Rect)
        screen.blit(life_value, life_value_Rect)
        screen.blit(expbar, expbar_rect)
        screen.blit(exp_text, exp_text_Rect)
        screen.blit(exp_value, exp_value_Rect)
        screen.blit(powerbar, powerbar_rect)
        screen.blit(power_text, power_text_Rect)
        screen.blit(power_value, power_value_Rect)
        screen.blit(cdbar, cdbar_rect)
        screen.blit(cd_text, cd_text_Rect)
        screen.blit(cd_value, cd_value_Rect)
        screen.blit(extra_shot, extra_shot_rect)
        screen.blit(extra_shot_value, extra_shot_value_Rect)
        screen.blit(clear, clear_rect)
        screen.blit(clear_value, clear_value_Rect)
        screen.blit(health, health_rect)
        screen.blit(health_value, health_value_Rect)
        screen.blit(speed_down, speed_down_rect)
        screen.blit(speed_down_value, speed_down_value_Rect)
        
        # Collision Detecting
        if pygame.sprite.spritecollideany(player, enemies):
            hit = pygame.sprite.spritecollide(player, enemies, True)
            explosion_sound.play()
            new_explosion = Explosion_Player()
            explosions.add(new_explosion)
            all_sprites.add(new_explosion)
            life_total -= 3
            if life_total <= 0:
                if tools[2] >= 1:
                    tools[2] -= 1
                    life_total = 8
                else:
                    pygame.mixer.music.stop()
                    gameover_sound.play()
                    player.kill()
                    data.saverecord(username, difficulty, level, exp_total)
                    running = False
                    launcher.main_menu(True,"over")
                
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        enemies.update()
        clouds.update()
        explosions.update()
    
pygame.quit()
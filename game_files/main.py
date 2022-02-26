import pygame
from sys import exit


def display_score():
    current_time = pygame.time.get_ticks() - start_time
    score = current_time // 1000
    score_surf = text_font.render(f'score: {score}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return score


pygame.init()
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pixel Runner')
text_font = pygame.font.Font('game_files/font/Pixeltype.ttf', 36)
clock = pygame.time.Clock()
FPS = 60
start_time = 0
game_active = False

text_surf = text_font.render('Press space to restart', False, (64, 64, 64))
sky_surf = pygame.image.load('game_files/graphics/Sky.png').convert()
ground_surf = pygame.image.load('game_files/graphics/ground.png').convert()

snail_surf = pygame.image.load('game_files/graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(midbottom=(500, 300))
snail_speed = 4

player_surf = pygame.image.load('game_files/graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom=(80, 300))
player_gravity = 0
score = 0

#  Intro screen
player_stand_surf = pygame.image.load('game_files/graphics/Player/player_stand.png').convert_alpha()
player_stand_surf = pygame.transform.rotozoom(player_stand_surf, 0, 2)
player_stand_rect = player_stand_surf.get_rect(center=(WIDTH//2, HEIGHT//2))
game_name_surf = text_font.render('Pixel Runner', False, (111, 196, 169))
game_name_rect = game_name_surf.get_rect(center=(400, 50))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom >= 300:
                if player_rect.collidepoint(event.pos):
                    player_gravity = -20
            if event.type == pygame.KEYDOWN and player_rect.bottom >= 300:
                player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                snail_rect.left = WIDTH
                game_active = True
                start_time = pygame.time.get_ticks()

    if game_active:
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 300))
        score = display_score()

        #  Snail
        snail_rect.left -= snail_speed + score
        if snail_rect.right < 0:
            snail_rect.left = WIDTH
        screen.blit(snail_surf, snail_rect)

        #  Player
        player_gravity += 1
        player_rect.bottom += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        screen.blit(player_surf, player_rect)

        #  Collision (lose condition)
        if snail_rect.colliderect(player_rect):
            game_active = False
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand_surf, player_stand_rect)
        screen.blit(text_surf, (WIDTH//3, HEIGHT-80))
        score_surf = text_font.render(f'your score: {score}', False, (64, 64, 64))
        screen.blit(score_surf, (WIDTH//3+50, 80))
        screen.blit(game_name_surf, game_name_rect)
    pygame.display.update()
    clock.tick(FPS)

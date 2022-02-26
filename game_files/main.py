import pygame
from random import randint, choice
from sys import exit


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('game_files/graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('game_files/graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('game_files/graphics/Player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('game_files/audio/jump.mp3')
        self.jump_sound.set_volume(0.15)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.jump_sound.play()
            self.gravity = -20
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left >= 0:
            self.rect.left -= 3
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right <= 0.6*WIDTH:
            self.rect.left += 3             

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_frame_1 = pygame.image.load('game_files/graphics/fly/fly1.png').convert_alpha()
            fly_frame_2 = pygame.image.load('game_files/graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_frame_1, fly_frame_2]
            y_pos = 210
        elif type == 'snail':
            snail_frame_1 = pygame.image.load('game_files/graphics/snail/snail1.png').convert_alpha()
            snail_frame_2 = pygame.image.load('game_files/graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame_1, snail_frame_2]
            y_pos = 300
        
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1200), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 5
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    current_time = pygame.time.get_ticks() - start_time
    score = current_time // 1000
    score_surf = text_font.render(f'score: {score}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return score


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    return True


pygame.init()
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pixel Runner')
text_font = pygame.font.Font('game_files/font/Pixeltype.ttf', 36)
clock = pygame.time.Clock()
FPS = 60
start_time = 0
score = 0
game_active = False
bg_music = pygame.mixer.Sound('game_files/audio/music.wav')
bg_music.play(loops=-1)
bg_music.set_volume(0.25)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

#  Textures
sky_surf = pygame.image.load('game_files/graphics/Sky.png').convert()
ground_surf = pygame.image.load('game_files/graphics/ground.png').convert()

#  Intro screen
text_surf = text_font.render('Press space to run', False, (64, 64, 64))
text_rect = text_surf.get_rect(center=(WIDTH//2, HEIGHT-80))
player_stand_surf = pygame.image.load('game_files/graphics/Player/player_stand.png').convert_alpha()
player_stand_surf = pygame.transform.rotozoom(player_stand_surf, 0, 2)
player_stand_rect = player_stand_surf.get_rect(center=(WIDTH//2, HEIGHT//2))
game_name_surf = text_font.render('Pixel Runner', False, (111, 196, 169))
game_name_rect = game_name_surf.get_rect(center=(400, 50))

#  Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail'])))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()

    if game_active:
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 300))
        score = display_score()
        player.draw(screen)
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()
        game_active = collision_sprite()
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand_surf, player_stand_rect)
        screen.blit(text_surf, text_rect)
        if score != 0:
            score_surf = text_font.render(f'your score: {score}', False, (64, 64, 64))
            score_rect = score_surf.get_rect(center=(WIDTH//2, 80))
            screen.blit(score_surf, score_rect)
        screen.blit(game_name_surf, game_name_rect)

    pygame.display.update()
    clock.tick(FPS)

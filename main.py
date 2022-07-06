import pygame
from sys import exit
from random import randint

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        pablo_walk_1 = pygame.image.load("graphics/rightlegblo.png").convert_alpha()
        pablo_walk_2 = pygame.image.load("graphics/leftlegblo.png").convert_alpha()
        self.pablo_jump = pygame.image.load("graphics/jublo.png").convert_alpha()
        self.pablo_walk = [pablo_walk_1, pablo_walk_2]
        self.pablo_index = 0

        self.image = self.pablo_walk[self.pablo_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0


    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20

    def apply_gravity(self):
        self.gravity  += 1
        self.rect.y += self.gravity
        if self.rect.bottom > 300: self.rect.bottom = 300

    def pablimation(self):
        if self.rect.bottom < 300: self.image = self.pablo_jump
        else:
            self.pablo_index += 0.1
            if self.pablo_index >= len(self.pablo_walk): self.pablo_index = 0
            self.image = self.pablo_walk[int(self.pablo_index)]


    def update(self):
        self.player_input()
        self.apply_gravity()
        self.pablimation()



class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        snail_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
        snail_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()

        fly_1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
        fly_2 = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()

        self.index = 0

        if type == 1:
            self.walk = [snail_1, snail_2]
            self.image = self.walk[self.index]
            self.rect = self.image.get_rect(bottomleft=(randint(850, 1200), 300))
        else:
            self.walk = [fly_1, fly_2]
            self.image = self.walk[self.index]
            self.rect = self.image.get_rect(bottomleft=(randint(850, 1200), 200))

    def animation(self):
        self.index += 0.1
        if self.index >= len(self.walk): self.index = 0
        self.image = self.walk[int(self.index)]

    def update(self):
        self.animation()
        self.rect.x -= 5
        if self.rect.x <= -50:
            self.kill()



active = False
score_count = 0
stat_time = 0


def display_score():
    global score_count
    curr_time = pygame.time.get_ticks() - stat_time
    score_count = round(curr_time/1000)
    score = test_font.render(f"Score: {score_count}", False, "Black")
    score_rec = score.get_rect(topleft=(20, 10))
    pygame.draw.rect(screen, "Pink", score_rec)
    pygame.draw.rect(screen, "Pink", score_rec, 15)
    screen.blit(score, score_rec)



def collision(player, obstacle_list):
    if obstacle_list:
        for obst in obstacle_list:
            if player.colliderect(obst):
                return False
            else:
                return True
    return True



def sprite_coll():
    if pygame.sprite.spritecollide(player.sprite, obstacles, False):
        obstacles.empty()
        return False
    return True



pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Super Pablo Bros.")
clock = pygame.time.Clock()
test_font = pygame.font.Font("font/Pixeltype.ttf", 23)
Big_font = pygame.font.Font("font/Pixeltype.ttf", 40)
name_font = pygame.font.Font("font/Pixeltype.ttf", 75)

player = pygame.sprite.GroupSingle()
player.add(Player())

obstacles = pygame.sprite.Group()


Sky = pygame.image.load("graphics/Sky.png").convert_alpha()
ground = pygame.image.load("graphics/ground.png").convert_alpha()

pablo_to_scale = pygame.image.load("graphics/superpablo.png").convert_alpha()
pablo_scaled = pygame.transform.scale(pablo_to_scale, (200, 320))
pablo_scaled_rec = pablo_scaled.get_rect(center=(475, 160))

text = test_font.render("Pablo's brother has been transformed into lizard by evil witch and now it's his turn to save his bruther.", False, "Black")
text_rec = text.get_rect(center=(400, 50))

score = test_font.render(f"Score: {score_count}", False, "Black")
score_rec = score.get_rect(topleft=(20, 10))

restart_text = Big_font.render("Pedro needs help press space to start.", False, "Black")
restart_text_rec = restart_text.get_rect(center=(400, 350))

game_name = name_font.render("Super Pablo Bros", False, "Black")
game_name_rec = game_name.get_rect(midleft=(20, 200))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1250)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if active:
            if event.type == obstacle_timer:
                obstacles.add(Obstacle(randint(0, 2)))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                active = True
                stat_time = pygame.time.get_ticks()

    if active:
        screen.blit(Sky, (0, 0))
        screen.blit(ground, (0, 300))
        player.draw(screen)
        player.update()
        obstacles.draw(screen)
        obstacles.update()
        screen.blit(text, text_rec)
        display_score()
        active = sprite_coll()
    else:
        screen.fill("Red")
        screen.blit(pablo_scaled, pablo_scaled_rec)
        score_text = Big_font.render(f"Score: {score_count}", False, "Black")
        score_text_rec = score_text.get_rect(center=(400, 350))
        if score_count == 0:
            screen.blit(restart_text, restart_text_rec)
        else:
            screen.blit(score_text, score_text_rec)
        screen.blit(game_name, game_name_rec)


    pygame.display.update()

    clock.tick(60)

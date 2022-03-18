import pygame
from pygame.locals import *
import sys
import random


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        for i in range(1, 8):
            image = pygame.image.load(f"sprites/character/idle{i}.png")
            self.sprites.append(image)
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

        # movement
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0
        self.movey = 0
        self.frame = 0

    def update(self):
        self.current_sprite += 0.3
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey

    def control(self, x, y):
        self.movex += x
        self.movey += y

    def fire(self, k, m):
        return Bullet(self.rect.left + 15 + k, self.rect.top + -10 + m)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        image = pygame.image.load(f"sprites/projectiles/knife1.png")
        self.image = image
        self.rect = self.image.get_rect(center=(pos_x, pos_y))

    def update(self):
        self.rect.y += -20

        if self.rect.y > window_height + 300:
            self.kill()


class Menu(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        image = pygame.image.load(f"sprites/menu/menu.png")
        self.image = image
        self.rect = self.image.get_rect(center=(pos_x, pos_y))

    def update(self):
        self.health()

    def health(self):
        for n in range(playerHp):
            pygame.draw.rect(window, (255, 0, 0), (508 + n * 25, 212, 10, 10))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        for i in range(1, 8):
            image = pygame.image.load(f"sprites/enemy/idle{i}.png")
            self.sprites.append(image)
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
        self.enemyHp = 10
        self.movex = 0
        self.movey = 1
        self.spawnPos = self.rect.x

    def update(self):
        # Sprite stuff
        self.current_sprite += 0.3
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]

        # movement stuff
        if self.spawnPos <= window_width / 2:
            self.movex = 1
        else:
            self.movex = -1
        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey

        # death stuff
        if self.enemyHp <= 0 or self.rect.x > window_height + 50:
            self.kill()

    def powerupdrop(self):
        return PowerUp(self.rect.left, self.rect.top)

    def fire(self, pos_x, pos_y):
        return EnemyProjectile(self.rect.left + pos_x, self.rect.top + pos_y)


class EnemyProjectile(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        image = pygame.image.load(f"sprites/projectiles/enemyProjectile.png")
        self.image = image
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.startx = self.rect.x
        self.starty = self.rect.y
        self.destx = player.rect.x
        self.desty = player.rect.y
        self.bulletvelocity = 0.001
        self.deltax = self.destx - self.startx
        self.deltay = self.desty - self.starty

    def update(self):
        self.rect.x = self.rect.x + self.deltax * 0.01
        self.rect.y = self.rect.y + self.deltay * 0.01
        if self.rect.y >= window_height:
            self.kill()
            print("success")


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        image = pygame.image.load(f"sprites/items/power.png")
        self.image = image
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.movey = 1

    def update(self):
        # gravity stuff
        self.movey += 0.1
        self.rect.y = self.rect.y + self.movey
        if self.rect.y >= window_height:
            self.kill()


# general
pygame.init()
clock = pygame.time.Clock()
previous_time = pygame.time.get_ticks()
previous_time2 = pygame.time.get_ticks()
previous_time3 = pygame.time.get_ticks()
velocity = 10
playerHp = 5
power = 1
score = 0
isInvulnerable = False
font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surf.blit(text_surface, text_rect)


# window
window_width = 650
window_height = 700
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Touhou")
bg = pygame.image.load("sprites/background/bg.jpg")
moving_sprites = pygame.sprite.Group()
player = Player(200, 500)
menu = Menu(550, 350)
menug = pygame.sprite.Group()
moving_sprites.add(player)
menug.add(menu)
powerup_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemyProjectile_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
while True:
    enemy = Enemy(random.randint(-50, 450), random.randint(-50, 200))
    current_time = pygame.time.get_ticks()
    current_time2 = pygame.time.get_ticks()
    current_time3 = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.control(-velocity, 0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.control(velocity, 0)
            if event.key == pygame.K_UP or event.key == ord('w'):
                player.control(0, -velocity)
            if (event.key == pygame.K_DOWN or event.key == ord('s')):
                player.control(0, velocity)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.control(velocity, 0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.control(-velocity, 0)
            if event.key == pygame.K_UP or event.key == ord('w'):
                player.control(0, velocity)
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                player.control(0, -velocity)
    key = pygame.key.get_pressed()
    if key[K_SPACE]:
        if current_time - previous_time > 50:
            previous_time = current_time
            if power <= 4:
                bullet_group.add(player.fire(0, 0))
            if power >= 5:
                bullet_group.add(player.fire(0, 0))
                bullet_group.add(player.fire(10, 0))
                bullet_group.add(player.fire(-10, 0))
    if random.randrange(0, 100) < 2:
        enemy_group.add(enemy)
        if random.randrange(0, 100) < 25:
            enemyProjectile_group.add(enemy.fire(0, 0))
            enemyProjectile_group.add(enemy.fire(15, 0))
            enemyProjectile_group.add(enemy.fire(-15, 0))
        else:
            enemyProjectile_group.add(enemy.fire(0, 0))

    for enemy in enemy_group:
        gets_hit = pygame.sprite.spritecollideany(enemy, bullet_group)
        if gets_hit:
            # power cap
            if power < 10:
                enemy.enemyHp -= power * 0.4
            if power >= 10:
                enemy.enemyHp -= 4
            if enemy.enemyHp <= 0:
                score += 125
                if random.randrange(0, 100) < 50:
                    powerup_group.add(enemy.powerupdrop())
            for bullet in bullet_group:
                if pygame.Rect.colliderect(bullet.rect, enemy.rect):
                    bullet.kill()
    if pygame.sprite.spritecollideany(player, powerup_group):
        power += 1
        score += 50
        for powerup in powerup_group:
            if pygame.Rect.colliderect(powerup.rect, player.rect):
                powerup.kill()
    if pygame.sprite.spritecollideany(player, enemyProjectile_group) and isInvulnerable == False:
        playerHp -= 1
        if playerHp == 0:
            pygame.quit()
            sys.exit()
        for enemyprojectile in enemyProjectile_group:
            if pygame.Rect.colliderect(enemyprojectile.rect, player.rect):
                enemyprojectile.kill()



    window.blit(bg, (0, 0))
    bullet_group.draw(window)
    bullet_group.update()
    moving_sprites.draw(window)
    moving_sprites.update()
    enemy_group.draw(window)
    enemy_group.update()
    enemyProjectile_group.draw(window)
    enemyProjectile_group.update()
    powerup_group.draw(window)
    powerup_group.update()
    menug.draw(window)
    menug.update()
    draw_text(window, str(score), 18, 515, 188)
    pygame.display.flip()
    clock.tick(60)

import pygame
import sys

# pixel variables
WIN_WIDTH = 640
WIN_HEIGHT = 360
ON_BASE = 96
TILE_SIZE = 32
VEL = 5

BASE_IMG = pygame.image.load('images/tile.png')
BG_IMG = pygame.image.load('images/sunset_bg.jpg')
BG_IMG = pygame.transform.scale(BG_IMG, (WIN_WIDTH, WIN_HEIGHT))
ICON = pygame.image.load('images/pango_saint.jpg')
END_GAME = pygame.image.load('images/pango_saint.jpg')
END_GAME = pygame.transform.scale(END_GAME, (640, 360))

PANGO_AVATAR = pygame.image.load('images/pango_avatar.png')
COVID_AVATAR = pygame.image.load('images/covid_avatar.png')

FULL_LIFE = pygame.image.load('images/life.png')
HALF_LIFE = pygame.image.load('images/half_life.png')

PANGO_JUMP_IMG = pygame.image.load('images/pango_jump.png')
PANGO_GREEN_JUMP_IMG = pygame.image.load('images/pango_green_jump.png')

PANGO_STILL_RIGHT_IMG = [pygame.image.load('images/pango_still_right_1.png'),
                         pygame.image.load('images/pango_still_right_2.png')]
PANGO_STILL_LEFT_IMG = [pygame.image.load('images/pango_still_left_1.png'),
                        pygame.image.load('images/pango_still_left_2.png')]

PANGO_GREEN_STILL_RIGHT_IMG = [pygame.image.load('images/pango_green_still_right_1.png'),
                               pygame.image.load('images/pango_green_still_right_2.png')]
PANGO_GREEN_STILL_LEFT_IMG = [pygame.image.load('images/pango_green_still_left_1.png'),
                              pygame.image.load('images/pango_green_still_left_2.png')]

PANGO_SPIN_IMG = [pygame.image.load('images/pango_spin_1.png'), pygame.image.load('images/pango_spin_2.png'),
                  pygame.image.load('images/pango_spin_3.png'), pygame.image.load('images/pango_spin_4.png')]

PANGO_GREEN_SPIN_IMG = [pygame.image.load('images/pango_green_spin_1.png'),
                        pygame.image.load('images/pango_green_spin_2.png'),
                        pygame.image.load('images/pango_green_spin_3.png'),
                        pygame.image.load('images/pango_green_spin_4.png')]

PANGO_ATTACK_RIGHT = [pygame.image.load('images/pango_attack_right_1.png'),
                      pygame.image.load('images/tongue_1.png'),
                      pygame.image.load('images/tongue_2.png'),
                      pygame.image.load('images/tongue_3.png')]
PANGO_ATTACK_LEFT = [pygame.image.load('images/pango_attack_left_1.png'),
                     pygame.transform.rotate(PANGO_ATTACK_RIGHT[1], 180),
                     pygame.transform.rotate(PANGO_ATTACK_RIGHT[2], 180),
                     pygame.transform.rotate(PANGO_ATTACK_RIGHT[3], 180)]

PANGO_GREEN_ATTACK_RIGHT = [pygame.image.load('images/pango_green_attack_right_1.png'),
                            pygame.image.load('images/tongue_1.png'),
                            pygame.image.load('images/tongue_2.png'),
                            pygame.image.load('images/tongue_3.png')]

PANGO_GREEN_ATTACK_LEFT = [pygame.image.load('images/pango_green_attack_left_1.png'),
                           pygame.transform.rotate(PANGO_ATTACK_RIGHT[1], 180),
                           pygame.transform.rotate(PANGO_ATTACK_RIGHT[2], 180),
                           pygame.transform.rotate(PANGO_ATTACK_RIGHT[3], 180)]
COVID_IMG = [pygame.image.load('images/covid_aura_left.png'), pygame.image.load('images/covid_aura_right.png')]


def draw_avatars():
    win.blit(PANGO_AVATAR, (0, 0))
    if covid_lives > 0:
        win.blit(COVID_AVATAR, (640-16, 0))


def draw_lives():
    if pango_green:
        win.blit(HALF_LIFE, (0+16, 0))
    else:
        win.blit(FULL_LIFE, (0 + 16, 0))
    if covid_lives == 2:
        win.blit(FULL_LIFE, (640 - 32, 0))
    elif covid_lives == 1:
        win.blit(HALF_LIFE, (640 - 32, 0))


def draw_covid():
    global pango_x
    global covid_x
    global covid_y

    if pango_x > covid_x:
        enemy = COVID_IMG[1]
    else:
        enemy = COVID_IMG[0]
    win.blit(enemy, (covid_x, covid_y))


def draw_pango_still():
    global pango_green
    global pango_looking_right
    global pango_x
    global pango_still_idx
    global still_count
    global pango_still

    if not pango_attacking:
        still_count += 1
        if not pango_green:
            if pango_looking_right:
                imgs = PANGO_STILL_RIGHT_IMG
            else:
                imgs = PANGO_STILL_LEFT_IMG
        else:
            if pango_looking_right:
                imgs = PANGO_GREEN_STILL_RIGHT_IMG
            else:
                imgs = PANGO_GREEN_STILL_LEFT_IMG
        if still_count > 60:
            if pango_still_idx == 0:
                pango_still_idx = 1
                still_count = 0
            else:
                pango_still_idx = 0
                still_count = 0

        pango = imgs[pango_still_idx]
        win.blit(pango, (pango_x, pango_y))
        draw_pango_still.hitbox = (pango_x + 1, pango_y + 1, 60, 64)
        pygame.draw.rect(win, (255, 0, 0), draw_pango_still.hitbox, 2)


def draw_tiles(x, y):
    win.blit(BASE_IMG, (x, y))


def draw_map(list_of_cords):
    for tile_location in list_of_cords:
        draw_tiles(tile_location[0], tile_location[1])


def draw_pango_spin():
    global pango_green
    global pango_moving_right
    global pango_moving_left
    global spin_count
    global pango_x
    global pango_y
    global pango_spin_idx

    if pango_moving_right or pango_moving_left:
        if pango_green:
            img = PANGO_GREEN_SPIN_IMG
        else:
            img = PANGO_SPIN_IMG
        if pango_moving_left:
            if pango_green:
                img = list(reversed(PANGO_GREEN_SPIN_IMG))
            else:
                img = list(reversed(PANGO_SPIN_IMG))
        if spin_count < 5:
            pango_spin_idx = 0
        elif spin_count % 10 == 0:
            pango_spin_idx = 1
        elif spin_count % 15 == 0:
            pango_spin_idx = 2
        elif spin_count % 20 == 0:
            pango_spin_idx = 3
        elif spin_count % 30 == 0:
            pango_spin_idx = 0
        elif spin_count % 40 == 0:
            pango_spin_idx = 1
        pango = img[pango_spin_idx]
        win.blit(pango, (pango_x, pango_y))
        draw_pango_spin.hitbox = (pango_x + 11, pango_y + 15, 44, 48)
        pygame.draw.rect(win, (255, 0, 0), draw_pango_spin.hitbox, 2)


def pango_spin():
    global pango_moving_right
    global pango_moving_left
    global pango_looking_right
    global pango_moving_left
    global pango_y
    global pango_x
    global spin_count
    global pango_vel
    global pango_still

    if (pango_moving_left or pango_moving_right) and not pango_still:
        pango_vel += 0.5 * 1.2
        if pango_vel >= 16:
            pango_vel = 16
        if pango_moving_right:
            pango_x = pango_x + pango_vel
        else:
            pango_x = pango_x - pango_vel

        if pango_x >= 583:
            pango_x = 583
        if pango_moving_left and pango_x <= 0:
            pango_x = -10
        if pango_x > covid_x:
            pango_looking_right = False
        else:
            pango_looking_right = True
        spin_count += 1
        if spin_count >= 40:
            pango_still = True
            pango_moving_right = False
            pango_moving_left = False
            spin_count = 0
    else:
        pango_vel = 1.5
        spin_count = 0


def pango_jump():
    global pango_y
    global pango_jumping
    global jump_count

    if pango_jumping:
        if jump_count >= -10:

            pango_y -= abs(jump_count) * jump_count * 0.3
            jump_count -= 1
        else:

            pango_jumping = False
            jump_count = 10


def draw_pango_jump():
    global pango_looking_right
    global pango_green
    global pango_x
    global pango_y
    global pango_attacking

    # if not (pango_moving_left or pango_moving_right):
    if pango_looking_right:
        if not pango_green:
            img = PANGO_JUMP_IMG
        else:
            img = PANGO_GREEN_JUMP_IMG
    else:
        if not pango_green:
            img = PANGO_JUMP_IMG
            img = pygame.transform.flip(img, True, False)
        else:
            img = PANGO_GREEN_JUMP_IMG
            img = pygame.transform.flip(img, True, False)

    if pango_attacking:
        try:
            draw_pango_attack.pang_img
        except:
            img = PANGO_ATTACK_RIGHT[0]
    win.blit(img, (pango_x, pango_y))


def draw_pango_attack():
    global pango_green
    global pango_looking_right
    global pango_attacking
    global pango_jumping
    global pango_moving_left
    global pango_moving_right

    if not pango_green:
        if pango_looking_right:

            pang_img = PANGO_ATTACK_RIGHT[0]
            tongue_img = PANGO_ATTACK_RIGHT[1:]
        else:
            pang_img = PANGO_ATTACK_LEFT[0]
            tongue_img = PANGO_ATTACK_LEFT[1:]
            tongue_img = tongue_img[::-1]
    else:
        if pango_looking_right:

            pang_img = PANGO_GREEN_ATTACK_RIGHT[0]
            tongue_img = PANGO_GREEN_ATTACK_RIGHT[1:]
        else:
            pang_img = PANGO_GREEN_ATTACK_LEFT[0]
            tongue_img = PANGO_GREEN_ATTACK_LEFT[1:]
            tongue_img = tongue_img[::-1]
    if not pango_jumping:
        win.blit(pang_img, (pango_x, pango_y))
        pango_moving_left = False
        pango_moving_right = False
    draw_pango_attack.pang_img = pang_img
    draw_tongue(tongue_img)


def draw_tongue(img):
    global tongue_y
    global tongue_x
    global x_adj
    global y_adj
    global pango_y
    global pango_x
    global attack_count
    global pango_attacking
    global tongue_len
    global pango_looking_right
    global pango_still
    speed = 2
    if pango_looking_right:
        tongue_y = pango_y + y_adj
        tongue_x = pango_x + x_adj
        win.blit(img[0], (tongue_x, tongue_y))

        for k in range(1, tongue_len):
            win.blit(img[1], ((16 * k) + tongue_x, tongue_y))
        win.blit(img[-1], ((16 * tongue_len) + tongue_x, tongue_y))
        if pango_attacking:
            if attack_count >= -15:
                tongue_x += speed * 2
                attack_count -= 1
            else:
                pango_attacking = False
                attack_count = 15
                tongue_x = pango_x
                tongue_y = pango_y
    else:
        tongue_y = pango_y + y_adj
        tongue_x = pango_x + 9
        win.blit(img[0], ((-16 * tongue_len) + tongue_x, tongue_y))  # last image
        for k in range(1, tongue_len):
            win.blit(img[1], ((-16 * k) + tongue_x, tongue_y))
        win.blit(img[-1], (tongue_x, tongue_y))
        if pango_attacking:
            if attack_count >= -15:
                tongue_x += speed * 2
                attack_count -= 1
                # draw_tongue.hitbox = (tongue_x - 3 + (-16 * tongue_len), tongue_y, 16, 16)
                # pygame.draw.rect(win, (255, 0, 0), draw_tongue.hitbox, 2)
            else:
                pango_attacking = False
                attack_count = 15
                tongue_x = pango_x
                tongue_y = pango_y
    draw_tongue.rect = pygame.Rect(tongue_x, tongue_y, 16, 16)

    if pango_still:
        pango_attacking = False
        attack_count = 15
        tongue_x = pango_x
        tongue_y = pango_y


def enemy_collision():
    global lost
    global pango_green
    global pango_hit_once
    global covid_x
    global covid_y
    global pango_y
    global pango_x
    if pango_x > covid_x:
        adj = +20
    else:
        adj = -20
    pango_rect = pygame.Rect(pango_x + 2 * adj, pango_y, 64, 64)
    if move_towards_pango.rect.colliderect(pango_rect) == 1:
        if not pango_hit_once:
            covid_x = 640 - 32
            covid_y = 0 + 32
            pango_hit_once = True
            pango_green = True
        else:
            lost = True


def tongue_collision():
    global tongue_x
    global tongue_y
    global covid_x
    global covid_y
    global covid_speed
    global covid_hit_count
    global pango_x
    global covid_hit
    global covid_lives

    tongue_collision.rect = pygame.Rect(tongue_x, tongue_y, 16, 16)

    if pango_attacking:
        if not covid_hit:
            if tongue_collision.rect.colliderect(move_towards_pango.rect):
                covid_hit = True
                covid_lives -= 1

        else:
            if covid_hit_count >= 0:
                if pango_x < covid_x:
                    covid_x += covid_hit_count + 5
                else:
                    covid_x -= covid_hit_count + 5
                if covid_speed > 0:
                    covid_speed -= 0.3
                else:
                    covid_speed = 0.5
                covid_hit_count -= 2

            else:
                covid_hit_count = 20
                covid_speed = 1.5
                covid_hit = False


def move_towards_pango():
    global pango_x
    global pango_y
    global covid_x
    global covid_y
    global covid_speed
    global min_dist
    global covid_moving

    delta_x = pango_x - covid_x
    delta_y = pango_y - covid_y

    if abs(delta_x) <= min_dist and abs(delta_y) <= min_dist:
        covid_moving = True
    if covid_moving:
        covid_x += min(delta_x, covid_speed) if delta_x > 0 else max(delta_x, -covid_speed)
        covid_y += min(delta_y, covid_speed) if delta_y > 0 else max(delta_y, -covid_speed)
    if covid_lives > 0:
        move_towards_pango.rect = pygame.Rect(covid_x, covid_y, 64, 64)
    else:
        move_towards_pango.rect = pygame.Rect(-20, -20, 64, 64)
    # move_towards_pango.hitbox = (covid_x + 5, covid_y, 55, 64)


def redraw_game_window():
    win.blit(BG_IMG, (0, 0))
    draw_map(tile_cords)
    draw_avatars()
    if not pango_jumping and not pango_moving_right and not pango_moving_left:
        draw_pango_still()
    elif pango_still:
        draw_pango_still()
    elif pango_moving_left or pango_moving_right:
        draw_pango_spin()
    elif pango_jumping:
        draw_pango_jump()
    if pango_attacking:
        draw_pango_attack()
    if covid_lives > 0:
        draw_covid()
    draw_lives()
    pygame.display.update()


# pango init variables
pango_x = TILE_SIZE
pango_y = WIN_HEIGHT - ON_BASE
pango_still = True
pango_jumping = False
pango_moving_right = False
pango_moving_left = False
pango_looking_right = True
jump_count = 10
spin_count = 0
pango_vel = 1.5
still_count = 0
pango_still_idx = 0
pango_green = False
pango_spin_idx = 0
pango_attacking = False
lost = False
attack_count = 15
x_adj = 38
y_adj = 34

tongue_len = 5
pango_hit_once = False

# map variables
tile_cords = [(n, WIN_HEIGHT - TILE_SIZE) for n in range(0, 640) if n % TILE_SIZE == 0]

# enemy variables
covid_x = WIN_WIDTH - TILE_SIZE * 4
covid_y = 0
covid_speed = 1.5
min_dist = 200
covid_moving = False
covid_hit = False
covid_hit_count = 20
covid_lives = 2

# game variables
pygame.init()
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            pango_moving_left = True
            pango_moving_right = False
            pango_still = False

        if keys[pygame.K_RIGHT]:
            pango_moving_left = False
            pango_moving_right = True
            pango_still = False

        if not pango_jumping:
            if keys[pygame.K_UP]:
                pango_jumping = True
                pango_still = False
            # else:
            #     pango_still = True
        if keys[pygame.K_SPACE]:
            pango_attacking = True
            pango_still = False
        else:
            tongue_x = pango_x
            tongue_y = pango_y

    if not lost:
        pango_jump()
        pango_spin()
        move_towards_pango()
        enemy_collision()

        tongue_collision()
        redraw_game_window()
    else:
        print('lost')
        running = False

# TODO: fix bug with covid_speed after tongue_collision
# covid_speed changes even without collision
# covid_speed drops to negative and stays there

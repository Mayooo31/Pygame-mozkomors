import random

import pygame

# Init
pygame.init()

# Display
width = 1200
height = 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bitva s mozkomory")

# FPS and clock
fps = 60
clock = pygame.time.Clock()


# Classes
class Game:
    def __init__(self, our_player, group_of_mozkomors):
        self.score = 0
        self.round_number = 0

        self.round_time = 0
        self.slow_down_cycle = 0

        self.our_player = our_player
        self.group_of_mozkomors = group_of_mozkomors

        # Music in background
        pygame.mixer.music.load("media/bg-music-hp.mp3")
        pygame.mixer.music.play(-1, 0.0)

        # Fonts
        self.potter_font = pygame.font.Font("fonts/Harry.ttf", 24)
        self.potter_font_big = pygame.font.Font("fonts/Harry.ttf", 48)

        # Background
        self.background_image = pygame.image.load("img/bg-dementors.png")
        self.background_image_rect = self.background_image.get_rect()
        self.background_image_rect.topleft = (0, 0)

        # Images
        blue_image = pygame.image.load("img/mozkomor-modry.png")
        green_image = pygame.image.load("img/mozkomor-zeleny.png")
        purple_image = pygame.image.load("img/mozkomor-ruzovy.png")
        yellow_image = pygame.image.load("img/mozkomor-zluty.png")
        # ---
        self.mozkomors_images = [blue_image, green_image, purple_image, yellow_image]

        # generating Mozkomor that we want to catch...
        self.mozkomor_catch_type = random.randint(0, 3)
        self.mozkomor_catch_image = self.mozkomors_images[self.mozkomor_catch_type]

        self.mozkomor_catch_image_rect = self.mozkomor_catch_image.get_rect()
        self.mozkomor_catch_image_rect.centerx = width // 2
        self.mozkomor_catch_image_rect.top = 25

    def update(self):
        self.slow_down_cycle += 1
        if self.slow_down_cycle == fps:
            self.round_time += 1
            self.slow_down_cycle = 0

        # Check collision
        self.check_collisions()

    def draw(self):
        dark_yellow = pygame.Color("#938f0c")
        blue = (21, 31, 217)
        green = (24, 194, 38)
        purple = (195, 25, 189)
        yellow = (195, 181, 23)
        colors = [blue, green, purple, yellow]

        # Text settings
        catch_text = self.potter_font.render("Catch this Mozkomor", True, dark_yellow)
        catch_text_rect = catch_text.get_rect()
        catch_text_rect.centerx = width // 2
        catch_text_rect.top = 5

        score_text = self.potter_font.render(f"Score: {self.score}", True, dark_yellow)
        score_text_rect = score_text.get_rect()
        score_text_rect.topleft = (5, 5)

        lives_text = self.potter_font.render(f"Lives: {self.our_player.lives}", True, dark_yellow)
        lives_text_rect = lives_text.get_rect()
        lives_text_rect.topleft = (5, 30)

        round_text = self.potter_font.render(f"Round: {self.round_number}", True, dark_yellow)
        round_text_rect = round_text.get_rect()
        round_text_rect.topleft = (5, 60)

        time_text = self.potter_font.render(f"Round time: {self.round_time}", True, dark_yellow)
        time_text_rect = time_text.get_rect()
        time_text_rect.topright = (width - 5, 5)

        back_safe_zone_text = self.potter_font.render(f"Safe zone: {self.our_player.enter_safe_zone}", True, dark_yellow)
        back_safe_zone_text_rect = back_safe_zone_text.get_rect()
        back_safe_zone_text_rect.topright = (width - 5, 35)

        # Blitting
        screen.blit(catch_text, catch_text_rect)
        screen.blit(score_text, score_text_rect)
        screen.blit(lives_text, lives_text_rect)
        screen.blit(round_text, round_text_rect)
        screen.blit(time_text, time_text_rect)
        screen.blit(back_safe_zone_text, back_safe_zone_text_rect)
        screen.blit(self.mozkomor_catch_image, self.mozkomor_catch_image_rect)

        # Lines
        pygame.draw.rect(screen, colors[self.mozkomor_catch_type], (0, 100, width, height - 200), 4)

    def check_collisions(self):
        # Collision with who?
        collided_mozkomor = pygame.sprite.spritecollideany(self.our_player, self.group_of_mozkomors)

        if collided_mozkomor:
            # Did i collided with right Mozkomor?
            if collided_mozkomor.type == self.mozkomor_catch_type:
                # Play sound for catching right mozkomor
                self.our_player.catch_sound.play()
                # Increase score
                self.score += 10 * self.round_number
                # removing collided Mozkomor
                collided_mozkomor.remove(self.group_of_mozkomors)
                # Is there Mozkomors left?
                if self.group_of_mozkomors:
                    self.choose_new_target()
                else:
                    # Round is over
                    self.our_player.reset()
                    self.start_new_round()

            else:
                self.our_player.wrong_sound.play()
                self.our_player.lives -= 1
                # Did you died ? lives === 0 ?
                if self.our_player.lives <= 0:
                    self.pause_game(f"Final score {self.score}", "Click ENTER if you wanna play again.")
                    self.reset_game()
                self.our_player.reset()

    def start_new_round(self):
        # if you end round faster u will get bigger bonus
        self.score += int(100 * (self.round_number / (1 + self.round_time)))

        # Reset
        self.round_time = 0
        self.slow_down_cycle = 0
        self.round_number += 1
        self.our_player.enter_safe_zone += 1

        # clean list of mozkomors so we can add mozkomors
        for deleted_mozkomor in self.group_of_mozkomors:
            self.group_of_mozkomors.remove(deleted_mozkomor)

        for i in range(self.round_number):
            self.group_of_mozkomors.add(
                Mozkomor(random.randint(0, width - 64), random.randint(100, height - 164),
                         self.mozkomors_images[0], 0))
            self.group_of_mozkomors.add(
                Mozkomor(random.randint(0, width - 64), random.randint(100, height - 164),
                         self.mozkomors_images[1], 1))
            self.group_of_mozkomors.add(
                Mozkomor(random.randint(0, width - 64), random.randint(100, height - 164),
                         self.mozkomors_images[2], 2))
            self.group_of_mozkomors.add(
                Mozkomor(random.randint(0, width - 64), random.randint(100, height - 164),
                         self.mozkomors_images[3], 3))

            # self.choose_new_target()

        self.choose_new_target()

    def choose_new_target(self):
        new_mozkomor_to_catch = random.choice(self.group_of_mozkomors.sprites())
        self.mozkomor_catch_type = new_mozkomor_to_catch.type
        self.mozkomor_catch_image = new_mozkomor_to_catch.image

    def pause_game(self, main_text, subheading_text):
        global lets_continue

        # Colors
        dark_yellow = pygame.Color("#938f0c")
        black = (0, 0, 0)

        # main text for pause
        main_text_create = self.potter_font_big.render(main_text, True, dark_yellow)
        main_text_create_rect = main_text_create.get_rect()
        main_text_create_rect.center = (width // 2, height // 2)

        # Subheading for pause
        subheading_text_create = self.potter_font_big.render(subheading_text, True, dark_yellow)
        subheading_text_create_rect = subheading_text_create.get_rect()
        subheading_text_create_rect.center = (width // 2, height // 2 + 60)

        # Blitting
        screen.fill(black)
        screen.blit(main_text_create, main_text_create_rect)
        screen.blit(subheading_text_create, subheading_text_create_rect)
        pygame.display.update()

        # Stop game
        paused = True
        while paused:
            for one_event in pygame.event.get():
                if one_event.type == pygame.KEYDOWN:
                    if one_event.key == pygame.K_RETURN:
                        paused = False
                if one_event.type == pygame.QUIT:
                    paused = False
                    lets_continue = False

    def reset_game(self):
        self.score = 0
        self.round_number = 0

        self.our_player.lives = 5
        self.our_player.enter_safe_zone = 3
        self.start_new_round()

        # Music
        pygame.mixer.music.play(-1, 0.0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("img/potter-icon.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = width // 2
        self.rect.bottom = height

        self.lives = 5
        self.enter_safe_zone = 3
        self.speed = 8

        self.catch_sound = pygame.mixer.Sound("media/expecto-patronum.mp3")
        self.catch_sound.set_volume(0.1)
        self.wrong_sound = pygame.mixer.Sound("media/wrong.wav")
        self.wrong_sound.set_volume(0.1)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < width:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 100:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < height - 100:
            self.rect.y += self.speed

    def back_to_safe_zone(self):
        if self.enter_safe_zone > 0:
            self.enter_safe_zone -= 1
            self.rect.bottom = height

    def reset(self):
        self.rect.centerx = width // 2
        self.rect.bottom = height


class Mozkomor(pygame.sprite.Sprite):
    def __init__(self, x, y, image, mozkomor_type):
        super().__init__()
        # Loading image and set image
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # Mozkomor types: 0: blue, 1: green, 2: pink, 3: yellow
        self.type = mozkomor_type

        # random mozkomor direction
        self.x = random.choice([-1, 1])
        self.y = random.choice([-1, 1])
        self.speed = random.randint(1, 5)

    def update(self):
        # Mozkomor move
        self.rect.x += self.x * self.speed
        self.rect.y += self.y * self.speed

        # Mozkomor bounce
        if self.rect.left < 0 or self.rect.right > width:
            self.x = -1 * self.x

        if self.rect.top < 100 or self.rect.bottom > height - 100:
            self.y = -1 * self.y


mozkomor_group = pygame.sprite.Group()

player_group = pygame.sprite.Group()
one_player = Player()
player_group.add(one_player)

# GAME
my_game = Game(one_player, mozkomor_group)
my_game.pause_game("Harry Potter and Mozkomors", "Press Enter to play")
my_game.start_new_round()

# Main loop
lets_continue = True
while lets_continue:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            lets_continue = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                one_player.back_to_safe_zone()

    # Filling screen
    # screen.fill((0, 0, 0))
    screen.blit(my_game.background_image, my_game.background_image_rect)

    # Updating group of Mozkomor
    mozkomor_group.draw(screen)
    mozkomor_group.update()

    # Updating group of Player
    player_group.draw(screen)
    player_group.update()

    # Updating GAME
    my_game.update()
    my_game.draw()

    # Update display
    pygame.display.update()

    # Tick per sec
    clock.tick(fps)

# Quit
pygame.quit()

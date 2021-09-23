import pygame
import sys
from pygame.locals import *
import random

pygame.init()
# ________________________Global Variables________________________
game_mode = 0
ai_meet_point = 0
meet_point_set = False

is_reset = False
ballx = 10
bally = 10
main_bg = pygame.image.load('red_bg.jpg')
settings_bg = pygame.image.load('starting_bg.jpg')
colors = {"White": (255, 255, 255), "Black": (0, 0, 0), "Red": (255, 0, 0), "Green": (0, 255, 0), "Blue": (0, 0, 255)}
clock = pygame.time.Clock()
WIDTH = 800
HEIGHT = 600

font1 = pygame.font.Font('Zian free promo.ttf', 50)
font2 = pygame.font.Font('Zian free promo.ttf', 70)
font3 = pygame.font.Font('charter_bold_bt.ttf', 40)
# ________________________PowerUp setups________________________
current_powerUp = None

# ________________________Ball Setups________________________

ball_1 = pygame.image.load("light_blue_ball.png")
ball_1 = pygame.transform.scale(ball_1, (32, 32))

# ________________________Screen Setup________________________

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong with a twist')
bg = settings_bg


def new_random_int(int1, int2):
    numbs = []
    while True:
        numb = random.randint(int1, int2)
        for i in numbs:
            if i == numb:
                pass
            if i != numb:
                return numb


def screen_bg(background):
    global bg
    bg = background


def reset_pong():
    global is_reset
    ball.active = False
    ball.reset_ball()
    game_manager.player1_score = 0
    game_manager.player2_score = 0
    game_manager.ai_score = 0
    player1.movement = 0
    player2.movement = 0
    ai.movement = 0
    is_reset = True


'''________________________Block Class________________________'''


class Block(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))


'''________________________Ball Class ________________________'''


class Ball(Block):
    def __init__(self, path, x_pos, y_pos, speed_x, speed_y, paddles, ai_v_p_group, powerUps):
        super().__init__(path, x_pos, y_pos)

        self.speed_x = 4 * random.choice((-1.75, -1.5, -1.25, 0, 1.25, 1.5, 1.75))
        self.speed_y = 4 * random.choice((-1.75, -1.5, -1.25, 0, 1.25, 1.5, 0.75))
        self.paddles = paddles
        self.ai_v_p_group = ai_v_p_group
        self.powerUp = powerUps
        self.active = False
        self.score_time = 0
        self.a = random.randint(200, WIDTH - 200)
        self.b = random.randint(100, HEIGHT - 100)
        self.speed_boost = PowerUp("speed_boost.png", self.a, self.b)

    def increase_speed(self):
        self.times = 0
        timer = pygame.time.get_ticks()

        if timer % 700 == 0:
            self.speed_y *= 1.1
            self.speed_x *= 1.1
            print("increased")
            ball.times += 1


        else:
            pass

    def update_ball(self):
        if self.active:
            self.cur_time = pygame.time.get_ticks()

            self.rect.x += self.speed_x
            self.rect.y += self.speed_y


        else:
            self.reset_ball()
            self.restart_counter()

    def powerUp_collision(self, group):
        if pygame.sprite.spritecollide(self, group, False):
            self.collision_side = pygame.sprite.spritecollide(self, group, True)[0].rect
            # horizontals and verticals; left, right, up and down
            if abs(self.rect.right - self.collision_side.left) < self.speed_x:
                if self.speed_x > 0:
                    player1.updatePong_hotBar()
                if self.speed_x < 0:
                    player2.updatePong_hotBar()
            if abs(self.rect.left - self.collision_side.right) < self.speed_x:
                if self.speed_x > 0:
                    player1.updatePong_hotBar()
                if self.speed_x < 0:
                    player2.updatePong_hotBar()
            if abs(self.rect.top - self.collision_side.bottom) < self.speed_x:
                if self.speed_y < 0 and self.speed_x > 0:
                    player1.updatePong_hotBar()
                if self.speed_y < 0 and self.speed_x < 0:
                    player2.updatePong_hotBar()
            if abs(self.rect.bottom - self.collision_side.top) < self.speed_x:
                if self.speed_y > 0 and self.speed_x > 0:
                    player1.updatePong_hotBar()
                if self.speed_y > 0 and self.speed_x < 0:
                    player2.updatePong_hotBar()
            # diagonals
            if abs(self.rect.bottom - self.collision_side.top) < self.speed_x and abs(self.rect.right - self.collision_side.left) < self.speed_x:
                if self.speed_y > 0:
                    print("1")
                    player1.updatePong_hotBar()
            if abs(self.rect.top - self.collision_side.bottom) < self.speed_x and abs(self.rect.right - self.collision_side.left) < self.speed_x:
                if self.speed_y < 0:
                    print("2")
                    player1.updatePong_hotBar()
            if abs(self.rect.bottom - self.collision_side.top) < self.speed_x and abs(self.rect.left - self.collision_side.right) < self.speed_x:
                if self.speed_y > 0:
                    print("3")
                    player2.updatePong_hotBar()
            if abs(self.rect.top - self.collision_side.bottom) < self.speed_x and abs(self.rect.left - self.collision_side.right) < self.speed_x:
                if self.speed_y < 0:
                    print("4")
                    player2.updatePong_hotBar()

            print(f"p1: {player1.hot_bar, player1.num_coins}")
            print(f"p2: {player2.hot_bar, player2.num_coins}")

    def collisions(self):
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1

        if game_mode > 0:
            global meet_point_set
            if pygame.sprite.spritecollide(self, self.ai_v_p_group, False):
                collision_paddle = pygame.sprite.spritecollide(self, self.ai_v_p_group, False)[0].rect
                if abs(self.rect.right - collision_paddle.left) < 13 and self.speed_x > 0:
                    self.speed_x *= -1
                if abs(self.rect.left - collision_paddle.right) < 13 and self.speed_x < 0:
                    self.speed_x *= -1
                if abs(self.rect.top - collision_paddle.bottom) < 13 and self.speed_y < 0:
                    self.rect.top = collision_paddle.bottom
                    self.speed_y *= -1
                if abs(self.rect.bottom - collision_paddle.top) < 13 and self.speed_y > 0:
                    self.rect.bottom = collision_paddle.top
                    self.speed_y *= -1

        else:
            if pygame.sprite.spritecollide(self, self.paddles, False):
                collision_paddle = pygame.sprite.spritecollide(self, self.paddles, False)[0].rect
                if abs(self.rect.right - collision_paddle.left) < 13 and self.speed_x > 0:
                    self.speed_x *= -1
                if abs(self.rect.left - collision_paddle.right) < 13 and self.speed_x < 0:
                    self.speed_x *= -1
                if abs(self.rect.top - collision_paddle.bottom) < 13 and self.speed_y < 0:
                    self.rect.top = collision_paddle.bottom
                    self.speed_y *= -1
                if abs(self.rect.bottom - collision_paddle.top) < 13 and self.speed_y > 0:
                    self.rect.bottom = collision_paddle.top
                    self.speed_y *= -1

    def reset_ball(self):
        print("reset")
        global is_reset
        is_reset = False
        self.active = False
        self.times = 0
        self.speed_x = 4
        self.speed_x *= random.choice((-1, 1))
        self.speed_y = 4
        self.speed_y *= random.choice((-1, 1))
        self.score_time = pygame.time.get_ticks()
        self.a = random.randint(200, WIDTH - 200)
        self.b = random.randint(100, HEIGHT - 100)
        player1_hot_bar.clear()
        player2_hot_bar.clear()
        self.rect.center = (WIDTH / 2, random.randint(50, HEIGHT - 50))

        ai.rect.y = HEIGHT / 2 - int(player1.rect.height) / 2
        player1.rect.y = HEIGHT / 2 - int(player1.rect.height) / 2
        player2.rect.y = HEIGHT / 2 - int(player2.rect.height) / 2

    def restart_counter(self):

        self.active = True


'''________________________Ai Class________________________'''


class Ai(Block):
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__(path, x_pos, y_pos)
        self.speed = speed
        self.movement = 0

    def constraint(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT

    def update_movement(self):
        c = 0
        posi = ball.rect.centerx, ball.rect.centery

        if ball.times == 0:
            c = 4
        else:
            c = 4 * 1.1 * ball.times
        l = ball.rect.x + (HEIGHT - ball.rect.y) * ball.speed_x / float(c)
        a = 0
        b = 0
        if game_mode == 1:
            a, b = -30, 30
        if game_mode == 2:
            a, b = -20, 20
        if game_mode == 3:
            a, b = 0, 0
            self.speed = 5
            if ball.rect.centery + random.randint(a, b) < self.rect.centery:
                self.movement = -self.speed
                self.rect.y += self.movement
            elif ball.rect.centery + random.randint(a, b) > self.rect.centery:
                self.movement = self.speed
                self.rect.centery += self.movement
            else:
                self.movement = 0
                self.rect.y += self.movement

            self.constraint()
        if game_mode == 1 or 2:
            self.speed = 4
            if ball.rect.y + random.randint(a, b) < self.rect.y:
                self.movement = -self.speed
                self.rect.y += self.movement
            elif ball.rect.y + random.randint(a, b) > self.rect.y:
                self.movement = self.speed
                self.rect.y += self.movement
            else:
                self.movement = 0
                self.rect.y += self.movement

            self.constraint()


'''________________________Player Class________________________'''


class Player(Block):
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__(path, x_pos, y_pos)
        self.speed = speed
        self.movement = 0
        self.hot_bar = []
        self.num_coins = 0

    def constraint(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT

    def update_movement(self, ball_something):
        self.rect.y += self.movement
        self.constraint()

    def updatePong_hotBar(self):
        global current_powerUp
        if current_powerUp == "confusion":
            self.hot_bar.append("confusion")
        if current_powerUp == "times_2_coins":
            self.hot_bar.append("times_2_coins")
        if current_powerUp == "ball_speedboost":
            self.hot_bar.append("ball_speedboost")
        if current_powerUp == "speed_boost":
            self.hot_bar.append("speed_boost")
        if current_powerUp == "coin":
            self.num_coins += 10
        current_powerUp = "l"


'''________________________Two Player Manager Class________________________'''


class TwoPlayerManager:
    def __init__(self, ball_group, paddle_group, ai_v_p_group, powerUps):
        self.player1_score = 0
        self.player2_score = 0
        self.ai_score = 0
        self.ball_group = ball_group
        self.paddle_group = paddle_group
        self.ai_v_p_group = ai_v_p_group
        self.a = random.randint(70, WIDTH - 70)
        self.b = random.randint(60, HEIGHT - 60)
        self.f = 0
        self.powerUp = powerUps

    def run_game(self):

        if game_mode > 0:
            self.powerUp.draw(screen)
            self.ai_v_p_group.draw(screen)
            self.ball_group.draw(screen)
            confusion_group.draw(screen)
            times_2_coins_group.draw(screen)
            ball_speedboost_group.draw(screen)
            coin_group.draw(screen)

            self.ai_v_p_group.update(self.ball_group)
            self.ball_group.update()
            self.draw_score()
            ball.powerUp_collision(speed_boost_group)
            ball.powerUp_collision(ball_speedboost_group)
            ball.powerUp_collision(times_2_coins_group)
            ball.powerUp_collision(coin_group)
            ball.powerUp_collision(confusion_group)
            self.randomize_powerUps()
            self.find_new_place()
            ball.increase_speed()

            ai.update_movement()
            player2.update_movement(1)
            ball.increase_speed()
            if not ball.active:
                ball.reset_ball()
                ball.restart_counter()
            ball.update_ball()
            ball.collisions()
            self.isGameOver()
            self.reset_ball()

        else:
            self.paddle_group.draw(screen)
            self.ball_group.draw(screen)
            ball.powerUp_collision(speed_boost_group)
            ball.powerUp_collision(ball_speedboost_group)
            self.paddle_group.update(self.ball_group)
            self.ball_group.update()
            self.powerUp.draw(screen)

            confusion_group.draw(screen)
            times_2_coins_group.draw(screen)
            ball_speedboost_group.draw(screen)
            coin_group.draw(screen)

            self.draw_score()
            ball.powerUp_collision(speed_boost_group)
            ball.powerUp_collision(ball_speedboost_group)
            ball.powerUp_collision(times_2_coins_group)
            ball.powerUp_collision(coin_group)
            ball.powerUp_collision(confusion_group)
            self.randomize_powerUps()
            self.find_new_place()
            player1.update_movement(1)
            player2.update_movement(1)
            ball.increase_speed()
            if not ball.active:
                ball.reset_ball()
                ball.restart_counter()
            ball.update_ball()
            ball.collisions()
            self.isGameOver()

            self.reset_ball()

    def isGameOver(self):
        if game_mode > 0:
            if self.ai_score == 5:
                page.make_current("starting_screen")
                print(f"Ai lvl {game_mode} Won")

            if self.player2_score == 5:
                page.make_current("starting_screen")
                print("Player 2 Won")
        else:
            if self.player1_score == 5:
                page.make_current("starting_screen")
                print("Player 1 Won")

            if self.player2_score == 5:
                page.make_current("starting_screen")
                print("Player 2 Won")

    def reset_ball(self):
        if game_mode > 0:
            if self.ball_group.sprite.rect.right >= WIDTH:
                self.ai_score += 1
                self.randomize_powerUps()
                ball.reset_ball()

            if self.ball_group.sprite.rect.left <= 0:
                self.player2_score += 1
                self.randomize_powerUps()
                ball.reset_ball()
        else:
            if self.ball_group.sprite.rect.right >= WIDTH:
                self.player1_score += 1
                self.randomize_powerUps()
                ball.reset_ball()

            if self.ball_group.sprite.rect.left <= 0:
                self.player2_score += 1
                self.randomize_powerUps()
                ball.reset_ball()

    def randomize_powerUps(self):

        if len(coin_group) == 0 and len(speed_boost_group) == 0 and len(times_2_coins_group) == 0 and len(confusion_group) == 0 and len(
                ball_speedboost_group) == 0:
            if pygame.time.get_ticks() % 450 == 0:
                global current_powerUp
                choice = random.choice(types_of_powerUps)
                print(choice)

                if choice != 1:
                    current_powerUp = "coin"
                    coin_group.add(coin)
                if choice == confusion:
                    current_powerUp = "confusion"
                    confusion_group.add(confusion)
                if choice == speed_boost:
                    current_powerUp = "speed_boost"
                    speed_boost_group.add(speed_boost)
                if choice == times_2_coins:
                    current_powerUp = "times_2_coins"
                    times_2_coins_group.add(times_2_coins)
                if choice == ball_speedboost:
                    current_powerUp = "ball_speedboost"
                    ball_speedboost_group.add(ball_speedboost)

                self.find_new_place()
                # if self.timers > goal:

    def find_new_place(self):
        global speed_boost, ball_speedboost, confusion, coin, times_2_coins
        self.f += 1

        random.seed(self.f)
        self.a = random.randint(70, WIDTH - 70)
        self.b = random.randint(60, HEIGHT - 60)
        speed_boost = PowerUp("speed_boost.png", self.a, self.b)
        confusion = PowerUp("ball_confusion.png", self.a, self.b)
        ball_speedboost = PowerUp("ball_boost.png", self.a, self.b)
        times_2_coins = PowerUp("times_2_coins.png", self.a, self.b)
        coin = PowerUp("game_coin.png", self.a, self.b)

    def draw_score(self):
        if game_mode > 0:
            player2_score = Text(screen, f"{self.player2_score}", font3, colors["White"], WIDTH / 2 + 40, 20)
            ai_score = Text(screen, f"{self.ai_score}", font3, colors["White"], WIDTH / 2 - 70, 20)

            player2_score.draw()
            ai_score.draw()
        else:
            player2_score = Text(screen, f"{self.player2_score}", font3, colors["White"], WIDTH / 2 + 40, 20)
            player1_score = Text(screen, f"{self.player1_score}", font3, colors["White"], WIDTH / 2 - 70, 20)

            player2_score.draw()
            player1_score.draw()


'''________________________Text Class ________________________'''


class Text:
    def __init__(self, surface, text, font, color, x, y):
        self.surface = surface
        self.text = text
        self.font = font
        self.color = color
        self.x = x
        self.y = y

    def draw(self):
        textobj = self.font.render("{}".format(self.text), 1, self.color)
        textrect = textobj.get_rect()
        textrect.topleft = (self.x, self.y)
        self.surface.blit(textobj, textrect)


'''________________________PowerUp Class________________________'''


class PowerUp(Block):
    def __init__(self, path, x_pos, y_pos):
        super().__init__(path, x_pos, y_pos)


'''________________________More Set Up________________________'''
player1 = Player("Paddle.png", 35, HEIGHT / 2, 4)
player2 = Player("Paddle.png", WIDTH - 35, HEIGHT / 2 - 50, 4)

ai = Ai("Paddle.png", 35, HEIGHT / 2, 4)

paddle_group = pygame.sprite.Group()
paddle_group.add(player1)
paddle_group.add(player2)

ai_vs_player_group = pygame.sprite.Group()
player2.add(ai_vs_player_group)
ai.add(ai_vs_player_group)

speed_boost = PowerUp("speed_boost.png", random.randint(100, WIDTH - 100), random.randint(70, HEIGHT - 70))
speed_boost_group = pygame.sprite.Group()

confusion = PowerUp("ball_confusion.png", random.randint(100, WIDTH - 100), random.randint(70, HEIGHT - 70))
confusion_group = pygame.sprite.Group()

ball_speedboost = PowerUp("ball_boost.png", random.randint(100, WIDTH - 100), random.randint(70, HEIGHT - 70))
ball_speedboost_group = pygame.sprite.Group()

times_2_coins = PowerUp("times_2_coins.png", random.randint(100, WIDTH - 100), random.randint(70, HEIGHT - 70))
times_2_coins_group = pygame.sprite.Group()

coin = PowerUp("game_coin.png", random.randint(100, WIDTH - 100), random.randint(70, HEIGHT - 70))
coin_group = pygame.sprite.Group()

types_of_powerUps = [coin, speed_boost, times_2_coins, confusion, ball_speedboost]

ball = Ball("light_blue_ball.png", WIDTH / 2, random.randint(50, HEIGHT - 50), 5, 5, paddle_group, ai_vs_player_group,
            (speed_boost_group, times_2_coins_group, coin_group, confusion_group, ball_speedboost_group))
ball_sprite = pygame.sprite.GroupSingle(ball)

player1_hot_bar = []
player2_hot_bar = []

game_manager = TwoPlayerManager(ball_sprite, paddle_group, ai_vs_player_group, speed_boost_group)

'''________________________Button Class ________________________'''


class Button:
    def __init__(self, surface, color, font, x, y, text):
        self.text = text
        self.color = color
        self.x = x
        self.y = y
        self.font = font
        self.surface = surface

    def get_clicked(self):

        textobj = self.font.render(self.text, 1, self.color)
        textrect = textobj.get_rect()
        w = textrect.width
        h = textrect.height
        if self.x <= mx <= self.x + w and self.y <= my <= self.y + h - 6:
            return True
        else:
            return False

    def isHover(self, width, height):
        if self.x <= mx <= self.x + width:
            if self.y <= my <= self.y + height - 6:
                return True

    def draw(self, hover: bool = False, color2=colors['Red'],
             cur: int = 0):  # hh means 'highlight hover' as in to highlight the text if the mouse hovers over it
        textobj = self.font.render(self.text, 1, self.color)
        textrect = textobj.get_rect()
        textrect.topleft = self.x, self.y
        w = textrect.width
        h = textrect.height

        self.surface.blit(textobj, textrect)
        if hover:
            if self.isHover(w, h):
                pygame.mouse.set_cursor(cur)
                textobj = self.font.render(self.text, 1, color2)
                textrect = textobj.get_rect()
                textrect.topleft = self.x, self.y
                self.surface.blit(textobj, textrect)


'''________________________Screen Class ________________________'''


class CurrentScreen:
    def __init__(self):
        self.state = 'starting_screen'

    def starting_screen(self):

        if not is_reset:
            reset_pong()

        pygame.mouse.set_cursor(0)
        screen.blit(bg, (0, 0))

        # ________________________Start Screen Buttons________________________
        welcome_txt = Text(screen, "Welcome to Pong", font2, colors["White"], WIDTH / 4 - 170, HEIGHT / 6)
        play_btn = Button(screen, colors["White"], font1, WIDTH / 2 - 73, HEIGHT / 6 * 2, "Play")
        settings_btn = Button(screen, colors["White"], font1, WIDTH / 2 - 131, HEIGHT / 6 * 3, "Settings")
        welcome_txt.draw()
        play_btn.draw(True, color2=colors["Blue"], cur=11)
        settings_btn.draw(True, colors["Blue"], cur=11)
        screen_bg(settings_bg)

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == MOUSEBUTTONUP:
                if play_btn.get_clicked():
                    self.make_current("main_game")
                elif settings_btn.get_clicked():
                    self.make_current("settings")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    pass
        pygame.display.update()

    def main_game(self):
        pygame.mouse.set_cursor(0)
        screen.blit(bg, (0, 0))
        screen_bg(settings_bg)
        pygame.draw.line(screen, colors["Red"], (WIDTH / 2, 0), (WIDTH / 2, HEIGHT), 2)

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == MOUSEBUTTONUP:
                self.state = 'starting_screen'
                self.state_manager()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_w:
                    player1.movement = -player1.speed
                if event.key == pygame.K_s:
                    player1.movement = player1.speed
                if event.key == pygame.K_UP:
                    player2.movement = -player2.speed
                if event.key == pygame.K_DOWN:
                    player2.movement = player2.speed

            if event.type == KEYUP:

                if event.key == pygame.K_w:
                    player1.movement = 0
                if event.key == pygame.K_s:
                    player1.movement = 0
                if event.key == pygame.K_UP:
                    player2.movement = 0
                if event.key == pygame.K_DOWN:
                    player2.movement = 0

        game_manager.run_game()
        pygame.display.update()

    def settings(self):
        pygame.mouse.set_cursor(0)
        screen.blit(bg, (0, 0))
        screen_bg(settings_bg)

        title_txt = Text(screen, "Settings", font2, colors["White"], WIDTH / 2 - 187, HEIGHT / 9)
        title_txt.draw()

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == MOUSEBUTTONUP:
                self.make_current("starting_screen")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    pass

            pygame.display.update()

    def state_manager(self):
        if self.state == 'starting_screen':
            self.starting_screen()
        elif self.state == 'main_game':
            self.main_game()
        elif self.state == 'settings':
            self.settings()

    def make_current(self, ToBeCurrent):
        if ToBeCurrent == 'starting_screen':
            self.state = 'starting_screen'
            self.state_manager()

        if ToBeCurrent == 'main_game':
            self.state = 'main_game'
            self.state_manager()

        if ToBeCurrent == 'settings':
            self.state = 'settings'
            self.state_manager()


page = CurrentScreen()
while True:
    clock.tick(60)
    mx, my = pygame.mouse.get_pos()
    pos = pygame.mouse.get_pos()
    page.state_manager()

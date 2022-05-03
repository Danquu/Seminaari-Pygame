import pygame
import random

pygame.init()

#Pelinäyttö
WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyPong")

#Äänet
point = pygame.mixer.Sound("point.wav")
point.set_volume(0.03)

thunk = pygame.mixer.Sound("thunk.wav")
thunk.set_volume(0.02)

yay = pygame.mixer.Sound("yay.wav")
yay.set_volume(0.03)

#Musiikki
music = pygame.mixer.music.load("bensound.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.03)

#FPS-CAP
FPS = 60

#Eri värejä peliin satunnaisvaihteluksi
COLORS = [(255, 255, 255), (0, 0, 0), (0, 0, 204), (255, 165, 0), (189, 183, 107), (72, 61, 139), (0, 255, 0)]

#Värien vaihtelu
COLOR = random.choice(COLORS)

#Tarvittavat värit jotka eivät vaihdu
WHITE = (255, 255, 255)
PINK = (255,192,203)
BLUE = (0, 0, 139)
RED = (139,0,0)

#Pelitikun leveys & pituus
PADDLE_WIDTH, PADDLE_HEIGHT = 8, 85

#Pallon koko
BALL_RADIUS = 6

#Tulostekstin fontti & koko
SCORE_FONT = pygame.font.SysFont("calibri", 50)

#Monta pistettä voittoon?
WINNING_SCORE = 5

#Pelitikun luokka
class Paddle:

    #Väri satunnaiseksi sekä nopeus
    COLOR = COLOR
    VEL = 4

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move (self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset (self):
        self.x = self.original_x
        self.y = self.original_y



#Pallon luokka
class Ball:

    #Pallon nopeus & väri satunnaiseksi
    MAX_VEL = 5
    COLOR = COLOR

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1


#Funktio joka luo pelialueen
def draw(win, paddles, ball, left_score, right_score):

    #Tausta vakiona pinkiksi
    win.fill(PINK)

    left_score_text = SCORE_FONT.render(f"{left_score}", 1, COLOR)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, COLOR)
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (WIDTH * (3/4) - right_score_text.get_width()//2, 20))

    for paddle in paddles:
        paddle.draw(win)

    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:          
            continue
        
        #Keskiviivojen luonti, valkoinen vakioväri)
        pygame.draw.rect(win, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))

    ball.draw(win)
    pygame.display.update()


#Pelilogiikan funktio jotta pallo liikkuu minne pitää
def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT:
        thunk.play()
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        thunk.play()
        ball.y_vel *= -1

    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel
                thunk.play()
    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel
                thunk.play()

#Pelitikkujen funktio jotta ne liikkuvat ylös sekä alas
def handle_paddle_movement(keys, left_paddle, right_paddle):
        if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
            left_paddle.move(up=True)
        if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
            left_paddle.move(up=False)

        if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
            right_paddle.move(up=True)
        if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
            right_paddle.move(up=False)


#Main-funktio
def main():
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

    left_score = 0
    right_score = 0

    while run:
        clock.tick(FPS)
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break


        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        #Jos pallo menee yli rajan näytön vasemmalta puolelta
        if ball.x < 0:
            point.play()
            right_score += 1
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
        
        #Jos pallo menee yli rajan näytön oikealta puolelta
        elif ball.x > WIDTH:
            point.play()
            left_score += 1
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            

        won = False
        if left_score >= WINNING_SCORE:
            won = True
            win_text = "PLAYER 1 WINS"
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "PLAYER 2 WINS"
        
        #Voittotekstin asettelu, uuden pelin aloitus
        if won:
            text = SCORE_FONT.render(win_text, 1, COLOR)
            WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height() //2))
            yay.play()
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0
    
    pygame.quit()

if __name__ == '__main__':
    main()

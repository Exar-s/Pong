import pygame
pygame.init()

WIDTH, HEIGHT = 680, 480
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PONG")

PADDLE_WIDTH, PADDLE_HEIGHT = 15, 85
BALL_RADIUS = 12
ORIGNAL_Y = HEIGHT / 2 - PADDLE_HEIGHT / 2
ORIGNAL_LEFTX = 10
ORIGNAL_RIGHTX = WIDTH - 10 - PADDLE_WIDTH
FONT = pygame.font.Font('PressStart2P-Regular.ttf', 20)

class Paddle:
  color = (245,245,245)
  velocity = 5

  def __init__(self, x, y, width, height):
    self.x = self.originalX = x
    self.y = y
    self.width = width
    self.height = height
    self.score = 0

  def draw(self):
    pygame.draw.rect(WINDOW, self.color, (self.x, self.y, self.width, self.height))

  def move(self, direction):
    if direction == 'up':
      self.y -= self.velocity
    else:
      self.y += self.velocity

  def update_score(self):
    self.score += 1

  def reset(self):
    self.x = self.originalX
    self.y = ORIGNAL_Y
    self.score = 0

class Ball:
  color = (245,245,245)
  velocity = 5.5

  def __init__(self, x, y, radius):
    self.x = x
    self.y = y
    self.radius = radius
    self.x_velocity = self.velocity
    self.y_velocity = 0

  def draw(self):
    pygame.draw.circle(WINDOW, self.color, (self.x, self.y), self.radius)

  def move(self):
    self.x += self.x_velocity
    self.y += self.y_velocity

  def reset(self):
    self.x = WIDTH / 2
    self.y = HEIGHT / 2
    self.x_velocity *= -1
    self.y_velocity = 0

def update_window(paddles, ball):
  WINDOW.fill((0,0,0))
  pygame.draw.line(WINDOW, (84,84,84), (WIDTH / 2, 0), (WIDTH / 2, HEIGHT), 5)
  left_score = FONT.render(str(paddles[0].score), True, (255,255,255))
  right_score = FONT.render(str(paddles[1].score), True, (255,255,255))
  WINDOW.blit(left_score, (WIDTH/4 - left_score.get_width()/2,10))
  WINDOW.blit(right_score, (WIDTH * (3/4) - right_score.get_width()/2,10))
  for paddle in paddles:
    paddle.draw()
  ball.draw()
  pygame.display.update()

def handle_movement(keys, left_paddle, right_paddle):
  if keys[pygame.K_w] and left_paddle.y - left_paddle.velocity >= 0:
    left_paddle.move('up')
  if keys[pygame.K_s] and left_paddle.y + left_paddle.height + left_paddle.velocity <= HEIGHT:
    left_paddle.move('down')
  if keys[pygame.K_UP] and right_paddle.y - right_paddle.velocity >= 0:
    right_paddle.move('up')
  if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.height + right_paddle.velocity <= HEIGHT:
    right_paddle.move('down')

def handle_collision(ball, left_paddle, right_paddle):
  if ball.y - ball.radius <= 0:
    ball.y_velocity *= -1
  elif ball.y + ball.radius >= HEIGHT:
    ball.y_velocity *= -1

  if ball.x_velocity < 0:
    if ball.y + ball.radius >= left_paddle.y and ball.y - ball.radius <= left_paddle.y + left_paddle.height and ball.x <= left_paddle.x + left_paddle.width:
        ball.x_velocity *= -1
        mid = left_paddle.y + left_paddle.height / 2
        diff = ball.y - mid
        paddle_portions = (left_paddle.height / 2) / ball.velocity
        ball.y_velocity = diff / paddle_portions
  elif ball.x_velocity > 0:
    if ball.y + ball.radius >= right_paddle.y and ball.y - ball.radius <= right_paddle.y + right_paddle.height and ball.x >= right_paddle.x:
        ball.x_velocity *= -1
        mid = right_paddle.y + right_paddle.height / 2
        diff = ball.y - mid
        paddle_portions = (right_paddle.height / 2) / ball.velocity
        ball.y_velocity = diff / paddle_portions

def handle_score(ball, left_paddle, right_paddle):
  if ball.x - ball.radius < 0 :
    right_paddle.update_score()
    ball.reset()
  elif ball.x + ball.radius > WIDTH:
    left_paddle.update_score()
    ball.reset()

def winner_screen(winner):
  WINDOW.fill((0,0,0))
  win_msg = FONT.render(winner, True, (255,255,255))
  restart_msg = FONT.render('Press Enter To Restart', True, (255,255,255))
  quit_msg = FONT.render('Press Q To Quit', True, (255,255,255))
  WINDOW.blit(win_msg, (WIDTH /2 - win_msg.get_width() / 2, HEIGHT/2 - win_msg.get_height() * 2))
  WINDOW.blit(restart_msg, (WIDTH /2 - restart_msg.get_width() / 2, HEIGHT/2 - restart_msg.get_height() / 2))
  WINDOW.blit(quit_msg, (WIDTH /2 - quit_msg.get_width() / 2, HEIGHT/2 + quit_msg.get_height()))
  pygame.display.update()

def main():
  clock = pygame.time.Clock()
  left_paddle = Paddle(ORIGNAL_LEFTX, ORIGNAL_Y, PADDLE_WIDTH, PADDLE_HEIGHT)
  right_paddle = Paddle(ORIGNAL_RIGHTX, ORIGNAL_Y, PADDLE_WIDTH, PADDLE_HEIGHT)
  ball = Ball(WIDTH / 2, HEIGHT / 2, BALL_RADIUS)
  win = False
  winner = ''
  while True:
    clock.tick(60)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        exit()
      if event.type == pygame.KEYDOWN and win:
        if event.key == pygame.K_q:
          exit()
        if event.key == pygame.K_RETURN:
          ball.reset()
          left_paddle.reset()
          right_paddle.reset()
          win = False
    
    keys = pygame.key.get_pressed()
    if not win:
      update_window([left_paddle, right_paddle], ball)
      handle_movement(keys, left_paddle, right_paddle)
      ball.move()
      handle_collision(ball, left_paddle, right_paddle)
      handle_score(ball, left_paddle, right_paddle)
      if left_paddle.score >= 5:
        win = True
        winner = 'Left Won!'
      elif right_paddle.score >=5:
        win = True
        winner = 'Right Won!'
    else:
      winner_screen(winner)

if __name__ == '__main__':
  main()
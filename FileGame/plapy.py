import pygame, sys, random
# create funcition for game
def draw_floor():
    screen.blit(floor,(floor_x,570))
    screen.blit(floor,(floor_x + 432,570))
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(500,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop=(500,random_pipe_pos-650))
    return  bottom_pipe, top_pipe
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -=3
    return pipes
def draw_pipe(pipes): # thay doi neu pipe nguoc
    for pipe in pipes:
        if pipe.bottom >= 500 :
            screen.blit(pipe_surface,pipe)
        else:   
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)
def check(pipes):
    for pipe in pipes:
        if duck_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if duck_rect.top <= -75 or duck_rect.bottom >=650:
        return False
    return True
def rotate_duck( duck1) :
    new_duck = pygame.transform.rotozoom(duck1,- duck_move*3, 1)
    return new_duck
def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (216, 100))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'High Score: {int(hight_score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (216, 480))
        screen.blit(score_surface,score_rect)
        hight_score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        hight_score_rect = hight_score_surface.get_rect(center = (216, 100))
        screen.blit(hight_score_surface,hight_score_rect)
def update_score( score, hight_score):
    if score > hight_score:
        hight_score= score
    return hight_score
pygame.mixer.pre_init(frequency= 44100, size =-16, channels= 2, buffer=512)
pygame.init()
screen =pygame.display.set_mode((432,768))
clock =pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf', 40)
#tao bien
gravity = 0.08
duck_move = 0
game_active =True
score = 0
hight_score =0
bg = pygame.image.load('assets/background-night.png').convert()
bg = pygame.transform.scale2x(bg)
floor = pygame.image.load('assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x = 0

duck = pygame.image.load('assets/duck.png').convert_alpha()
duck_rect = duck.get_rect(center =(100,300))
#tao ong
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
#pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list =[]
#tao timer
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe,1300)
pipe_height =[  200, 250, 260, 270]
# tao man hinh ket thuc
game_over_surface = pygame.image.load('assets/message.png').convert_alpha()
game_over_surface = pygame.transform.scale2x(game_over_surface)
game_over_rect = game_over_surface.get_rect(center = (216,384))
# sound
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
point_sound = pygame.mixer.Sound('sound/sfx_point.wav')
count_down =100
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                duck_move = 0
                duck_move = -4
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                duck_rect.center = (100,300)
                duck_move = 0
                score=0 #tu them
        if event.type ==spawnpipe:
            pipe_list.extend(create_pipe())
    screen.blit(bg,(0,0))
    if game_active:
        #duck
    
        duck_move += gravity  #di chuyen xuong duoi
        rotated_duck = rotate_duck(duck)
        duck_rect.centery += duck_move 
        screen.blit(rotated_duck ,duck_rect)
        game_active = check(pipe_list)
        #pipe
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score += 0.01
        score_display('main_game')
        count_down -= 1
        if count_down < 0:
                point_sound.play()
                count_down=100
    else:
        screen.blit(game_over_surface, game_over_rect)
        hight_score= update_score(score, hight_score)
        score_display('game_over')
    #floor
    floor_x -=1
    draw_floor()
    if floor_x <=-432:
        floor_x=0
    pygame.display.update()
    clock.tick(130)

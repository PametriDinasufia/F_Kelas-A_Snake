
#Import module
import pygame, sys, random
from pygame.math import Vector2 #mempermudah supaya saat manggil g nulis pake "pygame.math.Vector2" terus2an

#Membuat kelas FARMER
class FARMER:
    def __init__(self): #menginisiasi
        self.randomize()

    def draw_farmer(self):
        #membuat rect
        farmer_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size) #xywh
        screen.blit(farmer,farmer_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)  # -1 supaya tetap ada di layar
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

#Membuat kelas FOOD
class FOOD:
    def __init__(self): #menginisiasi
        self.randomize()

    def draw_food(self):
        #membuat rect
        food_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size) #xywh
        screen.blit(mouse,food_rect)
        #menggambar rectangle
        #pygame.draw.rect(screen,(126,166,144), food_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)  # -1 supaya tetap ada di layar
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


#Membuat kelas SNAKE
class SNAKE:
    def __init__(self): #menginisiasi
        #              index 0        index 1       index 2  (enumerate tadi di draw_snake)
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)] #badan dari snake. posisi awal snake.
        self.direction = Vector2(0,0)
        self.new_block = False

        #load asset kepala snake
        self.head_up = pygame.image.load('asset/Snake/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('asset/Snake/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('asset/Snake/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('asset/Snake/head_left.png').convert_alpha()

        #load asset body snake
        self.body_vertical = pygame.image.load('asset/Snake/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('asset/Snake/body_horizontal.png').convert_alpha()

        #load asset body snake saat belok
        self.body_tr = pygame.image.load('asset/Snake/body_topright.png').convert_alpha()
        self.body_tl = pygame.image.load('asset/Snake/body_topleft.png').convert_alpha()
        self.body_br = pygame.image.load('asset/Snake/body_bottomright.png').convert_alpha()
        self.body_bl = pygame.image.load('asset/Snake/body_bottomleft.png').convert_alpha()

        #load asset ekor snake
        self.tail_up = pygame.image.load('asset/Snake/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('asset/Snake/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('asset/Snake/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('asset/Snake/tail_left.png').convert_alpha()

        #import audio
        self.munch_sound = pygame.mixer.Sound('asset/munch.mp3')
        self.crash_sound = pygame.mixer.Sound('asset/crash.mp3')

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body): #enumerate ngasih index di list
            #Membuat rect untuk ngasih posisi
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size) #xywh

            #Mencari tau arah dari kepala snake
            if index == 0: #index 0 = head
                screen.blit(self.head,block_rect)
            elif index == len(self.body)-1: #last item in self.body. -1 karena terhitung dari 0
                screen.blit(self.tail,block_rect)
            else:
                previous_block = self.body[index+1] - block #index yg sekarang ditambah satu
                next_block = self.body[index-1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical,block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal,block_rect)
                else: # belokan badan
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl,block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr,block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl,block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br,block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body [0] #
        if head_relation == Vector2(1,0):
            self.head = self.head_left
        elif head_relation == Vector2(-1,0):
            self.head = self.head_right
        elif head_relation == Vector2(0,1):
            self.head = self.head_up
        elif head_relation == Vector2(0,-1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]  #
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

        #membuat method untuk membuat snake bergerak
    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)  # 0 kepala
            self.body = body_copy[:]  # mengembalikan seluruh list kembali ke body
            self.new_block = False #supaya tidak memanjang terus (nilai tidak true)

        else:
            body_copy = self.body[:-1] #menggunakan slicing untuk mendapatkan 2 elemen pertama dari body list
            body_copy.insert(0, body_copy[0] + self.direction) #0 kepala
            self.body = body_copy[:] #mengembalikan seluruh list kembali ke body

    def add_block(self):
        self.new_block = True

    def play_munch_sound(self):
        self.munch_sound.play()

    def play_crash_sound(self):
        self.crash_sound.play()

    def reset(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)] #posisi awal kayak pas mulai game
        self.direction = Vector2(0, 0)

#Membuat kelas MAIN yg berisi game logic, objek snake, dan food
class MAIN:
    #menginstansiasi
    def __init__(self):
        self.snake = SNAKE() #membuat objek snake dari kelas SNAKE
        self.food = FOOD() #membuat objek food dari kelas FOOD
        self.farmer = FARMER() #membuat objek farmer dari kelas farmer

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.food.draw_food()
        self.farmer.draw_farmer()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        #TIKUS
        if self.food.pos == self.snake.body[0]: #jika posisi buah dan body snake sama, buah termakan dan hilang
            self.food.randomize() #muncul food baru secara acak
            self.farmer.randomize() #muncul farmer secara acak
            self.snake.add_block() #menambahkan panjang snake
            self.snake.play_munch_sound()

        for block in self.snake.body[1:]:
            if block == self.food.pos: #jika buah dan snake berada di posisi yang sama
                self.food.randomize()

        #FARMER
        if self.farmer.pos == self.snake.body[0]:  #jika posisi farmer dan body snake sama (kepala)
            self.snake.play_crash_sound()
            self.game_over()

            self.farmer.randomize() #muncul farmer baru secara acak
            self.food.randomize() #muncul food baru secara acak

    def check_fail(self):
        #Jika snake keluar dari screen
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number: #tabrakan dengan tembok kanan dan kiri
            self.snake.play_crash_sound()
            self.game_over()

        #mengecek jika snake bertabrakan dengan badannya sendiri
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    #method untuk reset
    def game_over(self):
        self.snake.reset()

    def draw_grass(self):
        grass_color = (167,209,61)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col*cell_size,row*cell_size,cell_size,cell_number)
                        pygame.draw.rect(screen,grass_color,grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col*cell_size,row*cell_size,cell_size,cell_number)
                        pygame.draw.rect(screen,grass_color,grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56,74,12)) #text, anti alias, color
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        mouse_rect = mouse.get_rect(midright =(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(mouse_rect.left-10, mouse_rect.top-5, mouse_rect.width + score_rect.width + 20, mouse_rect.height+10)

        pygame.draw.rect(screen,(167,209,61),bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(mouse,mouse_rect)
        pygame.draw.rect(screen,(56,209,61),bg_rect, 2) #ketebalan garis

    def pause(self):
        pause_text = "PAUSE"
        pause_surface = game_font.render(pause_text, True, (56, 74, 12))  # text, anti alias, color
        pause_x = int(cell_size * cell_number - 60)
        pause_y = int(cell_size * cell_number - 40)
        pause_rect = pause_surface.get_rect(center = (pause_x,pause_y))

        bg_rect = pygame.Rect(pause_rect.left - 10, pause_rect.top - 5, pause_rect.width + pause_rect.width + 20, pause_rect.height + 10)
        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(pause_surface, pause_rect)
        pygame.draw.rect(screen, (56, 209, 61), bg_rect, 2)  # ketebalan garis

pygame.mixer.pre_init(44100,-16,2,512)

pygame.init()
pygame.mixer.music.load('asset/bgm.mp3')
pygame.mixer.music.play(-1, 0.0)

cell_size = 35 #40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()

############TEKS###########################3
# Warna putih untuk teks
color = (255, 255, 255)
# Menyimpan lear dari screen ke dalam variabel
width = screen.get_width()
# Menyimpan tinggi dari screen ke dalam variabel
height = screen.get_height()
# Mendefinisikan font
smallfont = pygame.font.SysFont('Corbel', 35)
# Merender text di bawah
text = smallfont.render('Press up, right, left or down to start', True, color)
text2 = smallfont.render('', True, color)
text3 = smallfont.render('', True, color)
#####################################

mouse = pygame.image.load('asset/mouse.png').convert_alpha()
farmer = pygame.image.load('asset/farmer.png').convert_alpha()
game_font = pygame.font.Font('asset/font/Snake Chan.ttf', 25) #font(.ttf), font size

SCREEN_UPDATE = pygame.USEREVENT #custom event menggunakan triggger (menggunakan timer)

pygame.time.set_timer(SCREEN_UPDATE,150) #event tertrigger setiap 150ms

main_game = MAIN()

#Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN: #Controller
            if event.key == pygame.K_UP:
                text = smallfont.render('Press and hold h for help', True, color)
                if main_game.snake.direction.y !=1: #supaya tidak bertabrakan dengan badan sendiri
                    main_game.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_DOWN:
                text = smallfont.render('Press and hold h for help', True, color)
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_RIGHT:
                text = smallfont.render('Press and hold h for help', True, color)
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1,0)
            if event.key == pygame.K_LEFT:
                text = smallfont.render('Press and hold h for help', True, color)
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1,0)
            #QUIT game (pake ESC)
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            #PAUSE game (pake P dan Space)
            if event.key == pygame.K_p:
                pygame.time.set_timer(SCREEN_UPDATE, 0)  # buat pause pake P
                main_game.draw_score()
            if event.key == pygame.K_SPACE:
                pygame.time.set_timer(SCREEN_UPDATE, 150)  # buat continue pake space
            #HELP game (pake H)
            if event.key == pygame.K_h:
                # superimposing the text onto our button
                text = smallfont.render('Press p for pause', True, color)
                text2 = smallfont.render('SPACE for continue', True, color)
                text3 = smallfont.render('ESC for quit', True, color)

                screen.blit(text, (1, 4))
                screen.blit(text2, (1, 54))
                screen.blit(text3, (1, 104))
        if event.type == pygame.KEYUP:  # Controller
            if event.key == pygame.K_h:
                # superimposing the text onto our button
                text = smallfont.render('Press and hold h for help', True, color)
                text2 = smallfont.render('', True, color)
                text3 = smallfont.render('', True, color)
                #screen.blit(text, (1, 4))

    screen.fill((175,215,70))

    #main_game.level_speed()
    main_game.draw_elements()
    # tulisan instruksi help
    screen.blit(text, (1, 4))
    screen.blit(text2, (1, 54))
    screen.blit(text3, (1, 104))


    pygame.display.update()
    clock.tick(60) #framerate
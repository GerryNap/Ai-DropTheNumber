import pygame
import random
import math

from pygame import draw, font
from UtilityDLV import UtilityDLV
from Board import Board

COL = 5
ROW = 6
FONT_SIZE = 40
SIZE = 70

# ANIMATION
CONBINE = 1
FALL = 2

class Game:
    def __init__(self, display, stateManager, colors):
        self.display = display
        self.stateManager = stateManager
        self.colors = colors
        self.font = pygame.font.Font('freesansbold.ttf', FONT_SIZE)
        self.board_value = [[0 for i in range(COL)] for j in range(ROW)]
        self.utility = UtilityDLV()
        
        # New block
        self.is_moving = False
        self.moving_xy = [-1, -1]
        self.moving_num = 0
        self.speed = 0.1
        self.add_delay = 10
        self.h_input = 0
        self.h_delay = 0
        self.d_input = 65
        self.next_num = random.randint(1,5)

        # Animation
        self.is_animating = False
        self.animation_type = 0
        self.animation_progress = 0
        self.animation_place = False
        self.animation_directions = []
        self.fall_map = []
        self.animation_stack = []

        self.game_over = False

        # Game Type
        self.ai_game = False 
        self.path = ''

        # Score
        self.score = 0
        self.high_score = 0

        # Buttons
        self.button_rect_restart = pygame.Rect(0, 0, 150, 50)
        self.button_rect_home = pygame.Rect(0, 0, 150, 50)
        self.hover_restart = False
        self.hover_home = False

    def set_ai_game(self, type:bool):
        self.ai_game = type

        if type:
            self.path = 'resources/ai-highscore.txt'
        else:
            self.path = 'resources/highscore.txt'

        file = open(self.path, 'r')
        self.high_score = int(file.readline())
        file.close()

    def draw_txt(self, str:str, x:int, y:int):
        src = self.font.render(str, True, self.colors['light text'])
        self.display.blit(src, [x,y])

    def draw_board_base(self):
        self.display.fill(self.colors['bg'])
        self.draw_txt("NEXT", 450, 20)
        self.draw_txt("SCORE", 435, 150)
        self.draw_txt(str(self.score), 580-self.font.size(str(self.score))[0], 200)
        self.draw_txt("HIGH SCORE", 100, 540)
        self.draw_txt(str(self.high_score), 404, 540)
        if not self.ai_game:
            self.draw_txt("MOVE", 450, 290)
            self.draw_txt("A: LEFT", 420, 345)
            self.draw_txt("D: RIGHT", 420, 395)
            self.draw_txt("S: DOWN", 420, 445)
        pygame.draw.rect(self.display, 'black', [48, 20, 354, 74], 2, 5)
        pygame.draw.rect(self.display, 'dark gray', [50, 22, 350, 70], 0, 5)
        pygame.draw.rect(self.display, 'black', [48, 98, 354, 424], 2, 5)
        pygame.draw.rect(self.display, 'gray', [50, 100, 350, 420], 0, 5)
    
    def draw_block(self, value:int, x:int, y:int):
        block_value = 2**value
        if block_value > 8:
            txt_color = self.colors['light text']
        else:
            txt_color = self.colors['dark text']

        if block_value <= 2048:
            block_color = self.colors[block_value]
        else:
            block_color = self.colors['other']

        pygame.draw.rect(self.display, block_color, [x, y, SIZE, SIZE], 0, 5)
        pygame.draw.rect(self.display, txt_color, [x, y, SIZE, SIZE], 2, 5)
        if value > 0:
            value_len = len(str(block_value))
            font = pygame.font.Font('freesansbold.ttf', 45 - (5 * value_len))
            value_txt = font.render(str(block_value), True, txt_color)
            txt_rect = value_txt.get_rect(center=(x+SIZE/2, y+SIZE/2))
            self.display.blit(value_txt, txt_rect)

    def is_animating_place(self, x:int, y:int) -> bool:
        if self.animation_type == CONBINE:
            if self.animation_directions[0]:
                if  x == self.animation_place[0] - 1 and \
                    y == self.animation_place[1]:
                    return True
            if self.animation_directions[1]:
                if  x == self.animation_place[0] and \
                    y == self.animation_place[1] + 1:
                    return True
            if self.animation_directions[2]:
                if  x == self.animation_place[0] + 1 and \
                    y == self.animation_place[1]:
                    return True
        elif self.animation_type == FALL:
            if self.fall_map[y][x] == 1:
                return True
        return False

    def draw_board(self):
        for y in range(ROW):
            for x in range(COL):
                if self.board_value[y][x] > 0:
                    if self.is_animating and self.is_animating_place(x, y):
                        continue
                    else:
                        self.draw_block(self.board_value[y][x], 50+SIZE*x, 100+SIZE*y)

    def draw_button_restart(self):
        self.button_rect_restart.center = (200, 350)
        button_text = "RESTART"
        font.init()
        font_obj = font.Font(None, 30)

        if self.hover_restart:
            button_color = self.colors[64]
        else:
            button_color = self.colors[2048]

        text_surface = font_obj.render(button_text, True, self.colors['dark text'])
        draw.rect(self.display, button_color, self.button_rect_restart, border_radius=5)
        self.display.blit(text_surface, text_surface.get_rect(center=self.button_rect_restart.center))

    def draw_button_home(self):
        self.button_rect_home.center = (self.display.get_width()-200, 350)
        button_text = "HOME"
        font.init()
        font_obj = font.Font(None, 30)

        if self.hover_home:
            button_color = self.colors[64]
        else:
            button_color = self.colors[2048]

        text_surface = font_obj.render(button_text, True, self.colors['dark text'])
        draw.rect(self.display, button_color, self.button_rect_home, border_radius=5)
        self.display.blit(text_surface, text_surface.get_rect(center=self.button_rect_home.center))

    def draw_game_over(self):
        pygame.draw.rect(self.display, 'black', (100, 200, 420, 200), 0, 10)
        pygame.draw.rect(self.display, self.colors[2048], (100, 200, 420, 200), 4, 10)
        self.draw_txt('GAME OVER', 190, 240)
        self.draw_button_restart()
        self.draw_button_home()

    def start(self):
        self.board_value = [[0 for i in range(COL)] for j in range(ROW)]
        self.is_moving = False
        self.next_num = random.randint(1,5)
        self.h_input = 0
        self.h_delay = 0
        self.d_input = 0
        self.game_over = False
        self.score = 0

    def get_top_y(self, x:int) -> int:
        for y in range(ROW):
            if self.board_value[y][x] > 0:
                return y
        return ROW
    
    def is_fallable(self, x:int, y:int) -> bool:
        for _y in range(y+1, ROW):
            if self.board_value[_y][x] == 0:
                return True
        return False
    
    def update_fall_map(self):
        self.fall_map = [[0 for i in range(COL)] for j in range(ROW)]
        is_falling = False
        for y in range(ROW):
            for x in range(COL):
                if self.board_value[y][x] > 0 and self.is_fallable(x, y):
                    is_falling = True
                    self.fall_map[y][x] = 1

        if is_falling:
            self.is_animating = True
            self.animation_progress = 0
            self.animation_type = FALL

    def check_right(self, x:int, y:int) -> bool:
        value = self.board_value[y][x]
        if y+1 < ROW and value == self.board_value[y+1][x]:
            self.animation_directions[1] = True
        if x+1 < COL and value == self.board_value[y][x+1]:
            self.animation_directions[2] = True
        if self.animation_directions[1] or self.animation_directions[2]:
            self.animation_directions[0] = True
            self.animation_place = [x,y]
            self.is_animating = True
            self.animation_progress = 0
            self.animation_type = CONBINE
            return True
        return False

    def set_animation(self):
        self.animation_directions = [False, False, False]
        for y in range(ROW):
            for x in range(COL):
                value = self.board_value[y][x]
                if value > 0:
                    if x+1 < COL and value == self.board_value[y][x+1]:
                        if self.check_right(x+1, y):
                            return
                        self.animation_directions[2] = True
                    if y+1 < ROW and value == self.board_value[y+1][x]:
                        self.animation_directions[1] = True
                    if self.animation_directions[1] or self.animation_directions[2]:
                        self.animation_place=[x,y]
                        self.is_animating = True
                        self.animation_progress = 0
                        self.animation_type = CONBINE
                        return

    def run(self, events):
        self.draw_board_base()

        if self.game_over:
            for event in events:
                if event.type == pygame.MOUSEMOTION:
                    self.hover_home = self.button_rect_home.collidepoint(event.pos)
                    self.hover_restart = self.button_rect_restart.collidepoint(event.pos)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.hover_home:
                        self.stateManager.set_state('home')
                    else:
                        self.start()
        else:
            if self.h_delay > 0:
                self.h_delay -= -1
            if self.h_delay == 0 and self.is_moving:
                if self.ai_game:
                    if self.moving_xy[0] < self.utility.getSolution():
                        self.h_input += 1
                    elif self.moving_xy[0] > self.utility.getSolution():
                        self.h_input -= 1
                    else:
                        self.d_input = 1
                else:
                    for event in events:
                        if event.type == pygame.KEYUP:
                            if event.key == pygame.K_d:
                                self.h_input += 1
                            elif event.key == pygame.K_a:
                                self.h_input -= 1
                            elif event.key == pygame.K_s:
                                self.d_input = 1

            if not self.is_animating:
                if self.is_moving:
                    if  self.h_input == 1 and \
                        self.moving_xy[0] < COL-1 and \
                        self.moving_xy[1] > -1 and \
                        self.board_value[math.ceil(self.moving_xy[1])][self.moving_xy[0]+1] == 0:

                        self.moving_xy[0] += 1

                    elif    self.h_input == -1 and \
                            self.moving_xy[0] > 0 and \
                            self.moving_xy[1] > -1 and \
                            self.board_value[math.ceil(self.moving_xy[1])][self.moving_xy[0]-1] == 0:
                        
                        self.moving_xy[0] -= 1

                    # pavimento
                    if  self.moving_xy[1] < ROW-1 and \
                        self.board_value[math.floor(self.moving_xy[1])+1][self.moving_xy[0]] == 0:

                        self.moving_xy[1] += self.speed

                        if self.d_input:
                            self.moving_xy[1] += 20
                        self.moving_xy[1] = min(self.moving_xy[1], self.get_top_y(self.moving_xy[0])-1)
                    else:
                        if self.get_top_y(self.moving_xy[0]) > 0:
                            self.board_value[self.moving_xy[1]][self.moving_xy[0]] = self.moving_num
                        else:
                            self.game_over = True
                            if self.score > self.high_score:
                                self.high_score = self.score
                                file = open(self.path, 'w')
                                file.write(f'{self.high_score}')
                                file.close()

                        self.add_delay = 10
                        self.is_moving = False
                else:
                    if self.add_delay > 0:
                        self.add_delay -= 1
                    elif self.add_delay == 0:

                        self.is_moving = True
                        self.moving_num = self.next_num
                        self.next_num = random.randint(1,5)
                        self.moving_xy = [2, -1]

                        # DLV UPDATE
                        if self.ai_game:
                            board = Board(self.board_value, ROW, COL)
                            self.utility.set_facts(board.get_facts(), self.moving_num)
                            self.utility.set_DLV()

            if self.is_animating:
                if self.animation_type == CONBINE:
                    if self.animation_progress < 1:
                        self.animation_progress = min(self.animation_progress+0.1, 1)
                    elif self.animation_progress == 1:
                        if self.animation_directions[0] and self.animation_place[0] -1 >= 0:
                            self.board_value[self.animation_place[1]][self.animation_place[0]] += 1
                            self.board_value[self.animation_place[1]][self.animation_place[0]-1] = 0
                        if self.animation_directions[1] and self.animation_place[1] + 1 < ROW:
                            self.board_value[self.animation_place[1]][self.animation_place[0]] += 1
                            self.board_value[self.animation_place[1]+1][self.animation_place[0]] = 0
                        if self.animation_directions[2] and self.animation_place[0] + 1 < COL:
                            self.board_value[self.animation_place[1]][self.animation_place[0]] += 1
                            self.board_value[self.animation_place[1]][self.animation_place[0]+1] = 0
                        self.score += 2**(self.board_value[self.animation_place[1]][self.animation_place[0]])
                        self.is_animating = False
                        self.update_fall_map()
                        
                elif self.animation_type == FALL:
                    if self.animation_progress < 1:
                        self.animation_progress = min(self.animation_progress+0.1, 1)
                    elif self.animation_progress == 1:
                        for y in range(ROW-1, -1, -1):
                            for x in range(COL):
                                if self.fall_map[y][x] == 1:
                                    self.board_value[y+1][x] = self.board_value[y][x]
                                    self.board_value[y][x] = 0
                            self.is_animating = False
                            self.update_fall_map()
            else:
                self.set_animation()
            
            self.h_input = 0
            self.d_input = 0

            self.draw_board()

            if self.is_moving:
                self.draw_block(self.moving_num, 50+SIZE*self.moving_xy[0], 100+SIZE*self.moving_xy[1])
            if self.is_animating:
                if self.animation_type == CONBINE:
                    x = self.animation_place[0]
                    y = self.animation_place[1]
                    value = self.board_value[y][x]
                    if self.animation_directions[0] and x-1 >= 0:
                        self.draw_block(value, 50+SIZE*(x-1+self.animation_progress), 100+SIZE*y)
                    if self.animation_directions[1] and y+1 < ROW:
                        self.draw_block(value, 50+SIZE*x, 100+SIZE*(y+1-self.animation_progress))
                    if self.animation_directions[2] and x+1 < COL:
                        self.draw_block(value, 50+SIZE*(x+1-self.animation_progress), 100+SIZE*y)
                elif self.animation_type == FALL:
                    for y in range(ROW):
                        for x in range(COL):
                            if self.fall_map[y][x] == 1:
                                self.draw_block(self.board_value[y][x], 50+SIZE*x, 100+SIZE*(y+self.animation_progress))

            self.draw_block(self.next_num, 472, 60)

        if self.game_over:
            self.draw_game_over()
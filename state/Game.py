import pygame
import random
import math
import state.Home as Home

from pygame import draw, font
from UtilityDLV import UtilityDLV
from component.Board import Board
from component.Cell import Cell

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
        self.max_value = 4
        self.next_num = random.randint(1,self.max_value)

        # Animation
        self.is_animating = False
        self.animation_type = 0
        self.animation_progress = 0
        self.animation_place = False
        self.animation_directions = []
        self.fall_map = []
        self.animation_stack = []

        self.game_over = False
        self.pause = False

        # Game Type
        self.ai_game = False 
        self.path = ''

        # Score
        self.score = 0
        self.high_score = 0

        # Buttons
        self.button_rect_restart = pygame.Rect(0, 0, 150, 50)
        self.button_rect_home = pygame.Rect(0, 0, 150, 50)
        self.button_rect_pause = pygame.Rect(0, 0, 180, 50)
        self.button_rect_continue = pygame.Rect(0, 0, 150, 50)
        self.hover_restart = False
        self.hover_home = False
        self.hover_pause = False
        self.hover_continue = False

    def set_home(self, home:Home):
        self.home = home

    def set_ai_game(self, ai_game:bool):
        self.ai_game = ai_game

        if self.ai_game:
            self.path = 'resources/ai-highscore.txt'
        else:
            self.path = 'resources/highscore.txt'

        file = open(self.path, 'r')
        self.high_score = int(file.readline())
        file.close()

    def draw_txt(self, str:str, x:int, y:int, color='light text', size=FONT_SIZE):
        self.font = pygame.font.Font('freesansbold.ttf', size)
        src = self.font.render(str, True, self.colors[color])
        self.display.blit(src, [x,y])

    def draw_rectangle(self, x:int, y:int, size_x:int, size_y:int, color):
        pygame.draw.rect(self.display, 'black', [x-2, y-2, size_x+4, size_y+4], 2, 5)
        pygame.draw.rect(self.display, color, [x, y, size_x, size_y], 0, 5)

    def draw_button_pause(self):
        self.button_rect_pause.center = (508, 496)
        button_text = "PAUSE"
        font.init()
        font_obj = font.Font(None, 30)

        if self.hover_pause and not self.pause:
            button_color = self.colors[2048]
            text_color = self.colors['dark text']
        else:
            button_color = self.colors[64]
            text_color = self.colors['light text']

        shadow_rect = self.button_rect_pause.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        draw.rect(self.display, text_color, shadow_rect, border_radius=5)

        text_surface = font_obj.render(button_text, True, text_color)
        draw.rect(self.display, button_color, self.button_rect_pause, border_radius=5)
        self.display.blit(text_surface, text_surface.get_rect(center=self.button_rect_pause.center))

    def draw_board_base(self):
        self.display.fill(self.colors['bg'])
        
        # GAME BOARD
        self.draw_rectangle(50, 22, 350, 70, 'dark gray')
        self.draw_rectangle(50, 100, 350, 420, 'light gray')
        # NEXT BLOCK
        self.draw_rectangle(420, 22, 180, 70, 'dark gray')
        self.draw_txt("NEXT", 430, 42, 'other', size=30)
        Cell.draw(self.display,self.next_num,530,27,60)
        # LIVE SCORE
        self.draw_rectangle(420, 100, 180, 100, 'dark gray')
        self.draw_txt("SCORE", 440, 110, 'other')
        self.draw_txt(str(self.score), 590-self.font.size(str(self.score))[0], 155)
        # KEYBOARD
        if not self.ai_game:
            self.draw_rectangle(420, 208, 180, 200, 'dark gray')
            self.draw_txt("MOVE", 450, 218, 'other')
            self.draw_txt("A:", 430, 268, color='other',size=35)
            self.draw_txt("LEFT", 480, 268, size=35)
            self.draw_txt("D:", 430, 318, color='other', size=35)
            self.draw_txt("RIGHT", 480, 318, size=35)
            self.draw_txt("S:", 430, 368, color='other', size=35)
            self.draw_txt("DOWN", 480, 368, size=35)
        # PAUSE
        self.draw_button_pause()
        # HIGH SCORE
        self.draw_rectangle(50, 528, 550, 50, 'dark grey')
        self.draw_txt("HIGH SCORE", 100, 535, color='other')
        self.draw_txt(str(self.high_score), 404, 535)

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
                        Cell.draw(self.display,self.board_value[y][x], 50+SIZE*x, 100+SIZE*y, SIZE)

    def draw_button_restart(self):
        self.button_rect_restart.center = (200, 350)
        button_text = "RESTART"
        font.init()
        font_obj = font.Font(None, 30)

        if self.hover_restart:
            button_color = self.colors[64]
            text_color = self.colors['light text']
        else:
            button_color = self.colors[2048]
            text_color = self.colors['dark text']

        shadow_rect = self.button_rect_restart.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        draw.rect(self.display, text_color, shadow_rect, border_radius=5)

        text_surface = font_obj.render(button_text, True, text_color)
        draw.rect(self.display, button_color, self.button_rect_restart, border_radius=5)
        self.display.blit(text_surface, text_surface.get_rect(center=self.button_rect_restart.center))

    def draw_button_home(self):
        self.button_rect_home.center = (self.display.get_width()-200, 350)
        button_text = "HOME"
        font.init()
        font_obj = font.Font(None, 30)

        if self.hover_home:
            button_color = self.colors[64]
            text_color = self.colors['light text']
        else:
            button_color = self.colors[2048]
            text_color = self.colors['dark text']

        shadow_rect = self.button_rect_home.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        draw.rect(self.display, text_color, shadow_rect, border_radius=5)

        text_surface = font_obj.render(button_text, True, text_color)
        draw.rect(self.display, button_color, self.button_rect_home, border_radius=5)
        self.display.blit(text_surface, text_surface.get_rect(center=self.button_rect_home.center))

    def draw_game_over(self):
        pygame.draw.rect(self.display, 'black', (100, 200, 450, 200), 0, 10)
        pygame.draw.rect(self.display, self.colors[2048], (100, 200, 450, 200), 4, 10)
        self.draw_txt('GAME OVER', 190, 240)
        self.draw_button_restart()
        self.draw_button_home()

    def draw_button_continue(self):
        self.button_rect_continue.center = (200, 350)
        button_text = "CONTINUE"
        font.init()
        font_obj = font.Font(None, 30)

        if self.hover_continue:
            button_color = self.colors[64]
            text_color = self.colors['light text']
        else:
            button_color = self.colors[2048]
            text_color = self.colors['dark text']

        shadow_rect = self.button_rect_continue.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        draw.rect(self.display, text_color, shadow_rect, border_radius=5)

        text_surface = font_obj.render(button_text, True, text_color)
        draw.rect(self.display, button_color, self.button_rect_continue, border_radius=5)
        self.display.blit(text_surface, text_surface.get_rect(center=self.button_rect_continue.center))

    def draw_pause(self):
        pygame.draw.rect(self.display, 'black', (100, 200, 450, 200), 0, 10)
        pygame.draw.rect(self.display, self.colors[2048], (100, 200, 450, 200), 4, 10)
        self.draw_txt('PAUSE', 260, 240)
        self.draw_button_continue()
        self.draw_button_home()

    def start(self):
        self.board_value = [[0 for i in range(COL)] for j in range(ROW)]
        self.is_moving = False
        self.next_num = random.randint(1,self.max_value)
        self.h_input = 0
        self.h_delay = 0
        self.d_input = 0
        self.game_over = False
        self.pause = False
        self.score = 0
        self.speed = 0.1
        self.hover_restart = False
        self.hover_home = False
        self.hover_pause = False
        self.hover_continue = False

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
    
    def check_moving(self, x:int) -> bool:
        return x <= self.moving_xy[0]

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
            self.draw_game_over()
            for event in events:
                if event.type == pygame.MOUSEMOTION:
                    self.hover_home = self.button_rect_home.collidepoint(event.pos)
                    self.hover_restart = self.button_rect_restart.collidepoint(event.pos)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.hover_home:
                        self.home.reset()
                        self.stateManager.set_state('home')
                    elif self.hover_restart:
                        self.start()
        else:
            if not self.pause:
                for event in events:
                    if event.type == pygame.MOUSEMOTION:
                        self.hover_pause = self.button_rect_pause.collidepoint(event.pos)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.hover_pause:
                            self.pause = True
            else:
                self.speed = 0
                for event in events:
                    if event.type == pygame.MOUSEMOTION:
                        self.hover_home = self.button_rect_home.collidepoint(event.pos)
                        self.hover_continue = self.button_rect_continue.collidepoint(event.pos)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.hover_home:
                            self.home.reset()
                            self.stateManager.set_state('home')
                        elif self.hover_continue:
                            self.hover_continue = False
                            self.hover_pause = False
                            self.pause = False
                            self.speed = 0.1

            if self.h_delay > 0:
                self.h_delay -= -1
            if self.h_delay == 0 and self.is_moving:
                if self.ai_game and not self.pause:
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
                        self.next_num = random.randint(1,self.max_value)
                        self.moving_xy = [2, -1]

                        # DLV UPDATE
                        if self.ai_game and not self.pause:
                            board = Board(self.board_value)
                            self.utility.set_facts(board.get_cell_facts(), board.get_size_fact(), self.moving_num, self.next_num)
                            self.utility.set_DLV()
            if not self.pause:
                if self.is_animating:
                    if self.animation_type == CONBINE:
                        if self.animation_progress < 1:
                            self.animation_progress = min(self.animation_progress+0.1, 1)
                        elif self.animation_progress == 1:
                            x = self.animation_place[0]
                            y = self.animation_place[1]

                            if self.animation_directions[0] and x-1 >= 0:
                                self.board_value[y][x] += 1
                                self.board_value[y][x-1] = 0
                            if self.animation_directions[1] and y+1 < ROW:
                                self.board_value[y][x] += 1
                                self.board_value[y+1][x] = 0
                            if self.animation_directions[2] and x+1 < COL:
                                self.board_value[y][x] += 1
                                self.board_value[y][x+1] = 0
                            self.score += 2**(self.board_value[y][x])
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
                Cell.draw(self.display,self.moving_num, 50+SIZE*self.moving_xy[0], 100+SIZE*self.moving_xy[1], SIZE)
            if self.is_animating:
                if self.animation_type == CONBINE:
                    x = self.animation_place[0]
                    y = self.animation_place[1]
                    value = self.board_value[y][x]
                    if self.animation_directions[0] and x-1 >= 0:
                        Cell.draw(self.display,value, 50+SIZE*(x-1+self.animation_progress), 100+SIZE*y, SIZE)
                    if self.animation_directions[1] and y+1 < ROW:
                        Cell.draw(self.display,value, 50+SIZE*x, 100+SIZE*(y+1-self.animation_progress), SIZE)
                    if self.animation_directions[2] and x+1 < COL:
                        Cell.draw(self.display,value, 50+SIZE*(x+1-self.animation_progress), 100+SIZE*y, SIZE)
                elif self.animation_type == FALL:
                    for y in range(ROW):
                        for x in range(COL):
                            if self.fall_map[y][x] == 1:
                                Cell.draw(self.display,self.board_value[y][x], 50+SIZE*x, 100+SIZE*(y+self.animation_progress), SIZE)
            if self.pause:
                self.draw_pause()
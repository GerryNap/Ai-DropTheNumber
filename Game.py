import pygame
import random
import math

from UtilityDLV import UtilityDLV
from Board import Board

COL = 5
ROW = 6
FONT_SIZE = 40
SIZE = 70

# ANIMATION
CONBINE = 1
FALL = 2

LEFT = [-1, 0]
RIGHT = [1, 0]
DOWN = [0, 1]

class Game:
    def __init__(self, display, stateManager, colors):
        self.display = display
        self.stateManager = stateManager
        self.colors = colors
        self.font = pygame.font.Font('freesansbold.ttf', FONT_SIZE)
        self.board_value = [[0 for i in range(COL)] for j in range(ROW)]
        self.utility = UtilityDLV()

        #score
        self.score = 0
        file = open('resources/highscore.txt', 'r')
        self.high_score = int(file.readline())
        file.close()
        
        # New block
        self.is_moving = False
        self.moving_xy = [-1, -1]
        self.moving_num = 0
        self.speed = 0.08
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

        self.game_over = False

    def draw_txt(self, str:str, x:int, y:int):
        src = self.font.render(str, True, self.colors['light text'])
        self.display.blit(src, [x,y])

    def draw_board_base(self):
        self.draw_txt("NEXT", 450, 20)
        self.draw_txt("SCORE", 435, 150)
        self.draw_txt(str(self.score), 580-self.font.size(str(self.score))[0], 200)
        self.draw_txt("HIGH SCORE", 100, 540)
        self.draw_txt(str(self.high_score), 404, 540)
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
        

    def draw_board(self):
        for y in range(ROW):
            for x in range(COL):
                if self.board_value[y][x] > 0:
                    if self.is_animating and self.is_animating_place(x, y):
                        continue
                    else:
                        self.draw_block(self.board_value[y][x], 50+SIZE*x, 100+SIZE*y)

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
    
    # Return True if there are 0 blocks below the (x, y) field
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
    
    def set_animation(self):
        for y in range(ROW-1):
            for x in range(COL):
                if  self.board_value[y][x] > 0 and \
                    self.board_value[y][x] == self.board_value[y+1][x]:

                    self.animation_place = [x, y]
                    self.animation_directions = [DOWN]
                    self.is_animating = True
                    self.animation_progress = 0
                    self.animation_type = CONBINE
                    return
        
        for y in range(ROW):
            for x in range(COL-1):
                if  self.board_value[y][x] > 0 and \
                    self.board_value[y][x] == self.board_value[y][x+1]:

                    self.animation_place = [x, y]
                    self.animation_directions = [RIGHT]
                    self.is_animating = True
                    self.animation_progress = 0
                    self.animation_type = CONBINE
                    return

    def is_animating_place(self, x:int, y:int) -> bool:
        if self.animation_type == CONBINE:
            for i in self.animation_directions:
                if  x == self.animation_place[0] + i[0] and \
                    y == self.animation_place[1] + i[1]:
                    return True
        elif self.animation_type == FALL:
            if self.fall_map[y][x] == 1:
                return True
        return False

    def run(self, events):
        self.display.fill(self.colors['bg'])
        self.draw_board_base()

        if self.h_delay > 0:
            self.h_delay -= -1
        if self.h_delay == 0 and self.is_moving:
            if self.moving_xy[0] < self.utility.getSolution():
                self.h_input += 1
            elif self.moving_xy[0] > self.utility.getSolution():
                self.h_input -= 1
            else:
                self.d_input = 1

        if self.game_over:
            for event in events:
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RETURN:
                        self.start()
        else:
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
                                file = open('resources/highscore.txt', 'w')
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
                        board = Board(self.board_value, ROW, COL)
                        self.utility.set_facts(board.get_facts(), self.moving_num)
                        self.utility.set_DLV()

            if self.is_animating:
                if self.animation_type == CONBINE:
                    if self.animation_progress < 1:
                        self.animation_progress = min(self.animation_progress+0.05, 1)
                    elif self.animation_progress == 1:
                        for i in self.animation_directions:
                            self.board_value[self.animation_place[1]][self.animation_place[0]] += 1
                            self.board_value[self.animation_place[1]+i[1]][self.animation_place[0]+i[0]] = 0
                            self.score += 2**(self.board_value[self.animation_place[1]][self.animation_place[0]]-1)
                        self.is_animating = False
                        self.update_fall_map()
                        
                elif self.animation_type == FALL:
                    if self.animation_progress < 1:
                        self.animation_progress = min(self.animation_progress+0.05, 1)
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
                for i in self.animation_directions:
                    _x = self.animation_place[0] + i[0]
                    _y = self.animation_place[1] + i[1]
                    self.draw_block(self.board_value[_y][_x], 50+SIZE*_x-i[0]*self.animation_progress, 100+SIZE*(_y-i[1]*self.animation_progress))
            elif self.animation_type == FALL:
                for y in range(ROW):
                    for x in range(COL):
                        if self.fall_map[y][x] == 1:
                            self.draw_block(self.board_value[y][x], 50+SIZE*x, 100+SIZE*(y+self.animation_progress))
        self.draw_block(self.next_num, 472, 60)

        if self.game_over:
            pygame.draw.rect(self.display, 'black', (20, 260, 430, 110))
            self.draw_txt('GAME OVER', 150, 270)
            self.draw_txt('PRESS "ENTER"\nTO RESTART', 30, 330)
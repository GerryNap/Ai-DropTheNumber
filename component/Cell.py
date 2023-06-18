import pygame 

from component.Color import Color

class Cell:
    def draw(screen,value: int, x:int, y:int, size:int):
        block_value = 2**value
        if block_value > 8:
            txt_color = Color.get('light')
        else:
            txt_color = Color.get('dark')

        if block_value <= 2048:
            block_color = Color.get(block_value)
        else:
            block_color = Color.get('other')

        pygame.draw.rect(screen, block_color,[x,y,size,size],0,5)
        pygame.draw.rect(screen,txt_color,[x,y,size,size],2,5)

        if value > 0:
            value_len = len(str(block_value))
            font = pygame.font.Font('freesansbold.ttf', 45 - (5 * value_len))
            value_txt = font.render(str(block_value), True, txt_color)
            txt_rect = value_txt.get_rect(center=(x+size/2, y+size/2))
            screen.blit(value_txt, txt_rect)

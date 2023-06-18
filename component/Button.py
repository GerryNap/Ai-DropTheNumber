import pygame
from component.Color import Color

def draw(screen:pygame.display,rect:pygame.Rect,text,b_color,t_color):
    pygame.font.init()
    font_obj = pygame.font.Font(None, 30)
    shadow_rect = rect.copy()
    shadow_rect.x += 2
    shadow_rect.y += 2

    pygame.draw.rect(screen, t_color, shadow_rect, border_radius=5)

    text_surface = font_obj.render(text,True,t_color)
    pygame.draw.rect(screen,b_color,rect,border_radius=5)
    screen.blit(text_surface,text_surface.get_rect(center=rect.center))

class Button:
    def draw_dark(screen:pygame.display,rect:pygame.Rect,text,hover,width,height):
        if hover:
            button_color = Color.get(2048)
            text_color = Color.get('dark')
        else:
            button_color = Color.get('other')
            text_color = Color.get('light')

        rect.center = (width, height)
        draw(screen,rect,text,button_color,text_color)

    def draw_light(screen:pygame.display,rect:pygame.Rect,text,hover,width,height):
        if hover:
            button_color = Color.get(64)
            text_color = Color.get('light')
        else:
            button_color = Color.get(2048)
            text_color = Color.get('dark')

        rect.center = (width, height)
        draw(screen,rect,text,button_color,text_color)

    def draw_red(screen:pygame.display,rect:pygame.Rect,text,hover,width,height):
        if hover:
            button_color = Color.get(2048)
            text_color = Color.get('dark')
        else:
            button_color = Color.get(64)
            text_color = Color.get('light')

        rect.center = (width, height)
        draw(screen,rect,text,button_color,text_color)
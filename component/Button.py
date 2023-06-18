import pygame
from component.Color import Color

class Button:
    def draw(screen:pygame.display,rect:pygame.Rect,text,hover,width,height):
        rect.center = (width, height)

        pygame.font.init()
        font_obj = pygame.font.Font(None, 30)

        if hover:
            button_color = Color.get(2048)
            text_color = Color.get('dark')
        else:
            button_color = Color.get('other')
            text_color = Color.get('light')

        shadow_rect = rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2

        pygame.draw.rect(screen, text_color, shadow_rect, border_radius=5)

        text_surface = font_obj.render(text,True,text_color)
        pygame.draw.rect(screen,button_color,rect,border_radius=5)
        screen.blit(text_surface,text_surface.get_rect(center=rect.center))
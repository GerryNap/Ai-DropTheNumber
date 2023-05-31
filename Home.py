import pygame
from pygame import font, draw

class Home:
    def __init__(self, display, stateManager, colors):
        self.display = display
        self.stateManager = stateManager
        self.button_rect = pygame.Rect(0, 0, 200, 50)
        self.button_rect.center = (self.display.get_width() // 2, self.display.get_height() // 2)
        self.button_text = "START"
        self.font_size = 30
        self.hover = False
        self.title_text = "Drop the Number"
        self.title_font_size = 60
        self.colors = colors

    def draw_title(self):
        title_font = pygame.font.Font(None, self.title_font_size)
        title_surface = title_font.render(self.title_text, True, self.colors['light text'])
        title_rect = title_surface.get_rect(center=(self.display.get_width() // 2, self.display.get_height() // 4))
        self.display.blit(title_surface, title_rect)


    def draw_button(self):
        font.init()
        font_obj = font.Font(None, self.font_size)

        if self.hover:
            button_color = self.colors[2048]
            text_color = self.colors['dark text']
        else:
            button_color = self.colors['other']
            text_color = self.colors['light text']

        text_surface = font_obj.render(self.button_text, True, text_color)
        draw.rect(self.display, button_color, self.button_rect, border_radius=5)
        self.display.blit(text_surface, text_surface.get_rect(center=self.button_rect.center))

    def run(self, events):
        self.display.fill(self.colors['bg'])
        self.draw_title()
        self.draw_button()

        for event in events:
            if event.type == pygame.MOUSEMOTION:
                if self.button_rect.collidepoint(event.pos):
                    self.hover = True
                else:
                    self.hover = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.hover:
                    self.stateManager.set_state('game')
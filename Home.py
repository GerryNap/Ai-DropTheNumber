import pygame
from pygame import font, draw
from component.Color import Color
import Game

class Home:
    def __init__(self, display, stateManager, game:Game):
        self.display = display
        self.stateManager = stateManager
        self.font_size = 30
        self.title_text = "Drop the Number"
        self.title_font_size = 60
        self.game = game

        self.hover_start = False
        self.hover_play = False
        self.button_rect_start = pygame.Rect(0, 0, 200, 50)
        self.button_rect_play = pygame.Rect(0, 0, 200, 50)

    def draw_title(self):
        title_font = pygame.font.Font(None, self.title_font_size)
        title_surface = title_font.render(self.title_text, True, Color.get('light'))
        title_rect = title_surface.get_rect(center=(self.display.get_width() // 2, self.display.get_height() // 4))
        self.display.blit(title_surface, title_rect)

    def draw_button_start(self):
        self.button_rect_start.center = (self.display.get_width() // 2, self.display.get_height() // 2)
        button_text = "START"
        font.init()
        font_obj = font.Font(None, self.font_size)

        if self.hover_start:
            button_color = Color.get(2048)
            text_color = Color.get('dark')
        else:
            button_color = Color.get('other')
            text_color = Color.get('light')

        shadow_rect = self.button_rect_start.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        draw.rect(self.display, text_color, shadow_rect, border_radius=5)

        text_surface = font_obj.render(button_text, True, text_color)
        draw.rect(self.display, button_color, self.button_rect_start, border_radius=5)
        self.display.blit(text_surface, text_surface.get_rect(center=self.button_rect_start.center))

    def draw_button_play(self):
        self.button_rect_play.center = (self.display.get_width() // 2, self.display.get_height() // 2 + 70)
        button_play_text = "PLAY"

        font.init()
        font_obj = font.Font(None, self.font_size)

        if self.hover_play:
            button_color = Color.get(2048)
            text_color = Color.get('dark')
        else:
            button_color = Color.get('other')
            text_color = Color.get('light')

        shadow_rect = self.button_rect_play.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        draw.rect(self.display, text_color, shadow_rect, border_radius=5)

        text_surface = font_obj.render(button_play_text, True, text_color)
        draw.rect(self.display, button_color, self.button_rect_play, border_radius=5)
        self.display.blit(text_surface, text_surface.get_rect(center=self.button_rect_play.center))

    def reset(self):
        self.hover_play = False
        self.hover_start = False

    def run(self, events):
        self.display.fill(Color.get('bg'))
        self.draw_title()
        self.draw_button_start()
        self.draw_button_play()

        for event in events:
            if event.type == pygame.MOUSEMOTION:
                self.hover_start = self.button_rect_start.collidepoint(event.pos)
                self.hover_play = self.button_rect_play.collidepoint(event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.hover_start:
                    self.game.set_ai_game(True)
                    self.game.start()
                    self.stateManager.set_state('game')
                if self.hover_play:
                    self.game.set_ai_game(False)
                    self.game.start()
                    self.stateManager.set_state('game')
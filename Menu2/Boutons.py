
import pygame
white = (255, 255, 255)
class Boutton:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.font = pygame.font.SysFont(None, 24)
        self.label = self.font.render(text, True, white)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        surface.blit(self.label, (
            self.rect.centerx - self.label.get_width() // 2, self.rect.centery - self.label.get_height() // 2))


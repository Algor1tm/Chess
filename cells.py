import pygame

W, H = 660, 650
SCREEN = pygame.display.set_mode((W, H))
BLACK = (121, 105, 88)
WHITE = (238, 222, 206)

bP = pygame.image.load('figures/small/bP.png')
bK = pygame.image.load('figures/small/bK.png')
bQ = pygame.image.load('figures/small/bQ.png')
bR = pygame.image.load('figures/small/bR.png')
bB = pygame.image.load('figures/small/bB.png')
bN = pygame.image.load('figures/small/bN.png')

wP = pygame.image.load('figures/small/wP.png')
wK = pygame.image.load('figures/small/wK.png')
wQ = pygame.image.load('figures/small/wQ.png')
wR = pygame.image.load('figures/small/wR.png')
wB = pygame.image.load('figures/small/wB.png')
wN = pygame.image.load('figures/small/wN.png')

class Cell:
    size = 75

    def __init__(self, color, pos, id_='00'):
        self.id = id_
        self.color = color
        self.clr_possible = [(156, 194, 135), (98, 157, 102)]
        self.x = pos[0]
        self.y = pos[1]
        self.rect = (self.x, self.y, self.size, self.size)
        self.figure = 'None'

    def show_figure(self, name):
        if isinstance(name, str):
            self.figure = name
        elif isinstance(name, Cell):
            self.figure = name.figure
        SCREEN.blit(eval(self.figure), (self.x + 3, self.y + 3))
        pygame.display.update()

    def clear_figure(self):
        self.figure = 'None'
        SCREEN.fill(self.color, self.rect)
        pygame.display.update()

    def __repr__(self):
        return f"{self.id}, {self.figure}"  # "ABCDEFGH".index(self.id[0]) + 8 * (int(self.id[1]) - 1))

    def show_possible_move(self):
        if self.color == WHITE:
            color = self.clr_possible[0]
        else:
            color = self.clr_possible[1]
        if self.figure == 'None':
            pygame.draw.circle(SCREEN, self.clr_possible[1],
                               (self.x + self.size / 2, self.y + self.size / 2), 10)
        else:
            pygame.draw.polygon(SCREEN, color, ((self.x, self.y),
                                                (self.x + self.size / 6, self.y),
                                                (self.x, self.y + self.size / 6)))
            pygame.draw.polygon(SCREEN, color, ((self.x + self.size - 1, self.y),
                                                (self.x + 5 * self.size / 6, self.y),
                                                (self.x + self.size - 1, self.y + self.size / 6)))
            pygame.draw.polygon(SCREEN, color, ((self.x, self.y + self.size - 1),
                                                (self.x + self.size / 6, self.y + self.size - 1),
                                                (self.x, self.y + 5 * self.size / 6)))
            pygame.draw.polygon(SCREEN, color, ((self.x + self.size - 1, self.y + self.size - 1),
                                                (self.x + 5 * self.size / 6, self.y + self.size - 1),
                                                (self.x + self.size - 1, self.y + 5 * self.size / 6)))
        pygame.display.update()

    def clear_possible_move(self, last=False):
        if last is False:
            color = self.color
        else:
            color = last
        if self.figure == 'None':
            SCREEN.fill(self.color, self.rect)
        else:
            pygame.draw.polygon(SCREEN, color, ((self.x, self.y),
                                                (self.x + self.size / 6, self.y),
                                                (self.x, self.y + self.size / 6)))
            pygame.draw.polygon(SCREEN, color, ((self.x + self.size - 1, self.y),
                                                (self.x + 5 * self.size / 6, self.y),
                                                (self.x + self.size - 1, self.y + self.size / 6)))
            pygame.draw.polygon(SCREEN, color, ((self.x, self.y + self.size - 1),
                                                (self.x + self.size / 5, self.y + self.size - 1),
                                                (self.x, self.y + 5 * self.size / 6)))
            pygame.draw.polygon(SCREEN, color, ((self.x + self.size - 1, self.y + self.size - 1),
                                                (self.x + 5 * self.size / 6, self.y + self.size - 1),
                                                (self.x + self.size - 1, self.y + 5 * self.size / 6)))
        pygame.display.update()

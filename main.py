import pygame
from moves import PossibleMoves
from start_screen import draw_screen, SCREEN, Cell, WHITE

pygame.init()
bQ = pygame.image.load('figures/normal/bQ.png')
bR = pygame.image.load('figures/normal/bR.png')
bB = pygame.image.load('figures/normal/bB.png')
bN = pygame.image.load('figures/normal/bN.png')

wQ = pygame.image.load('figures/normal/wQ.png')
wR = pygame.image.load('figures/normal/wR.png')
wB = pygame.image.load('figures/normal/wB.png')
wN = pygame.image.load('figures/normal/wN.png')

beat = pygame.mixer.Sound('audio/beat.wav')
step = pygame.mixer.Sound('audio/step.wav')

class Game:
    field = None
    possibles = []
    cell1 = None
    cell2 = None
    pawn = None
    last_step = [0, 0]
    history = []
    clr_last_step = [(171, 181, 108), (129, 148, 69)]
    clr_select = (98, 157, 102)
    cast = {'wO-O': True, 'wO-O-O': True, 'bO-O': True, 'bO-O-O': True}

    def __init__(self):
        self.run = True
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.player = 'w'
        self.mode = 'play'
        print('   white               black')

    def start(self):
        self.field = draw_screen()
        while self.run:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.click(pos)
                if event.type == pygame.QUIT:
                    self.run = False

    def click(self, pos):
        if self.mode == 'choice':
            self.change_figure(pos)

        elif pygame.Rect(630, 310, 30, 30).collidepoint(pos):
            self.step_back()

        elif self.mode == 'play':
            self.click_on_field(pos)

        pygame.draw.rect(SCREEN, (0, 0, 0),
                         (30, 25, 8 * Cell.size, 8 * Cell.size),
                         width=1)
        pygame.display.update()

    def click_on_field(self, pos):
        for _cell in self.field.values():
            if pygame.Rect(_cell.rect).collidepoint(pos):
                cell = _cell
                break
        else:
            return None

        if cell.id in self.possibles:
            self.step(cell)

        elif self.cell1 == cell or (cell.figure == 'None' and self.cell1 is not None):
            self.unselect_figure()

        elif cell.figure != 'None' and cell.figure[0] == self.player:
            self.select_figure(cell)

    def select_figure(self, cell):
        for id_ in self.possibles:
            if self.field[id_] in self.last_step:
                self.field[id_].clear_possible_move(True)
            else:
                self.field[id_].clear_possible_move()
            if self.field[id_] in self.last_step:
                self.show_last_step()
        if self.cell1 in self.last_step:
            self.show_last_step()
        elif self.cell1 is not None:
            pygame.draw.rect(SCREEN, self.cell1.color,
                             (self.cell1.x, self.cell1.y, self.cell1.size, self.cell1.size))
            self.cell1.show_figure(self.cell1.figure)
        pygame.draw.rect(SCREEN, self.clr_select, (cell.x, cell.y, cell.size, cell.size))
        cell.show_figure(cell.figure)
        self.cell1 = cell
        self.possible_steps()

    def unselect_figure(self):
        for id_ in self.possibles:
            if self.field[id_] in self.last_step:
                if self.field[id_].color == WHITE:
                    self.field[id_].clear_possible_move(self.clr_last_step[0])
                else:
                    self.field[id_].clear_possible_move(self.clr_last_step[1])
            else:
                self.field[id_].clear_possible_move()
            if self.field[id_] in self.last_step:
                self.show_last_step()
        if self.last_step[1] == self.cell1:

            self.show_last_step()
        else:
            pygame.draw.rect(SCREEN, self.cell1.color,
                             (self.cell1.x, self.cell1.y, self.cell1.size, self.cell1.size))
        if self.cell1.figure != 'None':
            self.cell1.show_figure(self.cell1.figure)
        self.possibles = []
        self.cell1 = None

    def step(self, cell):
        self.legal_cast()

        self.cell2 = cell
        for id_ in self.possibles:
            self.field[id_].clear_possible_move()
            if self.field[id_] in self.last_step:
                self.show_last_step()
        self.possibles = []

        self.castling()

        if self.cell2.figure != 'None':
            beat.play()
            f = self.cell2.figure
            self.cell2.clear_figure()
        else:
            step.play()
            f = 'None'
        self.cell2.show_figure(self.cell1.figure)
        self.cell1.clear_figure()

        self.history.append([self.last_step[0], self.last_step[1], self.cell1, self.cell2, f])

        if isinstance(self.last_step[1], Cell):
            self.clear_last_step()
            self.show_last_step()
        else:
            self.last_step = [self.cell1, self.cell2]
            self.show_last_step()

        if self.cell2.id[1] == '8' and self.cell2.figure == 'wP':
            self.figure_choice('w')
            self.pawn = self.cell2
            self.mode = 'choice'
        elif self.cell2.id[1] == '1' and self.cell2.figure == 'bP':
            self.figure_choice('b')
            self.pawn = self.cell2
            self.mode = 'choice'

        self.note_step()

        self.check_result()

        self.cell1 = None
        self.cell2 = None

        if self.player == 'w':
            self.player = 'b'
        else:
            self.player = 'w'

    def check_result(self):
        pm = PossibleMoves(self.field, self.cast)
        clr = 'w' if self.player == 'b' else 'b'
        for cell in self.field.values():
            if cell.figure[0] == clr:
                if len(pm(cell)) != 0:
                    break
        else:
            king = '00'
            for cell in self.field.values():
                if cell.figure == clr + 'K':
                    king = cell.id
                    break
            for cell in self.field.values():
                if cell.figure[0] == self.player:
                    if king in pm(cell):
                        print('\nWHITE' if self.player == 'w' else '\nBLACK', 'WIN')
                        break
            else:
                print('DRAW')
            self.mode = 'stop'

    def step_back(self):
        if len(self.history) > 0:
            h = self.history.pop()
            pygame.draw.rect(SCREEN, h[2].color, h[2].rect)
            h[2].show_figure(h[3].figure)
            h[3].clear_figure()
            if h[4] != 'None':
                h[3].show_figure(h[4])
            self.last_step = [h[0], h[1]]
            if isinstance(self.last_step[1], Cell):
                self.show_last_step()
            if self.player == 'w':
                self.player = 'b'
            else:
                self.player = 'w'
            if self.mode == 'stop':
                self.mode = 'play'

    def note_step(self):
        if self.player == 'w':
            if self.cell1.id == 'E1' and self.cell2.id == 'G1' and self.cell2.figure == 'wK':
                print('    O-O   ', end='          ')
            elif self.cell1.id == 'E1' and self.cell2.id == 'C1' and self.cell2.figure == 'wK':
                print('   O-O-O   ', end='         ')
            else:
                print(f'{self.cell2.figure[1]}  {self.cell1.id} - {self.cell2.id}', end='          ')
        else:
            if self.cell1.id == 'E8' and self.cell2.id == 'G8' and self.cell2.figure == 'bK':
                print('    O-O   ')
            elif self.cell1.id == 'E8' and self.cell2.id == 'C8' and self.cell2.figure == 'bK':
                print('   O-O-O   ')
            else:
                print(f'{self.cell2.figure[1]}  {self.cell1.id} - {self.cell2.id}')

    def castling(self):
        if self.cell1.id == 'E1' and self.cell2.id == 'G1' and self.cell1.figure == 'wK':
            self.field['F1'].show_figure('wR')
            self.field['H1'].clear_figure()
        elif self.cell1.id == 'E1' and self.cell2.id == 'C1' and self.cell1.figure == 'wK':
            self.field['D1'].show_figure('wR')
            self.field['A1'].clear_figure()
        if self.cell1.id == 'E8' and self.cell2.id == 'G8' and self.cell1.figure == 'bK':
            self.field['F8'].show_figure('bR')
            self.field['H8'].clear_figure()
        elif self.cell1.id == 'E8' and self.cell2.id == 'C8' and self.cell1.figure == 'bK':
            self.field['D8'].show_figure('bR')
            self.field['A8'].clear_figure()

    def legal_cast(self):
        if self.cell1.id == 'A1':
            self.cast['wO-O-O'] = False
        elif self.cell1.id == 'H1':
            self.cast['wO-O'] = False
        elif self.cell1.id == 'E1':
            self.cast['wO-O'] = False
            self.cast['wO-O-O'] = False
        elif self.cell1.id == 'E8':
            self.cast['bO-O'] = False
            self.cast['bO-O-O'] = False
        elif self.cell1.id == 'A8':
            self.cast['bO-O-O'] = False
        elif self.cell1.id == 'H8':
            self.cast['bO-O'] = False

    def clear_last_step(self):
        pygame.draw.rect(SCREEN, self.last_step[0].color,
                         (self.last_step[0].x, self.last_step[0].y,
                          self.last_step[0].size, self.last_step[0].size))
        if self.last_step[0].figure != 'None':
            self.last_step[0].show_figure(self.last_step[0].figure)
        pygame.draw.rect(SCREEN, self.last_step[1].color,
                         (self.last_step[1].x, self.last_step[1].y,
                          self.last_step[1].size, self.last_step[1].size))
        if self.last_step[1].figure != 'None':
            self.last_step[1].show_figure(self.last_step[1].figure)
        self.last_step = [self.cell1, self.cell2]

    def show_last_step(self):
        if self.last_step[0].color == WHITE:
            color = self.clr_last_step[0]
        else:
            color = self.clr_last_step[1]
        pygame.draw.rect(SCREEN, color,
                         (self.last_step[0].x, self.last_step[0].y,
                          self.last_step[0].size, self.last_step[0].size))
        if self.last_step[1].color == WHITE:
            color = self.clr_last_step[0]
        else:
            color = self.clr_last_step[1]
        pygame.draw.rect(SCREEN, color,
                         (self.last_step[1].x, self.last_step[1].y,
                          self.last_step[1].size, self.last_step[1].size))
        self.last_step[1].show_figure(self.last_step[1].figure)

    def possible_steps(self):
        pm = PossibleMoves(self.field, self.cast)
        self.possibles = pm(self.cell1)
        for id_ in self.possibles:
            cell = self.field[id_]
            if cell in self.last_step:
                figure = cell.figure
                cell.clear_figure()
                if figure != 'None':
                    cell.show_figure(figure)
            cell.show_possible_move()

    def change_figure(self, pos):
        x, y = 105, 265
        if pygame.Rect((x, y, 450, 120)).collidepoint(pos):
            self.clear_choice()
            self.mode = 'play'
            clr = self.pawn.figure[0]
            if self.pawn.color == WHITE:
                color = self.clr_last_step[0]
            else:
                color = self.clr_last_step[1]
            if pygame.Rect(x, y, 115, 120).collidepoint(pos):
                pygame.draw.rect(SCREEN, color, self.pawn.rect)
                self.pawn.show_figure(clr + 'Q')
            elif pygame.Rect(x + 115, y, 115, 120).collidepoint(pos):
                pygame.draw.rect(SCREEN, color, self.pawn.rect)
                self.pawn.show_figure(clr + 'B')
            elif pygame.Rect(x + 230, y, 115, 120).collidepoint(pos):
                pygame.draw.rect(SCREEN, color, self.pawn.rect)
                self.pawn.show_figure(clr + 'N')
            elif pygame.Rect(x + 345, y, 450, 115).collidepoint(pos):
                pygame.draw.rect(SCREEN, color, self.pawn.rect)
                self.pawn.show_figure(clr + 'R')

    def clear_choice(self):
        l = 'BCDEFGBCDEFG'
        for i in range(len(l)):
            if i < 6:
                id_ = l[i] + '4'
            else:
                id_ = l[i] + '5'
            cell = self.field[id_]
            if cell.figure == 'None':
                pygame.draw.rect(SCREEN, cell.color, cell.rect)
            else:
                pygame.draw.rect(SCREEN, cell.color, cell.rect)
                cell.show_figure(cell.figure)

    @staticmethod
    def figure_choice(clr, x=105, y=265):
        rect = (x, y, 450, 120)
        pygame.draw.rect(SCREEN, (215, 188, 159), rect)
        if clr == 'w':
            SCREEN.blit(wQ, (x + 20, y + 20))
            SCREEN.blit(wB, (x + 35 + 100, y + 20))
            SCREEN.blit(wN, (x + 48 + 200, y + 20))
            SCREEN.blit(wR, (x + 58 + 300, y + 20))
        else:
            SCREEN.blit(bQ, (x + 20, y + 20))
            SCREEN.blit(bB, (x + 35 + 100, y + 20))
            SCREEN.blit(bN, (x + 48 + 200, y + 20))
            SCREEN.blit(bR, (x + 58 + 300, y + 20))
        pygame.draw.rect(SCREEN, (0, 0, 0), rect, width=1)
        for i in range(1, 4):
            pygame.draw.line(SCREEN, (0, 0, 0), (rect[0] + i * 115, rect[1]),
                             (rect[0] + i * 115, rect[1] + rect[3] - 1))
        pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.start()

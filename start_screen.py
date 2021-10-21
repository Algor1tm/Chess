import pygame
from cells import Cell, H, SCREEN, BLACK, WHITE

reset_button = pygame.image.load('reset.png')
pygame.init()
pygame.display.set_caption('CheSs')

def draw_screen():
    color = (215, 188, 159)
    SCREEN.fill(color)
    font = pygame.font.SysFont('arial', 13)
    letters = 'ABCDEFGH'
    size = 75

    # borders
    x = 62.5
    y = 55
    for l in letters:
        i = letters.index(l)
        follow = font.render(l, True, (0, 0, 0))
        SCREEN.blit(follow, (x + size * i, H - 25))
        follow = font.render(str(8 - i), True, (0, 0, 0))
        SCREEN.blit(follow, (15, y + size * i))

    # field
    field = dict()
    for l in letters:
        for i in range(1, 9):
            id_ = letters[i - 1] + str(letters.index(l) + 1)
            j = letters.index(l) + 1
            if (i + j) % 2 == 1:
                color = WHITE
            else:
                color = BLACK
            x = i * size - 45
            y = H - 25 - j * size
            cell = Cell(color, (x, y), id_)
            field.update({id_: cell})
            pygame.draw.rect(SCREEN, color, (x, y, size, size))
    pygame.draw.rect(SCREEN, (0, 0, 0), (30, 25, 8 * size, 8 * size), width=1)
    pygame.display.update()

    SCREEN.blit(reset_button, (630, 310))
    pygame.display.update()

    # figures
    for l in letters:
        field[l + '7'].show_figure('bP')
        field[l + '2'].show_figure('wP')

    field['E8'].show_figure('bK')
    field['D8'].show_figure('bQ')
    field['C8'].show_figure('bB')
    field['F8'].show_figure('bB')
    field['B8'].show_figure('bN')
    field['G8'].show_figure('bN')
    field['A8'].show_figure('bR')
    field['H8'].show_figure('bR')

    field['E1'].show_figure('wK')
    field['D1'].show_figure('wQ')
    field['C1'].show_figure('wB')
    field['F1'].show_figure('wB')
    field['B1'].show_figure('wN')
    field['G1'].show_figure('wN')
    field['A1'].show_figure('wR')
    field['H1'].show_figure('wR')

    pygame.display.update()
    return field

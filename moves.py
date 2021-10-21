from copy import deepcopy

class PossibleMoves:
    def __init__(self, field, cast):
        self.letters = 'ABCDEFGH'
        self.field = [i for i in field.values()]
        self.cell = None
        self.id_cell = None
        self.cast = cast

    def __call__(self, cell, field=None, is_num=False):
        if field is not None:
            self.field = field
        self.cell = cell
        self.id_cell = self.letters.index(self.cell.id[0]) + 8 * (int(self.cell.id[1]) - 1)
        figure = self.cell.figure
        if figure == 'bP':
            return self.black_pawn(is_num)
        elif figure == 'wP':
            return self.white_pawn(is_num)
        elif figure[1] == 'Q':
            return self.queen(is_num)
        elif figure[1] == 'R':
            return self.rook(is_num)
        elif figure[1] == 'B':
            return self.bishop(is_num)
        elif figure[1] == 'N':
            return self.horse(is_num)
        elif figure == 'wK':
            return self.w_castling(is_num) + self.king(is_num)
        elif figure == 'bK':
            return self.b_castling(is_num) + self.king(is_num)


    def black_pawn(self, is_num):
        res = []
        if self.id_cell < 56:
            if self.field[self.id_cell - 8].figure == 'None':
                res.append(self.id_cell - 8)
                if 47 < self.id_cell < 56 and self.field[self.id_cell - 16].figure == 'None':
                    res.append(self.id_cell - 16)
            if self.id_cell % 8 != 7 and self.field[self.id_cell - 7].figure != 'None':
                if self.cell.figure[0] != self.field[self.id_cell - 7].figure[0]:
                    res.append(self.id_cell - 7)
            if self.id_cell % 8 != 0 and self.field[self.id_cell - 9].figure != 'None':
                if self.cell.figure[0] != self.field[self.id_cell - 9].figure[0]:
                    res.append(self.id_cell - 9)
        if is_num:
            return res
        res = self.remove_move_to_lose(res)
        return self.num_to_id(res)


    def white_pawn(self, is_num):
        res = []
        if self.id_cell < 56:
            if self.field[self.id_cell + 8].figure == 'None':
                res.append(self.id_cell + 8)
                if 7 < self.id_cell < 16 and self.field[self.id_cell + 16].figure == 'None':
                    res.append(self.id_cell + 16)
            if self.id_cell % 8 != 0 and self.field[self.id_cell + 7].figure != 'None':
                if self.cell.figure[0] != self.field[self.id_cell + 7].figure[0]:
                    res.append(self.id_cell + 7)
            if self.id_cell % 8 != 7 and self.field[self.id_cell + 9].figure != 'None':
                if self.cell.figure[0] != self.field[self.id_cell + 9].figure[0]:
                    res.append(self.id_cell + 9)
        if is_num:
            return res
        res = self.remove_move_to_lose(res)
        return self.num_to_id(res)

    def rook(self, is_num):
        res = []
        i = 1
        while (self.id_cell - i) % 8 != 7 and -1 < (self.id_cell - i) < 64:
            if self.field[self.id_cell - i].figure == 'None':
                res.append(self.id_cell - i)
                i += 1
            else:
                if self.field[self.id_cell - i].figure[0] != self.cell.figure[0]:
                    res.append(self.id_cell - i)
                break
        i = 1
        while (self.id_cell + i) % 8 != 0 and -1 < (self.id_cell + i) < 64:
            if self.field[self.id_cell + i].figure == 'None':
                res.append(self.id_cell + i)
                i += 1
            else:
                if self.field[self.id_cell + i].figure[0] != self.cell.figure[0]:
                    res.append(self.id_cell + i)
                break
        i = 1
        while (self.id_cell - i * 8) > -1:
            if self.field[self.id_cell - i * 8].figure == 'None':
                res.append(self.id_cell - i * 8)
                i += 1
            else:
                if self.field[self.id_cell - i * 8].figure[0] != self.cell.figure[0]:
                    res.append(self.id_cell - i * 8)
                break
        i = 1
        while (self.id_cell + i * 8) < 64:
            if self.field[self.id_cell + i * 8].figure == 'None':
                res.append(self.id_cell + i * 8)
                i += 1
            else:
                if self.field[self.id_cell + i * 8].figure[0] != self.cell.figure[0]:
                    res.append(self.id_cell + i * 8)
                break
        if is_num:
            return res
        res = self.remove_move_to_lose(res)
        return self.num_to_id(res)

    def queen(self, is_num):
        res = self.bishop(is_num) + self.rook(is_num)
        return res

    def bishop(self, is_num):
        res = []
        i = 1
        while (self.id_cell + 7 * i) % 8 != 7 and -1 < (self.id_cell + 7 * i) < 64:
            if self.field[self.id_cell + 7 * i].figure == 'None':
                res.append(self.id_cell + 7 * i)
                i += 1
            else:
                if self.field[self.id_cell + 7 * i].figure[0] != self.cell.figure[0]:
                    res.append(self.id_cell + 7 * i)
                break
        i = 1
        while (self.id_cell + 9 * i) % 8 != 0 and -1 < (self.id_cell + 9 * i) < 64:
            if self.field[self.id_cell + 9 * i].figure == 'None':
                res.append(self.id_cell + 9 * i)
                i += 1
            else:
                if self.field[self.id_cell + 9 * i].figure[0] != self.cell.figure[0]:
                    res.append(self.id_cell + 9 * i)
                break
        i = 1
        while (self.id_cell - 9 * i) % 8 != 7 and -1 < (self.id_cell - 9 * i) < 64:
            if self.field[self.id_cell - 9 * i].figure == 'None':
                res.append(self.id_cell - 9 * i)
                i += 1
            else:
                if self.field[self.id_cell - 9 * i].figure[0] != self.cell.figure[0]:
                    res.append(self.id_cell - 9 * i)
                break
        i = 1
        while (self.id_cell - 7 * i) % 8 != 0 and -1 < (self.id_cell - 7 * i) < 64:
            if self.field[self.id_cell - 7 * i].figure == 'None':
                res.append(self.id_cell - 7 * i)
                i += 1
            else:
                if self.field[self.id_cell - 7 * i].figure[0] != self.cell.figure[0]:
                    res.append(self.id_cell - 7 * i)
                break
        if is_num:
            return res
        res = self.remove_move_to_lose(res)
        return self.num_to_id(res)

    def horse(self, is_num):
        res = []
        if self.id_cell < 48 and self.id_cell % 8 != 0:
            if self.cell.figure[0] != self.field[self.id_cell + 15].figure[0]:
                res.append(self.id_cell + 15)
        if self.id_cell < 56 and self.id_cell % 8 > 1:
            if self.cell.figure[0] != self.field[self.id_cell + 6].figure[0]:
                res.append(self.id_cell + 6)
        if self.id_cell > 7 and self.id_cell % 8 > 1:
            if self.cell.figure[0] != self.field[self.id_cell - 10].figure[0]:
                res.append(self.id_cell - 10)
        if self.id_cell > 15 and self.id_cell % 8 != 0:
            if self.cell.figure[0] != self.field[self.id_cell - 17].figure[0]:
                res.append(self.id_cell - 17)
        if self.id_cell < 48 and self.id_cell % 8 != 7:
            if self.cell.figure[0] != self.field[self.id_cell + 17].figure[0]:
                res.append(self.id_cell + 17)
        if self.id_cell < 56 and self.id_cell % 8 < 6:
            if self.cell.figure[0] != self.field[self.id_cell + 10].figure[0]:
                res.append(self.id_cell + 10)
        if self.id_cell > 7 and self.id_cell % 8 < 6:
            if self.cell.figure[0] != self.field[self.id_cell - 6].figure[0]:
                res.append(self.id_cell - 6)
        if self.id_cell > 15 and self.id_cell % 8 != 7:
            if self.cell.figure[0] != self.field[self.id_cell - 15].figure[0]:
                res.append(self.id_cell - 15)
        if is_num:
            return res
        res = self.remove_move_to_lose(res)
        return self.num_to_id(res)

    def king(self, is_num):
        res = []
        if self.id_cell < 56 and self.id_cell % 8 != 0:
            if self.cell.figure[0] != self.field[self.id_cell + 7].figure[0]:
                res.append(self.id_cell + 7)
        if self.id_cell + 8 < 64:
            if self.cell.figure[0] != self.field[self.id_cell + 8].figure[0]:
                res.append(self.id_cell + 8)
        if self.id_cell < 56 and self.id_cell % 8 != 7:
            if self.cell.figure[0] != self.field[self.id_cell + 9].figure[0]:
                res.append(self.id_cell + 9)
        if self.id_cell % 8 != 7:
            if self.cell.figure[0] != self.field[self.id_cell + 1].figure[0]:
                res.append(self.id_cell + 1)
        if self.id_cell > 7 and self.id_cell % 8 != 7:
            if self.cell.figure[0] != self.field[self.id_cell - 7].figure[0]:
                res.append(self.id_cell - 7)
        if self.id_cell > 7:
            if self.cell.figure[0] != self.field[self.id_cell - 8].figure[0]:
                res.append(self.id_cell - 8)
        if self.id_cell > 7 and self.id_cell % 8 != 0:
            if self.cell.figure[0] != self.field[self.id_cell - 9].figure[0]:
                res.append(self.id_cell - 9)
        if self.id_cell % 8 != 0:
            if self.cell.figure[0] != self.field[self.id_cell - 1].figure[0]:
                res.append(self.id_cell - 1)
        if is_num:
            return res
        res = self.remove_move_to_lose(res)
        return self.num_to_id(res)

    def w_castling(self, is_num):
        res = []
        if self.cast['wO-O']:
            if self.id_cell == 4 and self.field[7].figure == 'wR':
                if self.field[5].figure == self.field[6].figure == 'None':
                    res.append(6)
        if self.cast['wO-O-O']:
            if self.id_cell == 4 and self.field[0].figure == 'wR':
                if self.field[1].figure == self.field[2].figure == self.field[3].figure == 'None':
                    res.append(2)
        if len(res) != 0:
            _cell = deepcopy(self.cell)
            ind = self.id_cell
            for cell in self.field:
                if cell.figure[0] == 'b' and cell.figure != 'bK':
                    p = self(cell, is_num=True)
                    if 6 in res:
                        if 4 in p or 5 in p or 6 in p:
                            res.remove(6)
                    if 2 in res:
                        if 2 in p or 3 in p or 4 in p:
                            res.remove(2)
            self.cell = _cell
            self.id_cell = ind
        if is_num:
            return res
        return self.num_to_id(res)

    def b_castling(self, is_num):
        res = []
        if self.cast['bO-O']:
            if self.id_cell == 60 and self.field[63].figure == 'bR':
                if self.field[61].figure == self.field[62].figure == 'None':
                    res.append(62)
        if self.cast['bO-O-O']:
            if self.id_cell == 60 and self.field[56].figure == 'bR':
                if self.field[57].figure == self.field[58].figure == self.field[59].figure == 'None':
                    res.append(58)

        if len(res) != 0:
            _cell = deepcopy(self.cell)
            ind = self.id_cell
            for cell in self.field:
                if cell.figure[0] == 'w' and cell.figure != 'wK':
                    p = self(cell, is_num=True)
                    if 62 in res:
                        if 60 in p or 61 in p or 62 in p:
                            res.remove(62)
                    if 58 in res:
                        if 58 in p or 59 in p or 60 in p:
                            res.remove(58)
            self.cell = _cell
            self.id_cell = ind
        if is_num:
            return res
        return self.num_to_id(res)

    def remove_move_to_lose(self, res):
        clr = self.cell.figure[0]
        _clr = 'w' if clr == 'b' else 'b'
        num_king = None
        remove_res = []

        for i in range(len(self.field)):
            if self.field[i].figure == clr + 'K':
                num_king = i
                break
        cell = deepcopy(self.cell)
        ind = self.id_cell
        _field = self.field
        for step in res:
            if cell.figure == clr + 'K':
                num_king = step
            field = deepcopy(_field)
            field[step].figure = cell.figure
            field[ind].figure = 'None'
            for f in field:
                if f.figure[0] == _clr:
                    p = self(f, field=field, is_num=True)
                    if num_king in p:
                        remove_res.append(step)
        self.field = _field
        self.id_cell = ind
        self.cell = cell

        return [i for i in res if i not in remove_res]


    def num_to_id(self, res):
        res = [self.letters[(num + 1) % 8 - 1] + str(num // 8 + 1) for num in res]
        return res

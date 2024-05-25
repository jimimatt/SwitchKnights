from copy import deepcopy
import queue
import time


class Position:

    def __init__(self, knight1, knight2, knight3, knight4):
        self.k1 = knight1
        self.k2 = knight2
        self.k3 = knight3
        self.k4 = knight4
        self.position_list = []
        self.position_list.append((self.k1, self.k2, self.k3, self.k4))

    def get_coord(self, piece_number):
        if piece_number == 0:
            return self.k1
        if piece_number == 1:
            return self.k2
        if piece_number == 2:
            return self.k3
        if piece_number == 3:
            return self.k4
        return -1

    def set_coord(self, piece_number, new_coord):
        if piece_number == 0:
            self.k1 = new_coord
        elif piece_number == 1:
            self.k2 = new_coord
        elif piece_number == 2:
            self.k3 = new_coord
        elif piece_number == 3:
            self.k4 = new_coord
        else:
            print("Fehler in set_coord()")
        self.position_list.append((self.k1, self.k2, self.k3, self.k4))

    def print_trace(self):
        for pos in self.position_list:
            # print(self.decode_pos_str(pos))
            print(pos)
            print(Position.decode_pos_t(pos))

    def move_count(self):
        return len(self.position_list) - 1

    @staticmethod
    def decode_pos_t(pos_t):
        field = ["." for _ in range(9)]
        field[pos_t[0]] = "W"
        field[pos_t[1]] = "W"
        field[pos_t[2]] = "B"
        field[pos_t[3]] = "B"
        output_str = ""
        for i in range(9):
            output_str = output_str + field[i] + " "
            if (i+1) % 3 == 0:
                output_str = output_str + "\n"
        return output_str

    def __str__(self):
        if self.k1 > self.k2:
            output_str = str(self.k2) + str(self.k1)
        else:
            output_str = str(self.k1) + str(self.k2)
        if self.k3 > self.k4:
            output_str = output_str + str(self.k4) + str(self.k3)
        else:
            output_str = output_str + str(self.k3) + str(self.k4)
        return output_str


class Chessboard:

    def __init__(self):
        self.possible_moves = []
        self.possible_moves.append([1, 2])
        self.possible_moves.append([2, 3])
        self.possible_moves.append([3, 4])
        self.possible_moves.append([1, 8])
        self.possible_moves.append([0])
        self.possible_moves.append([4, 5])
        self.possible_moves.append([7, 8])
        self.possible_moves.append([6, 7])
        self.possible_moves.append([5, 6])

    def get_moves(self, coord):
        # if coord < 0 or coord > 8:
        #     print("Bullshit: coord = " + str(coord))
        return self.possible_moves[coord]

    @staticmethod
    def knights_move(variation, coord):
        if variation == 1 or variation == 3:
            return coord + 5
        elif variation == 2:
            return coord + 7
        elif variation == 4:
            return coord + 1
        elif variation == 5 or variation == 7:
            return coord - 5
        elif variation == 6:
            return coord - 7
        elif variation == 8:
            return coord - 1
        return -1


class SwapKnights:

    def __init__(self):
        self.processed_positions = set([])
        self.board = Chessboard()
        self.solve()

    def solve(self):
        positions = queue.Queue()
        positions.put(Position(0, 2, 6, 8))
        while not positions.empty():
            pos = positions.get()
            if str(pos) == "6802":
                print("Lösung gefunden:")
                print("in " + str(pos.move_count()) + " Zügen:")
                pos.print_trace()
                break
            elif str(pos) in self.processed_positions:
                pass
            else:
                self.processed_positions.add(str(pos))
                # move 4 pieces
                for piece in range(4):
                    coord = pos.get_coord(piece)
                    possible_moves = self.board.get_moves(coord)
                    for possible_move in possible_moves:
                        new_coord = Chessboard.knights_move(possible_move, pos.get_coord(piece))
                        if str(pos).count(str(new_coord)) == 0:
                            new_pos = deepcopy(pos)
                            new_pos.set_coord(piece, new_coord)
                            positions.put(new_pos)


if __name__ == "__main__":
    calc_time = time.time()
    chess = SwapKnights()
    calc_time = round((time.time() - calc_time), 2)
    print(str(calc_time) + "s zur Berechnung benötigt.")

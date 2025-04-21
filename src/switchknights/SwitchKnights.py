import queue
import time
from copy import deepcopy


class Position:
    """Position Class."""

    __slots__ = ("k1", "k2", "k3", "k4", "position_list")

    def __init__(self, knight1: int, knight2: int, knight3: int, knight4: int) -> None:
        """Initialize Position Object."""
        self.k1 = knight1
        self.k2 = knight2
        self.k3 = knight3
        self.k4 = knight4
        self.position_list = []
        self.position_list.append((self.k1, self.k2, self.k3, self.k4))

    def get_coord(self, piece_number: int) -> int:
        """Get coordinate of the knight piece."""
        match piece_number:
            case 0:
                return self.k1
            case 1:
                return self.k2
            case 2:
                return self.k3
            case 3:
                return self.k4
        return -1

    def set_coord(self, piece_number: int, new_coord: int) -> None:
        """Set the coordinate for the knight piece."""
        match piece_number:
            case 0:
                self.k1 = new_coord
            case 1:
                self.k2 = new_coord
            case 2:
                self.k3 = new_coord
            case 3:
                self.k4 = new_coord
        self.position_list.append((self.k1, self.k2, self.k3, self.k4))

    def print_trace(self) -> None:
        """Print the solution."""
        for pos in self.position_list:
            print(pos)
            print(Position.decode_pos_t(pos))

    def move_count(self) -> int:
        """Get move count."""
        return len(self.position_list) - 1

    @staticmethod
    def decode_pos_t(pos_t: tuple[int, int, int, int]) -> str:
        """Decode position."""
        field = ["." for _ in range(9)]
        field[pos_t[0]] = "W"
        field[pos_t[1]] = "W"
        field[pos_t[2]] = "B"
        field[pos_t[3]] = "B"
        output_str = ""
        for i in range(9):
            output_str = output_str + field[i] + " "
            if (i + 1) % 3 == 0:
                output_str = output_str + "\n"
        return output_str

    def __str__(self) -> str:
        """To string of Position class."""
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
    """Chessboard class."""

    def __init__(self) -> None:
        """Initialize Chessboard."""
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

    def get_moves(self, coord: int) -> list[int]:
        """Get moves for coordinate."""
        return self.possible_moves[coord]

    @staticmethod
    def knights_move(variation: int, coord: int) -> int:
        """Knights move."""
        match variation:
            case 1 | 3:
                return coord + 5
            case 2:
                return coord + 7
            case 4:
                return coord + 1
            case 5 | 7:
                return coord - 5
            case 6:
                return coord - 7
            case 8:
                return coord - 1
        return -1


class SwapKnights:
    """SwapKnights class."""

    def __init__(self) -> None:
        """Initialize SwapKnights."""
        self.processed_positions: set[str] = set()
        self.board: Chessboard = Chessboard()
        self.solve()

    def solve(self) -> None:
        """Solve the knights puzzle."""
        positions = queue.Queue()
        positions.put(Position(0, 2, 6, 8))
        while not positions.empty():
            pos = positions.get()
            if (pos_str := str(pos)) == "6802" or pos_str == '8602' or pos_str == '6820' or pos_str == '8620':
                print(f"Solution found: {pos.move_count()} moves")
                pos.print_trace()
                break
            elif str(pos) in self.processed_positions:
                continue
            else:
                self.processed_positions.add(str(pos))
                # move 4 pieces
                for piece in range(4):
                    coord = pos.get_coord(piece)
                    possible_moves = self.board.get_moves(coord)
                    for possible_move in possible_moves:
                        new_coord = Chessboard.knights_move(
                            possible_move, pos.get_coord(piece)
                        )
                        if str(pos).count(str(new_coord)) == 0:
                            new_pos = deepcopy(pos)
                            new_pos.set_coord(piece, new_coord)
                            positions.put(new_pos)


if __name__ == "__main__":
    calc_time = time.time()
    chess = SwapKnights()
    print(f"Computing time {time.time() - calc_time:.4f}s")

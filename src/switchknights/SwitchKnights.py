import time
from collections import deque
from enum import IntEnum, unique
from typing import NamedTuple, NewType

Coord = NewType("Coord", int)


@unique
class Knight(IntEnum):
    """Knight piece."""

    WHITE_1 = 0
    WHITE_2 = 1
    BLACK_1 = 2
    BLACK_2 = 3


class KnightPosition(NamedTuple):
    """Position class."""

    white_knight_1: Coord
    white_knight_2: Coord
    black_knight_1: Coord
    black_knight_2: Coord

    def __str__(self) -> str:
        """To string of Position class."""
        return f"{self.white_knight_1}{self.white_knight_2}{self.black_knight_1}{self.black_knight_2}"


class TurnOrder:
    """TurnOrder Class."""

    __slots__ = ("position", "position_list")

    def __init__(
        self,
        white_knight_1: Coord,
        white_knight_2: Coord,
        black_knight_1: Coord,
        black_knight_2: Coord,
    ) -> None:
        """Initialize Position Object."""
        self.position = KnightPosition(
            white_knight_1, white_knight_2, black_knight_1, black_knight_2
        )
        self.position_list = [
            self.position,
        ]

    def get_coord(self, knight: Knight) -> Coord:
        """Get coordinate of the knight piece."""
        return self.position[knight.value]

    def print_trace(self) -> None:
        """Print the solution."""
        for pos in self.position_list:
            print(pos)
            print(TurnOrder.decode_pos_t(pos))

    def move_count(self) -> int:
        """Get move count."""
        return len(self.position_list) - 1

    @staticmethod
    def decode_pos_t(pos_t: KnightPosition) -> str:
        """Decode position."""
        field = ["." for _ in range(9)]
        field[pos_t[Knight.WHITE_1.value]] = "W"
        field[pos_t[Knight.WHITE_2.value]] = "W"
        field[pos_t[Knight.BLACK_1.value]] = "B"
        field[pos_t[Knight.BLACK_2.value]] = "B"
        output_str = ""
        for i in range(9):
            output_str = output_str + field[i] + " "
            if (i + 1) % 3 == 0:
                output_str = output_str + "\n"
        return output_str

    def __str__(self) -> str:
        """To string of Position class."""
        return self.position.__str__()


class Chessboard:
    """Chessboard class.

    Coordinate system:
    0 1 2
    3 4 5
    6 7 8
    """

    class MoveVariation(IntEnum):
        """Move variation Enum.

        U = Up
        D = Down
        L = Left
        R = Right
        """

        UUL = -7
        UUR = -5
        URR = -1
        DRR = 5
        DDR = 7
        DDL = 5
        DLL = 1
        ULL = -5

    possible_moves: dict[Coord, list[MoveVariation]] = {
        Coord(0): [MoveVariation.DDR, MoveVariation.DRR],
        Coord(1): [MoveVariation.DDL, MoveVariation.DDR],
        Coord(2): [MoveVariation.DDL, MoveVariation.DLL],
        Coord(3): [MoveVariation.URR, MoveVariation.DRR],
        Coord(4): [],
        Coord(5): [MoveVariation.ULL, MoveVariation.DLL],
        Coord(6): [MoveVariation.UUR, MoveVariation.URR],
        Coord(7): [MoveVariation.UUL, MoveVariation.UUR],
        Coord(8): [MoveVariation.UUL, MoveVariation.ULL],
    }

    @staticmethod
    def get_moves(coord: Coord) -> list[Coord]:
        """Get moves for coordinate."""
        return [
            Coord(coord + possible_move)
            for possible_move in Chessboard.possible_moves[coord]
        ]


class SwapKnights:
    """SwapKnights class."""

    target_positions = {
        KnightPosition(Coord(6), Coord(8), Coord(0), Coord(2)),
        KnightPosition(Coord(8), Coord(6), Coord(0), Coord(2)),
        KnightPosition(Coord(6), Coord(8), Coord(2), Coord(0)),
        KnightPosition(Coord(8), Coord(6), Coord(2), Coord(0)),
    }

    def __init__(self) -> None:
        """Initialize SwapKnights."""
        self.processed_positions: set[KnightPosition] = set()
        self.win_condition: KnightPosition = KnightPosition(
            Coord(0), Coord(2), Coord(6), Coord(8)
        )
        if (solution := self.solve()) is not None:
            print(f"Solution found: {solution.move_count()} moves")
            solution.print_trace()
        else:
            print("No solution found")

    def solve(self) -> TurnOrder | None:
        """Solve the knights puzzle."""
        positions = deque[TurnOrder]()
        positions.append(TurnOrder(Coord(0), Coord(2), Coord(6), Coord(8)))
        while len(positions) > 0:
            pos: TurnOrder = positions.popleft()
            if pos.position in SwapKnights.target_positions:
                return pos
            elif pos.position in self.processed_positions:
                continue
            else:
                self.processed_positions.add(pos.position)
                # move 4 pieces
                for piece in list(Knight):
                    coord = pos.get_coord(piece)
                    for new_coord in Chessboard.get_moves(coord):
                        # check if the new position is not occupied by another knight
                        if pos.position.count(new_coord) == 0:
                            new_position_values = list(pos.position)
                            new_position_values[piece.value] = new_coord
                            new_pos = TurnOrder(*new_position_values)
                            new_pos.position_list = pos.position_list + [
                                new_pos.position
                            ]
                            positions.append(new_pos)
        return None


if __name__ == "__main__":
    calc_time = time.time()
    chess = SwapKnights()
    print(f"Computing time {time.time() - calc_time:.4f}s")

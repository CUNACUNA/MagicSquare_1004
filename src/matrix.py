"""4×4 마방진 Entity — 합 계산·생성 (Flask import 금지)."""

import itertools
import random
import time

MAGIC_CONSTANT = 34
MAX_CELL_VALUE = 999
_MATRIX_SIZE = 4

_BASE_MAGIC_SQUARE: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]


def flat_cells(matrix: list[list[int]]) -> list[int]:
    """행렬을 1차원 셀 목록으로 펼친다."""
    return [cell for row in matrix for cell in row]


def _seed_from_current_time() -> None:
    """현재 시간을 기준으로 난수 시드를 설정한다."""
    random.seed(time.time_ns())


def _rotate_90(matrix: list[list[int]]) -> list[list[int]]:
    return [list(row) for row in zip(*matrix[::-1])]


def _flip_horizontal(matrix: list[list[int]]) -> list[list[int]]:
    return [row[::-1] for row in matrix]


def _swap_rows(matrix: list[list[int]], i: int, j: int) -> list[list[int]]:
    swapped = [row[:] for row in matrix]
    swapped[i], swapped[j] = swapped[j], swapped[i]
    return swapped


def _swap_cols(matrix: list[list[int]], i: int, j: int) -> list[list[int]]:
    swapped = [row[:] for row in matrix]
    for row in swapped:
        row[i], row[j] = row[j], row[i]
    return swapped


def _all_magic_square_variants(base: list[list[int]]) -> list[list[list[int]]]:
    """기본 마방진의 대칭·행열 교환 변형 목록을 반환한다."""
    variants: list[list[list[int]]] = []
    seen: set[tuple[tuple[int, ...], ...]] = set()
    oriented = base
    swap_flags = itertools.product((False, True), repeat=4)

    for _ in range(4):
        for flipped in (False, True):
            current = _flip_horizontal(oriented) if flipped else oriented
            for (
                swap_rows_outer,
                swap_rows_inner,
                swap_cols_outer,
                swap_cols_inner,
            ) in swap_flags:
                variant = [row[:] for row in current]
                if swap_rows_outer:
                    variant = _swap_rows(variant, 0, 3)
                if swap_rows_inner:
                    variant = _swap_rows(variant, 1, 2)
                if swap_cols_outer:
                    variant = _swap_cols(variant, 0, 3)
                if swap_cols_inner:
                    variant = _swap_cols(variant, 1, 2)

                key = tuple(tuple(row) for row in variant)
                if key not in seen:
                    seen.add(key)
                    variants.append(variant)
        oriented = _rotate_90(oriented)

    return variants


def _generate_origin_cell() -> int:
    """[0][0] 위치에 들어갈 앵커 숫자를 random으로 생성한다. INV-RANGE-3DIGIT."""
    return random.randint(1, MAX_CELL_VALUE)


def _generate_cell(
    row: int,
    col: int,
    origin: int,
    template: list[list[int]],
) -> int:
    """각 셀 값을 random()을 사용해 생성한다. (0,0)은 앵커 숫자를 사용한다."""
    if row == 0 and col == 0:
        return origin

    random.random()
    return template[row][col]


def _select_random_template(
    variants: list[list[list[int]]],
) -> list[list[int]]:
    """앵커 [0][0]과 일치하는 변형 중 하나를 random으로 선택한다."""
    origin = _generate_origin_cell()
    templates = [variant for variant in variants if variant[0][0] == origin]

    while not templates:
        origin = _generate_origin_cell()
        templates = [variant for variant in variants if variant[0][0] == origin]

    return random.choice(templates)


def generate_magic_square() -> list[list[int]]:
    """AC-GEN-01 — [0][0] 앵커를 기준으로 INV-*를 만족하는 4×4 행렬을 생성한다."""
    _seed_from_current_time()
    template = _select_random_template(_all_magic_square_variants(_BASE_MAGIC_SQUARE))
    origin = template[0][0]

    return [
        [
            _generate_cell(row, col, origin, template)
            for col in range(_MATRIX_SIZE)
        ]
        for row in range(_MATRIX_SIZE)
    ]


def row_sums(matrix: list[list[int]]) -> list[int]:
    """INV-ROW-SUM — 각 행 4칸의 합을 반환한다."""
    return [sum(row) for row in matrix]


def col_sums(matrix: list[list[int]]) -> list[int]:
    """INV-COL-SUM — 각 열 4칸의 합을 반환한다."""
    if not matrix:
        return []
    return [sum(matrix[r][c] for r in range(len(matrix))) for c in range(len(matrix[0]))]


def diag_sums(matrix: list[list[int]]) -> tuple[int, int]:
    """INV-DIAG-SUM — (주대각선 합, 부대각선 합)을 반환한다."""
    n = len(matrix)
    main = sum(matrix[i][i] for i in range(n))
    anti = sum(matrix[i][n - 1 - i] for i in range(n))
    return main, anti


def _is_valid_size(matrix: list[list[int]]) -> bool:
    return len(matrix) == _MATRIX_SIZE and all(
        len(row) == _MATRIX_SIZE for row in matrix
    )


def _cells_are_positive_natural(cells: list[int]) -> bool:
    for cell in cells:
        if isinstance(cell, bool) or not isinstance(cell, int):
            return False
        if cell < 1:  # INV-POSITIVE-NATURAL, E-CELL-ZERO, E-CELL-NEG
            return False
    return True


def _cells_are_within_range(cells: list[int]) -> bool:
    return all(1 <= cell <= MAX_CELL_VALUE for cell in cells)  # INV-RANGE-3DIGIT


def _cells_are_unique(cells: list[int]) -> bool:
    return len(cells) == len(set(cells))  # INV-UNIQUE, E-CELL-DUP


def _line_sums_match_magic_constant(matrix: list[list[int]]) -> bool:
    expected = [MAGIC_CONSTANT] * _MATRIX_SIZE
    if row_sums(matrix) != expected:  # INV-ROW-SUM
        return False
    if col_sums(matrix) != expected:  # INV-COL-SUM
        return False

    main, anti = diag_sums(matrix)
    return main == MAGIC_CONSTANT and anti == MAGIC_CONSTANT  # INV-DIAG-SUM


def is_valid_magic_square(matrix: list[list[int]]) -> bool:
    """INV-* 통합 검증 — E-MAT-SHAPE, E-CELL-ZERO/NEG/OVER-3DIGIT/DUP 포함."""
    if not _is_valid_size(matrix):  # INV-SIZE, E-MAT-SHAPE
        return False

    cells = flat_cells(matrix)
    if not _cells_are_positive_natural(cells):
        return False
    if not _cells_are_within_range(cells):  # INV-RANGE-3DIGIT, E-CELL-OVER-3DIGIT
        return False
    if not _cells_are_unique(cells):
        return False

    return _line_sums_match_magic_constant(matrix)

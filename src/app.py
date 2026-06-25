"""Boundary — 입력 파싱·E-* 검증 후 Entity 호출."""

from src.matrix import is_valid_magic_square


def parse_matrix(raw: object) -> list[list[int]]:
    """E-CELL-NONINT — 문자·실수·빈칸 등 비정수 셀은 Boundary에서 거부한다."""
    if not isinstance(raw, list):
        raise ValueError("matrix must be a list")

    matrix: list[list[int]] = []
    for row in raw:
        if not isinstance(row, list):
            raise ValueError("each row must be a list")

        parsed_row: list[int] = []
        for cell in row:
            if isinstance(cell, bool) or not isinstance(cell, int):
                raise ValueError("each cell must be an integer")
            parsed_row.append(cell)
        matrix.append(parsed_row)

    return matrix


def validate_magic_square(matrix: list[list[int]]) -> bool:
    """E-MAT-SHAPE, E-CELL-* — Entity is_valid_magic_square에 위임한다."""
    return is_valid_magic_square(matrix)

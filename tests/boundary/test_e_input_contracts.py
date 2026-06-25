"""Boundary E-* 입력 계약 검증.

Flask Boundary(`src/app.py`)가 E-* 검증 후 Entity(`src/matrix.py`)를 호출한다.
"""

import pytest

from src.app import parse_matrix, validate_magic_square

# 알려진 유효 4×4 마방진 — E-CELL-* 케이스 변형용 베이스
VALID_4X4: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]


# --- E-MAT-SHAPE: 4×4가 아닌 배열 → 거부 또는 False ---


@pytest.mark.boundary
def test_e_mat_shape_three_rows_returns_false() -> None:
    """E-MAT-SHAPE — 행이 3개인 배열은 유효하지 않다."""
    matrix = [row[:] for row in VALID_4X4[:3]]

    assert validate_magic_square(matrix) is False  # E-MAT-SHAPE


@pytest.mark.boundary
def test_e_mat_shape_five_rows_returns_false() -> None:
    """E-MAT-SHAPE — 행이 5개인 배열은 유효하지 않다."""
    matrix = [row[:] for row in VALID_4X4] + [[1, 2, 3, 4]]

    assert validate_magic_square(matrix) is False  # E-MAT-SHAPE


@pytest.mark.boundary
def test_e_mat_shape_row_length_not_four_returns_false() -> None:
    """E-MAT-SHAPE — 열 길이가 4가 아닌 행이 있으면 유효하지 않다."""
    matrix = [row[:] for row in VALID_4X4]
    matrix[0] = [16, 3, 2]

    assert validate_magic_square(matrix) is False  # E-MAT-SHAPE


@pytest.mark.boundary
def test_e_mat_shape_empty_matrix_returns_false() -> None:
    """E-MAT-SHAPE — 빈 배열은 유효하지 않다."""
    assert validate_magic_square([]) is False  # E-MAT-SHAPE


# --- E-CELL-ZERO: 셀에 0 포함 → is_valid → False ---


@pytest.mark.boundary
def test_e_cell_zero_any_zero_cell_returns_false() -> None:
    """E-CELL-ZERO — 0이 포함된 4×4 배열은 유효하지 않다."""
    matrix = [row[:] for row in VALID_4X4]
    matrix[0][0] = 0

    assert validate_magic_square(matrix) is False  # E-CELL-ZERO


# --- E-CELL-NONINT: 문자·실수·빈칸 → Boundary에서 거부 ---


@pytest.mark.boundary
def test_e_cell_nonint_string_cell_rejected_at_boundary() -> None:
    """E-CELL-NONINT — 문자열 셀은 Boundary에서 거부한다 (Entity까지 가지 않음)."""
    raw = [[str(cell) for cell in row] for row in VALID_4X4]

    with pytest.raises(ValueError):  # E-CELL-NONINT
        parse_matrix(raw)


@pytest.mark.boundary
def test_e_cell_nonint_float_cell_rejected_at_boundary() -> None:
    """E-CELL-NONINT — 실수 셀은 Boundary에서 거부한다."""
    raw = [row[:] for row in VALID_4X4]
    raw[1][1] = 10.5

    with pytest.raises(ValueError):  # E-CELL-NONINT
        parse_matrix(raw)


@pytest.mark.boundary
def test_e_cell_nonint_none_cell_rejected_at_boundary() -> None:
    """E-CELL-NONINT — None 셀은 Boundary에서 거부한다."""
    raw = [row[:] for row in VALID_4X4]
    raw[2][2] = None

    with pytest.raises(ValueError):  # E-CELL-NONINT
        parse_matrix(raw)


# --- E-CELL-NEG: 음수 → is_valid → False ---


@pytest.mark.boundary
def test_e_cell_neg_negative_cell_returns_false() -> None:
    """E-CELL-NEG — 음수 셀이 포함된 4×4 배열은 유효하지 않다."""
    matrix = [row[:] for row in VALID_4X4]
    matrix[3][3] = -1

    assert validate_magic_square(matrix) is False  # E-CELL-NEG


# --- E-CELL-OVER-3DIGIT: 999 초과 → is_valid → False ---


@pytest.mark.boundary
def test_e_cell_over_3digit_cell_over_999_returns_false() -> None:
    """E-CELL-OVER-3DIGIT — 999를 초과하는 셀이 있으면 유효하지 않다."""
    matrix = [row[:] for row in VALID_4X4]
    matrix[0][0] = 1000

    assert validate_magic_square(matrix) is False  # E-CELL-OVER-3DIGIT


# --- E-CELL-DUP: 동일 값 중복 → is_valid → False ---


@pytest.mark.boundary
def test_e_cell_dup_duplicate_values_returns_false() -> None:
    """E-CELL-DUP — 중복 값이 있는 4×4 배열은 유효하지 않다."""
    matrix = [row[:] for row in VALID_4X4]
    matrix[0][1] = matrix[0][0]

    assert validate_magic_square(matrix) is False  # E-CELL-DUP

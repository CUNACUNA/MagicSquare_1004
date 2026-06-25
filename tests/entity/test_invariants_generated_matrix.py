"""generate_magic_square() 결과 INV-* 불변식 검증 — AC-GEN-01."""

import pytest

from src.matrix import (
    MAGIC_CONSTANT,
    MAX_CELL_VALUE,
    col_sums,
    diag_sums,
    flat_cells,
    generate_magic_square,
    row_sums,
)


@pytest.fixture
def generated_matrix() -> list[list[int]]:
    return generate_magic_square()  # AC-GEN-01


# --- INV-SIZE ---


@pytest.mark.entity
def test_inv_size_generated_matrix_is_4x4(
    generated_matrix: list[list[int]],
) -> None:
    """INV-SIZE — 생성된 행렬은 4×4 형상이다."""
    assert len(generated_matrix) == 4  # INV-SIZE
    assert all(len(row) == 4 for row in generated_matrix)  # INV-SIZE


# --- INV-POSITIVE-NATURAL ---


@pytest.mark.entity
def test_inv_positive_natural_generated_matrix_cells_are_at_least_one(
    generated_matrix: list[list[int]],
) -> None:
    """INV-POSITIVE-NATURAL — 생성된 행렬의 모든 셀은 0보다 큰 자연수이다."""
    assert all(cell >= 1 for cell in flat_cells(generated_matrix))  # INV-POSITIVE-NATURAL


# --- INV-RANGE-3DIGIT ---


@pytest.mark.entity
def test_inv_range_3digit_generated_matrix_cells_are_within_999(
    generated_matrix: list[list[int]],
) -> None:
    """INV-RANGE-3DIGIT — 생성된 행렬의 모든 셀은 3자리 이하 자연수(1~999)이다."""
    assert all(1 <= cell <= MAX_CELL_VALUE for cell in flat_cells(generated_matrix))  # INV-RANGE-3DIGIT


# --- INV-UNIQUE ---


@pytest.mark.entity
def test_inv_unique_generated_matrix_has_no_duplicate_cells(
    generated_matrix: list[list[int]],
) -> None:
    """INV-UNIQUE — 생성된 행렬 16칸 값은 서로 다르다."""
    cells = flat_cells(generated_matrix)
    assert len(cells) == len(set(cells))  # INV-UNIQUE


# --- INV-ROW-SUM ---


@pytest.mark.entity
def test_inv_row_sum_generated_matrix_each_row_sums_to_magic_constant(
    generated_matrix: list[list[int]],
) -> None:
    """INV-ROW-SUM — 생성된 행렬의 각 행 4칸 합은 34이다."""
    assert row_sums(generated_matrix) == [MAGIC_CONSTANT] * 4  # INV-ROW-SUM


# --- INV-COL-SUM ---


@pytest.mark.entity
def test_inv_col_sum_generated_matrix_each_column_sums_to_magic_constant(
    generated_matrix: list[list[int]],
) -> None:
    """INV-COL-SUM — 생성된 행렬의 각 열 4칸 합은 34이다."""
    assert col_sums(generated_matrix) == [MAGIC_CONSTANT] * 4  # INV-COL-SUM


# --- INV-DIAG-SUM ---


@pytest.mark.entity
def test_inv_diag_sum_generated_matrix_diagonals_sum_to_magic_constant(
    generated_matrix: list[list[int]],
) -> None:
    """INV-DIAG-SUM — 생성된 행렬의 주·부 대각선 각 4칸 합은 34이다."""
    main_diag, anti_diag = diag_sums(generated_matrix)
    assert main_diag == MAGIC_CONSTANT  # INV-DIAG-SUM
    assert anti_diag == MAGIC_CONSTANT  # INV-DIAG-SUM

"""AC-GEN-01 — 웹 Boundary에서 출력 버튼으로 4×4 마방진 생성·표시."""

import re

import pytest

from src.app import create_app, format_matrix_display
from src.matrix import is_valid_magic_square


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


# --- AC-GEN-01: 행렬 표시 형식 (한 줄 4개 숫자 × 4줄) ---


@pytest.mark.boundary
def test_ac_gen_01_format_matrix_display_shows_four_numbers_per_line() -> None:
    """AC-GEN-01 — 표시 형식은 한 줄에 4개 숫자, 총 4줄이다."""
    matrix = [
        [16, 3, 2, 13],
        [5, 10, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 1],
    ]

    display = format_matrix_display(matrix)
    lines = display.splitlines()

    assert len(lines) == 4  # AC-GEN-01
    assert all(len(line.split()) == 4 for line in lines)  # AC-GEN-01


# --- AC-GEN-01: 웹 UI ---


@pytest.mark.boundary
def test_ac_gen_01_home_page_has_output_button(client) -> None:
    """AC-GEN-01 — 홈 페이지에 '출력' 버튼이 있다."""
    response = client.get("/")

    assert response.status_code == 200  # AC-GEN-01
    assert "출력" in response.get_data(as_text=True)  # AC-GEN-01


@pytest.mark.boundary
def test_ac_gen_01_output_button_displays_generated_4x4_matrix(client) -> None:
    """AC-GEN-01 — '출력' 버튼 클릭 시 Entity가 생성한 4×4 행렬을 표시한다."""
    response = client.post("/", data={"action": "output"})

    assert response.status_code == 200  # AC-GEN-01
    html = response.get_data(as_text=True)
    match = re.search(r'<pre class="matrix">(.*?)</pre>', html, re.DOTALL)
    assert match is not None  # AC-GEN-01

    lines = match.group(1).strip().splitlines()
    assert len(lines) == 4  # AC-GEN-01

    matrix = [[int(cell) for cell in line.split()] for line in lines]
    assert all(len(row) == 4 for row in matrix)  # AC-GEN-01
    assert is_valid_magic_square(matrix)  # AC-GEN-01, INV-*

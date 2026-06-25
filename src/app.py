"""Boundary — 입력 파싱·E-* 검증·Flask UI 후 Entity 호출."""

from flask import Flask, render_template_string, request

from src.matrix import generate_magic_square, is_valid_magic_square

_INDEX_HTML = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <title>MagicSquare_1004</title>
</head>
<body>
  <h1>4×4 마방진 생성기</h1>
  <form method="post">
    <button type="submit" name="action" value="output">출력</button>
  </form>
  {% if matrix_display %}
  <pre class="matrix">{{ matrix_display }}</pre>
  {% endif %}
</body>
</html>
"""


def format_matrix_display(matrix: list[list[int]]) -> str:
    """AC-GEN-01 — 4×4 행렬을 한 줄 4개 숫자 × 4줄 텍스트로 반환한다."""
    return "\n".join(" ".join(str(cell) for cell in row) for row in matrix)  # AC-GEN-01


def parse_matrix(raw: object) -> list[list[int]]:
    """E-CELL-NONINT — 문자·실수·빈칸 등 비정수 셀은 Boundary에서 거부한다."""
    if not isinstance(raw, list):  # E-CELL-NONINT
        raise ValueError("matrix must be a list")

    matrix: list[list[int]] = []
    for row in raw:
        if not isinstance(row, list):  # E-CELL-NONINT
            raise ValueError("each row must be a list")

        parsed_row: list[int] = []
        for cell in row:
            if isinstance(cell, bool) or not isinstance(cell, int):  # E-CELL-NONINT
                raise ValueError("each cell must be an integer")
            parsed_row.append(cell)
        matrix.append(parsed_row)

    return matrix


def validate_magic_square(matrix: list[list[int]]) -> bool:
    """E-MAT-SHAPE, E-CELL-* — Entity is_valid_magic_square에 위임한다."""
    return is_valid_magic_square(matrix)  # E-MAT-SHAPE, E-CELL-ZERO, E-CELL-NEG, E-CELL-OVER-3DIGIT, E-CELL-DUP


def create_app() -> Flask:
    """Flask Boundary 앱 팩토리."""
    app = Flask(__name__)

    @app.route("/", methods=["GET", "POST"])
    def index():
        matrix_display = None
        if request.method == "POST" and request.form.get("action") == "output":
            matrix = generate_magic_square()  # AC-GEN-01
            matrix_display = format_matrix_display(matrix)  # AC-GEN-01

        return render_template_string(
            _INDEX_HTML,
            matrix_display=matrix_display,
        )

    return app


if __name__ == "__main__":
    create_app().run(debug=True)

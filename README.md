# MagicSquare_1004

4×4 마방진 생성기 — Python 3.12, pytest 기반 Dual-Track TDD(C2C 추적) 프로젝트.

> **목표:** **4×4** 격자에서 모든 **행·열·주/부 대각선(각 4칸)** 의 합이 **34**, 모든 셀은 **3자리 이하 자연수(1~999)**, **16칸 값 중복 없음**을 만족하는 행렬을 **생성·검증**한다.
>
> 상세 사양: [docs/PRODUCT-Spec.md](docs/PRODUCT-Spec.md) · 개발 규칙: [AGENTS.md](AGENTS.md) · 구현 보고서: [report/02.entity-boundary-implementation.REPORT.md](report/02.entity-boundary-implementation.REPORT.md)

## 아키텍처 (ECB)

| 레이어 | 경로 | 책임 |
|--------|------|------|
| **Entity** | `src/matrix.py` | 합 계산, INV-* 검증, 마방진 생성 알고리즘 |
| **Boundary** | `src/app.py` | HTTP/폼 파싱, E-* 입력 검증, Entity 결과 표시 |
| **Entity 테스트** | `tests/entity/` | INV-* 불변식 (`@pytest.mark.entity`) |
| **Boundary 테스트** | `tests/boundary/` | E-*, AC-* 계약 (`@pytest.mark.boundary`) |

---

## 구현 로드맵

TDD 순서: **RED(테스트) → GREEN(최소 구현) → REFACTOR**. 계약 ID 없는 동작은 구현하지 않는다.

### 1. Entity — 불변식 검증 (`src/matrix.py`, `tests/entity/`)

마방진(또는 후보 행렬)이 항상 만족해야 하는 규칙.  
`tests/entity/test_invariants_generated_matrix.py` — `generate_magic_square()` 결과 검증 (7 passed).

- [x] **INV-POSITIVE-NATURAL** — 모든 셀은 0보다 큰 자연수 (`M[i][j] >= 1`)
- [x] **INV-RANGE-3DIGIT** — 셀 값은 3자리 이하 자연수 (`1 <= M[i][j] <= 999`)
- [x] **INV-UNIQUE** — 16칸 값 중복 없음
- [x] **INV-ROW-SUM** — 각 행 4칸의 합 = 34
- [x] **INV-COL-SUM** — 각 열 4칸의 합 = 34
- [x] **INV-DIAG-SUM** — 주대각선·부대각선 각 4칸의 합 = 34
- [x] **INV-SIZE** — 4×4 형상 검증 (`len(matrix)==4`, 각 행 길이 4)

### 2. Entity — 검증 API (`src/matrix.py`, `tests/entity/`)

불변식을 조합하는 Entity 공개 API.

- [x] `row_sums(matrix)` — 4개 행 합 반환
- [x] `col_sums(matrix)` — 4개 열 합 반환
- [x] `diag_sums(matrix)` — (주대각선 합, 부대각선 합) 반환
- [x] `is_valid_magic_square(matrix)` — INV-* 통합 검증 (`True` / `False`)

### 3. Entity — 마방진 생성 (`src/matrix.py`, `tests/entity/`)

- [x] **AC-GEN-01** — 생성 요청 시 INV-*를 모두 만족하는 4×4 행렬 반환
  - 현재 시간 기반 시드 → `[0][0]` 앵커 random 생성 → 변형 마방진 템플릿으로 16셀 채움

### 4. Boundary — 입력 계약 (`src/app.py`, `tests/boundary/`)

Boundary에서 E-* 검증 후 Entity 호출. Entity까지 가지 않아야 하는 입력은 Boundary에서 거부.  
`tests/boundary/test_e_input_contracts.py` — 11 passed.

- [x] **E-MAT-SHAPE** — 4×4가 아닌 배열 → 거부 또는 `False` / 명확한 오류
- [x] **E-CELL-ZERO** — 셀에 0 포함 → `is_valid` → `False`
- [x] **E-CELL-NONINT** — 문자·실수·빈칸 → Boundary에서 거부
- [x] **E-CELL-NEG** — 음수 → `is_valid` → `False`
- [x] **E-CELL-OVER-3DIGIT** — 999 초과 → `is_valid` → `False` (INV-RANGE-3DIGIT)
- [x] **E-CELL-DUP** — 동일 값 중복 → `is_valid` → `False`

### 5. Boundary — 수용 조건 & Flask UI (`src/app.py`, `tests/boundary/`)

사용자가 "됐다"고 받아들이는 기능 수준 조건.

- [ ] **AC-VAL-01** — 사용자가 4×4 행렬을 입력하면 마방진 여부(합 34 + 1~999 자연수 + 중복 없음) 확인 가능
- [ ] **AC-VAL-02** — 조건 위반 시 어느 규칙에서 실패했는지 구분 가능 *(선택, v0.2)*
- [x] **AC-GEN-01 Flask 생성 UI** — 「출력」 버튼으로 4×4 마방진 생성·표시 (한 줄 4숫자 × 4줄)
- [ ] **Flask 검증 UI** — 4×4 입력 폼 + 마방진 검증 결과 표시 (AC-VAL-01)

### 6. 확정된 범위 제외 (구현하지 않음)

| 항목 | 확정 내용 |
|------|-----------|
| 격자 크기 | **4×4 매트릭스만** 생성·검증 (3×3, 5×5 등 다른 차수 제외) |
| 셀 값 범위 | **3자리 이하 자연수** (`1~999`) — `INV-RANGE-3DIGIT` |
| 부가 기능 | 힌트, 풀이 과정, 난이도, 점수 **고려하지 않음** |

---

## 작업 내역

| 단계 | 내용 | 파일 |
|------|------|------|
| RED | `generate_magic_square()` 결과 INV-* 7건 | `tests/entity/test_invariants_generated_matrix.py` |
| GREEN | 합 계산·생성·검증 Entity | `src/matrix.py` |
| RED | E-* 입력 계약 11건 | `tests/boundary/test_e_input_contracts.py` |
| GREEN | `parse_matrix`, `validate_magic_square` | `src/app.py` |
| REFACTOR | INV-* 헬퍼 분리, 계약 ID 주석 | `src/matrix.py`, tests |
| RED | AC-GEN-01 웹 UI 3건 | `tests/boundary/test_ac_gen_01_web.py` |
| GREEN | Flask `create_app`, `format_matrix_display` | `src/app.py`, `requirements.txt` |

```bash
pytest -q                # 21 passed
pytest tests/entity -q   # 7 passed
pytest tests/boundary -q # 14 passed
```

### Flask 서버 실행

```bash
pip install -r requirements.txt
python -m src.app
```

브라우저: `http://127.0.0.1:5000/` → **출력** 클릭.

---

## 알려진 정답 예시 (GREEN / refactor용)

표준 1~16 마방진, magic constant 34:

```
16  3  2 13
 5 10 11  8
 9  6  7 12
 4 15 14  1
```

---

## 릴리스 노트

### v0.2.0 — Entity · Boundary 구현 (main @ `a77dcd7`)

#### 기능

- **Entity INV-*** — `generate_magic_square()` 결과 7건 테스트 통과
- **Entity API** — `row_sums`, `col_sums`, `diag_sums`, `is_valid_magic_square`
- **AC-GEN-01** — 마방진 생성 + Flask 「출력」 웹 UI
- **Boundary E-*** — 입력 형상·타입·범위·중복 검증 11건

#### 테스트

- Entity 7 + Boundary 14 = **21 passed**

#### 다음 버전 예고

AC-VAL-01(4×4 입력 검증 UI) 및 AC-VAL-02(실패 규칙 구분) 구현.

### v0.1.0 — 마방진 생성기 Dual-Track TDD 프로젝트 초기 스캐폴드

> 기준: `95946d7`(Initial commit) · 첫 릴리스

#### 기타

- **프로젝트 초기 스캐폴드** — `AGENTS.md`, `pytest.ini`, `conftest.py`
- **PRODUCT-Spec** — [docs/PRODUCT-Spec.md](docs/PRODUCT-Spec.md) Mom Test 기반 계약 정의
- **Mom Test 보고서** — [report/01.mom-test-product-spec.REPORT.md](report/01.mom-test-product-spec.REPORT.md)

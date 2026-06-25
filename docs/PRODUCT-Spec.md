# MagicSquare_1004 개발 사양 (Draft v0.1)

## 1. 개요

| 항목 | 내용 |
|------|------|
| 프로젝트명 | MagicSquare_1004 (4×4 마방진 생성기) |
| 목적 | **4×4** 숫자 격자에서 **행·열·대각선(각 4칸)의 합이 34**이고, **각 셀이 3자리 이하 자연수(1~999)이며 서로 중복되지 않는** 배열을 다룬다 |
| 스택 | Python 3.12, pytest, Dual-Track TDD |
| 아키텍처 | ECB — Entity(`src/cart.py`), Boundary(`src/app.py`) |

---

## 2. Mom Test 해석 — 고객 말 → 계약

### 고객 발화 (원문)

> 가로 혹은 세로, 그리고 대각선이 4개인 경우 이 4개의 합이 34가 되어야 해.
> 각 셀의 값은 0이면 안 돼.
> 각 셀의 값은 0보다 큰 자연수여야 한다.
> 중복은 허용하지 않는다.

### 해석

| 고객 표현 | 기술적 의미 (4×4 고정) | 계약 유형 |
|-----------|------------------------|-----------|
| 가로 4개 합 = 34 | 4개 **행** 각각 `sum(row) == 34` | **Invariant** |
| 세로 4개 합 = 34 | 4개 **열** 각각 `sum(col) == 34` | **Invariant** |
| 대각선 4개 합 = 34 | **주대각선·부대각선** 각각 `sum == 34` | **Invariant** |
| 0보다 큰 자연수 | 모든 `cell >= 1` (양의 정수; 0·음수 불가) | **Invariant** |
| 3자리 이하 자연수 | `1 <= cell <= 999` | **Invariant** (`INV-RANGE-3DIGIT`) |
| 중복 불허 | 16칸 값 **서로 다름** | **Invariant** |

Mom Test 관점: 위는 **“어떤 입력/출력에서도 깨지면 안 되는 규칙”** → Entity 불변식(`INV-*`)이다.
**셀 값 상한(3자리 이하 자연수)** 은 확정되어 `INV-RANGE-3DIGIT`으로 분리한다.
**“생성기인지 검증기인지”** 는 프로젝트명·AC-GEN-01 기준 **생성 + 검증** 가정.

---

## 3. 범위

### In Scope (v0.1 — 고객 확인분)

- **4×4 정수 행렬만** 생성·검증 (다른 차수 제외)
- 행 4개, 열 4개, 대각선 2개 — 각 4칸 합 = **34**
- 모든 셀 **0보다 큰 자연수** (양의 정수, `>= 1`)
- 셀 값 **3자리 이하 자연수** (`1 <= cell <= 999`)
- 16칸 값 **중복 불허** (서로 다른 수)

### Out of Scope (v0.1 — 구현하지 않음)

- 3×3, 5×5 등 **4×4가 아닌** 다른 차수
- Flask UI·주문 폼 (`src/app.py`) — Entity 계약 확정 후
- **힌트, 풀이 과정, 난이도, 점수** (고려하지 않음)
- “부분 행/열”만 검사하는 UI (4×4 전체가 아닌 경우)

### 가정 (Assumptions)

| ID | 가정 | 상태 |
|----|------|------|
| A-1 | 격자 크기는 **4×4 고정** — 4×4 매트릭스만 생성 | **확정** |
| A-2 | 셀 값은 **양의 정수**(0보다 큰 자연수) | **확정** |
| A-3 | **생성 + 검증** 둘 다 필요 (프로젝트명 “생성기”) | 가정 |
| A-4 | 셀 값 **3자리 이하 자연수** (`1~999`); 중복 불허 | **확정** → `INV-RANGE-3DIGIT` |
| A-5 | 대각선은 **주대각선·부대각선** 2개만 | 가정 |

---

## 4. 도메인 모델 (Entity)

```
Matrix4x4 = list[list[int]]   # 4행 × 4열, 각 원소 int
MagicConstant = 34
LinesToCheck = 4 rows + 4 cols + 2 diagonals = 10 lines
```

**행/열/대각선 정의 (0-indexed)**

| 종류 | 인덱스 | 4칸 |
|------|--------|-----|
| 행 `r` | r ∈ {0,1,2,3} | `M[r][0..3]` |
| 열 `c` | c ∈ {0,1,2,3} | `M[0..3][c]` |
| 주대각선 | — | `M[i][i]`, i=0..3 |
| 부대각선 | — | `M[i][3-i]`, i=0..3 |

---

## 5. 불변식 (Invariant) — `tests/entity/`

Entity는 **유효한 4×4 마방진(또는 후보 행렬)** 이 항상 만족해야 하는 규칙.

| ID | 규칙 | 검증 조건 |
|----|------|-----------|
| **INV-ROW-SUM** | 각 행 4칸의 합 = 34 | `∀r: sum(M[r]) == 34` |
| **INV-COL-SUM** | 각 열 4칸의 합 = 34 | `∀c: sum(M[:,c]) == 34` |
| **INV-DIAG-SUM** | 주·부 대각선 각 4칸의 합 = 34 | `sum(M[i][i]) == sum(M[i][3-i]) == 34` |
| **INV-POSITIVE-NATURAL** | 모든 셀은 0보다 큰 자연수 | `∀i,j: M[i][j] >= 1` (정수) |
| **INV-RANGE-3DIGIT** | 셀 값은 3자리 이하 자연수 | `∀i,j: 1 <= M[i][j] <= 999` |
| **INV-UNIQUE** | 16칸 값 중복 없음 | `len(flat(M)) == len(set(flat(M)))` |

### Entity API (초안 — TDD RED에서 시그니처 확정)

```python
# src/cart.py (Entity — Flask import 금지)

def is_valid_magic_square(matrix: list[list[int]]) -> bool:
    """INV-ROW/COL/DIAG-SUM, INV-POSITIVE-NATURAL, INV-RANGE-3DIGIT, INV-UNIQUE 통합 검증"""

def row_sums(matrix: list[list[int]]) -> list[int]: ...
def col_sums(matrix: list[list[int]]) -> list[int]: ...
def diag_sums(matrix: list[list[int]]) -> tuple[int, int]: ...
```

### 권장 Invariant (형상)

| ID | 규칙 | 비고 |
|----|------|------|
| INV-SIZE | `len(matrix)==4 and all(len(row)==4 for row in matrix)` | 4×4 형상 불변 (A-1) |

---

## 6. 수용 조건 (AC) & Boundary 계약 — `tests/boundary/`

AC = **사용자가 “됐다”고 받아들이는 조건** (입력·출력·오류 UX).

### AC (기능 수준)

| ID | 수용 조건 |
|----|-----------|
| **AC-GEN-01** | 사용자가 생성을 요청하면, **INV-*를 모두 만족하는** 4×4 행렬을 받는다 |
| **AC-VAL-01** | 사용자가 4×4 행렬을 입력하면, 마방진 여부(합 34 + 1~999 자연수 + 중복 없음)를 알 수 있다 |
| **AC-VAL-02** | 조건 위반 시 **어느 규칙**에서 실패했는지 구분 가능 (선택, v0.2) |

### Boundary 입력 계약 (E-*)

| ID | 입력 | 기대 동작 |
|----|------|-----------|
| **E-MAT-SHAPE** | 4×4가 아닌 배열 | 거부 또는 `False` / 명확한 오류 |
| **E-CELL-ZERO** | 셀에 0 포함 | `is_valid` → `False` (INV-POSITIVE-NATURAL) |
| **E-CELL-NONINT** | 문자·실수·빈칸 | Boundary에서 거부 (Entity까지 안 감) |
| **E-CELL-NEG** | 음수 | `is_valid` → `False` (INV-POSITIVE-NATURAL) |
| **E-CELL-OVER-3DIGIT** | 999 초과 | `is_valid` → `False` (INV-RANGE-3DIGIT) |
| **E-CELL-DUP** | 동일 값 중복 | `is_valid` → `False` (INV-UNIQUE) |

Flask Boundary(`src/app.py`)는 **E-* 검증 후** Entity 호출만 담당.

---

## 7. ECB 책임 분리

| 레이어 | 파일 | 책임 |
|--------|------|------|
| **Entity** | `src/cart.py` | 합 계산, INV-* 검증, (확정 시) 마방진 **생성** 알고리즘 |
| **Boundary** | `src/app.py` | HTTP/폼 파싱, E-* 입력 검증, Entity 결과 표시 |
| **tests/entity/** | | INV-* 단위 테스트 (`@pytest.mark.entity`) |
| **tests/boundary/** | | E-*, UC-* 계약 테스트 (`@pytest.mark.boundary`) |

---

## 8. TDD 구현 순서 (RED → GREEN 권장)

과잉 구현 금지 — **계약 ID 없는 동작은 구현하지 않음**.

| 순서 | RED (tests만) | GREEN (최소 구현) |
|------|---------------|-------------------|
| 1 | `INV-POSITIVE-NATURAL` | 0·음수 포함 시 `False` |
| 2 | `INV-RANGE-3DIGIT` | 999 초과 시 `False` |
| 3 | `INV-UNIQUE` | 중복 값 포함 시 `False` |
| 4 | `INV-ROW-SUM` | 행 합 검증 |
| 5 | `INV-COL-SUM` | 열 합 검증 |
| 6 | `INV-DIAG-SUM` | 대각선 합 검증 |
| 7 | `INV-SIZE` (권장) | 4×4 형상 검증 |
| 8 | `AC-GEN-01` / 생성 | 4×4 알고리즘 (Siamese 등) |
| 9 | `E-*` Boundary | `app.py` + boundary tests |

**알려진 정답 예시 (GREEN/refactor용)** — 표준 1~16 마방진, magic constant 34:

```
16  3  2 13
 5 10 11  8
 9  6  7 12
 4 15 14  1
```

---

## 9. Mom Test — 사양 확정 전 확인 질문

사양을 **AC/Invariant로 잠그기 전** 고객에게 물어볼 것:

1. **생성**만 필요한가, **검증**만 필요한가, 둘 다인가?
2. ~~숫자 **범위·중복**은?~~ → **중복 불허 확정**; 값 범위 **3자리 이하 자연수(1~999) 확정** (`INV-RANGE-3DIGIT`)
3. ~~**음수·실수** 입력 가능한가?~~ → **음수·0 불가 확정**; 실수·문자는 Boundary(E-CELL-NONINT) 처리
4. ~~격자 크기는?~~ → **4×4만** 생성·검증 **확정** (A-1)
5. “대각선”은 **2개(주·부)** 만인가?
6. ~~힌트·풀이·난이도·점수?~~ → **고려하지 않음 확정** (Out of Scope)
7. 마지막으로 비슷한 문제를 풀 때 **실패한 순간**은 언제였는가? (오류 메시지 AC 근거)

---

## 10. 한 줄 요약

> **Invariant:** **4×4** 격자에서 모든 **행·열·주/부 대각선(각 4칸)** 의 합은 **34**, 모든 셀은 **3자리 이하 자연수(1~999)**, **16칸 값 중복 없음**.
> **AC(가정):** 위를 만족하는 **4×4** 행렬을 **생성·검증**할 수 있다.
> **제외:** 다른 차수, 힌트·풀이·난이도·점수. UI(Flask)는 Entity 계약 확정 후.

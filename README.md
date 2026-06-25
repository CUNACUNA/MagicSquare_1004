# MagicSquare_1004

4×4 마방진 생성기 — Python 3.12, pytest 기반 Dual-Track TDD(C2C 추적) 프로젝트.

> **목표:** 4×4 격자에서 모든 **행·열·주/부 대각선(각 4칸)** 의 합이 **34**, 모든 셀은 **0보다 큰 자연수**, **16칸 값 중복 없음**을 만족하는 행렬을 **생성·검증**한다.
>
> 상세 사양: [docs/PRODUCT-Spec.md](docs/PRODUCT-Spec.md) · 개발 규칙: [AGENTS.md](AGENTS.md)

## 아키텍처 (ECB)

| 레이어 | 경로 | 책임 |
|--------|------|------|
| **Entity** | `src/cart.py` | 합 계산, INV-* 검증, 마방진 생성 알고리즘 |
| **Boundary** | `src/app.py` | HTTP/폼 파싱, E-* 입력 검증, Entity 결과 표시 |
| **Entity 테스트** | `tests/entity/` | INV-* 불변식 (`@pytest.mark.entity`) |
| **Boundary 테스트** | `tests/boundary/` | E-*, AC-* 계약 (`@pytest.mark.boundary`) |

---

## 구현 로드맵

TDD 순서: **RED(테스트) → GREEN(최소 구현) → REFACTOR**. 계약 ID 없는 동작은 구현하지 않는다.

### 1. Entity — 불변식 검증 (`src/cart.py`, `tests/entity/`)

마방진(또는 후보 행렬)이 항상 만족해야 하는 규칙.

- [ ] **INV-POSITIVE-NATURAL** — 모든 셀은 0보다 큰 자연수 (`M[i][j] >= 1`)
- [ ] **INV-UNIQUE** — 16칸 값 중복 없음
- [ ] **INV-ROW-SUM** — 각 행 4칸의 합 = 34
- [ ] **INV-COL-SUM** — 각 열 4칸의 합 = 34
- [ ] **INV-DIAG-SUM** — 주대각선·부대각선 각 4칸의 합 = 34
- [ ] **INV-SIZE** — 4×4 형상 검증 (`len(matrix)==4`, 각 행 길이 4)

### 2. Entity — 검증 API (`src/cart.py`, `tests/entity/`)

불변식을 조합하는 Entity 공개 API.

- [ ] `row_sums(matrix)` — 4개 행 합 반환
- [ ] `col_sums(matrix)` — 4개 열 합 반환
- [ ] `diag_sums(matrix)` — (주대각선 합, 부대각선 합) 반환
- [ ] `is_valid_magic_square(matrix)` — INV-* 통합 검증 (`True` / `False`)

### 3. Entity — 마방진 생성 (`src/cart.py`, `tests/entity/`)

- [ ] **AC-GEN-01** — 생성 요청 시 INV-*를 모두 만족하는 4×4 행렬 반환 (Siamese 등 알고리즘)

### 4. Boundary — 입력 계약 (`src/app.py`, `tests/boundary/`)

Boundary에서 E-* 검증 후 Entity 호출. Entity까지 가지 않아야 하는 입력은 Boundary에서 거부.

- [ ] **E-MAT-SHAPE** — 4×4가 아닌 배열 → 거부 또는 `False` / 명확한 오류
- [ ] **E-CELL-ZERO** — 셀에 0 포함 → `is_valid` → `False`
- [ ] **E-CELL-NONINT** — 문자·실수·빈칸 → Boundary에서 거부
- [ ] **E-CELL-NEG** — 음수 → `is_valid` → `False`
- [ ] **E-CELL-DUP** — 동일 값 중복 → `is_valid` → `False`

### 5. Boundary — 수용 조건 & Flask UI (`src/app.py`, `tests/boundary/`)

사용자가 "됐다"고 받아들이는 기능 수준 조건.

- [ ] **AC-VAL-01** — 사용자가 4×4 행렬을 입력하면 마방진 여부(합 34 + 양의 정수 + 중복 없음) 확인 가능
- [ ] **AC-VAL-02** — 조건 위반 시 어느 규칙에서 실패했는지 구분 가능 *(선택, v0.2)*
- [ ] Flask 주문 폼 — 생성·검증 요청 UI, E-* 검증 후 Entity 결과 표시

### 6. 미확정 / 고객 확인 후 추가

Mom Test로 사양 확정 전까지 **구현 금지**.

- [ ] **INV-RANGE-1-16** — 셀 값 1~16 범위 *(Entity — A-4 상한 확정 시)*
- [ ] 3×3, 5×5 등 다른 차수 *(Out of Scope v0.1)*
- [ ] 힌트, 풀이 과정, 난이도, 점수 *(Out of Scope v0.1)*

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

## 빠른 시작

```bash
pytest -q              # 전체
pytest tests/entity -q # Entity (INV-*)
pytest tests/boundary -q # Boundary (E-*, AC-*)
```

---

## 릴리스 노트

### v0.1.0 — 마방진 생성기 Dual-Track TDD 프로젝트 초기 스캐폴드

> 기준: `95946d7`(Initial commit) → `HEAD` · 첫 릴리스

#### 기능

_(해당 없음 — 도메인 기능·테스트·구현 코드는 아직 포함되지 않음)_

#### 기타

- **프로젝트 초기 스캐폴드 구성** — TDD 개발 환경 기반 마련
  - `AGENTS.md`: ECB 구조, MomTest/계약 ID, RED→GREEN→REFACTOR 워크플로
  - `pytest.ini`: `entity` / `boundary` Dual-Track 마커
  - `conftest.py`, `.gitignore`
- **PRODUCT-Spec** — [docs/PRODUCT-Spec.md](docs/PRODUCT-Spec.md) Mom Test 기반 계약 정의

#### 다음 버전 예고

위 **구현 로드맵** 1번(Entity 불변식)부터 RED 테스트 추가를 권장합니다.

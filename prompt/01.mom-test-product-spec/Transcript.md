# 01. Mom Test · Product Spec — Prompt Transcript

| 항목 | 내용 |
|------|------|
| 작성일 | 2026-06-25 |
| 프로젝트 | MagicSquare_1004 |
| 관련 보고서 | [../../report/01.mom-test-product-spec.REPORT.md](../../report/01.mom-test-product-spec.REPORT.md) |
| 세션 ID | a761c7b3-dc61-43db-bba8-dbb2941515d0 |
| 원본 JSONL | [Transcript.jsonl](./Transcript.jsonl) |

---

## Prompt 1

**User**

```
/create-rule cursor ai를 위한 rule 생성하도록 도와줘
```

**Cursor**

Cursor rule 생성을 위해 create-rule 스킬과 프로젝트 컨텍스트를 확인합니다.

---

**Cursor**

프로젝트에 `AGENTS.md`는 있지만 `.cursor/rules/`는 아직 없습니다. 규칙 범위와 적용 방식을 먼저 정하면 맞춤 rule을 만들 수 있습니다.

---

## Prompt 2

**User**

```
---
description: Dual-Track TDD(RED·GREEN·REFACTOR) · C2C 추적 작업 규칙
globs:
alwaysApply: true
---
 
# 작업 규칙 (항상 적용)
- 사이클은 항상 RED → GREEN → REFACTOR 순서를 따른다.
- 가장 단순한 실패 테스트부터 쓰고, 통과시킬 최소 코드만 구현하고,
  전부 통과한 뒤에만 리팩터링한다.
- 구현 줄에는 충족한 계약 ID(INV-*/E-*)를 주석으로 단다.
- 구조적 변경과 동작적 변경을 한 커밋에 섞지 않는다(구조 먼저).
- 테스트를 수정·삭제·비활성화하거나 assert True/skip 으로 우회하지 않는다.
- 요청하지 않은 기능을 추가하지 않는다. 작업 끝에 `pytest -q` 로 전부 통과를 확인한다.
```

**Cursor**

제공하신 내용으로 `.cursor/rules/`에 항상 적용되는 TDD 규칙 파일을 생성합니다.

---

**Cursor**

`.cursor/rules/dual-track-tdd.mdc` 파일을 생성했습니다.

**적용한 조정**
- `alwaysApply: true`이면 `globs`는 필요 없어서 빈 `globs:` 줄은 제거했습니다.
- 파일명은 내용에 맞게 `dual-track-tdd.mdc`로 지었습니다.

**동작**
- 이 rule은 **모든 대화에 자동 적용**됩니다.
- Cursor Settings → Rules에서 "Dual-Track TDD(RED·GREEN·REFACTOR) · C2C 추적 작업 규칙"으로 확인할 수 있습니다.

**AGENTS.md와의 관계**
- `AGENTS.md`는 프로젝트 지도(ECB 구조, MomTest, 테스트 명령 등) 역할
- 이 rule은 **작업 중 AI가 지켜야 할 TDD 워크플로**에 집중

추가로 분리하면 좋은 rule 예시:
- `contracts.mdc` — MomTest, INV-*/E-*, ID 없는 동작 금지
- `ecb-structure.mdc` — `src/cart.py` / `src/app.py` 역할 (`globs: src/**`)

원하시면 이어서 만들어 드리겠습니다.

---

## Prompt 3

**User**

```
Next.js 15에서 미들웨어 설정하는 방법 알려줘. use context7
```

**Cursor**

Next.js 15 미들웨어 문서를 context7에서 조회합니다.

---

**Cursor**

Ask 모드에서는 context7 MCP 호출이 제한되어, 공식 Next.js 문서에서 미들웨어 설정 방법을 확인합니다.

---

**Cursor**

Next.js 15에서 미들웨어를 설정하는 방법입니다. (Ask 모드에서는 context7 MCP 호출이 제한되어, [Next.js v15.5.6 공식 문서](https://github.com/vercel/next.js/blob/v15.5.6/docs/01-app/03-api-reference/03-file-conventions/middleware.mdx) 기준으로 정리했습니다.)

---

## 1. 파일 위치

프로젝트 **루트** 또는 `src/` 디렉터리(`app/`과 같은 레벨)에 `middleware.ts` (또는 `.js`)를 만듭니다.

```
my-app/
├── middleware.ts   ← 여기
├── app/
├── package.json
```

`pageExtensions`를 커스터마이즈했다면 `middleware.page.ts`처럼 맞춰 이름을 지정합니다.

---

## 2. 기본 구조

파일에서 **하나의 함수**를 export하고, 선택적으로 **`config`** 객체를 함께 export합니다.

```tsx
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // redirect, rewrite, 헤더/쿠키 수정, 직접 응답 등
  return NextResponse.redirect(new URL('/home', request.url))
}

export const config = {
  matcher: '/about/:path*',
}
```

- `middleware` — default export 또는 named export `middleware` 둘 다 가능
- 한 파일에 미들웨어 함수는 **하나만** 지원
- 라우트 렌더링 **전**에 실행됨 (인증, 리다이렉트, 로깅 등에 적합)

---

## 3. `matcher`로 실행 경로 지정

`matcher` 없으면 **모든 경로**에서 미들웨어가 실행되므로, 보통 `config.matcher`로 범위를 좁힙니다.

### 단일 / 다중 경로

```ts
export const config = {
  matcher: ['/about/:path*', '/dashboard/:path*'],
}
```

### 정적 파일 제외 (자주 쓰는 패턴)

```ts
export const config = {
  matcher: [
    '/((?!api|_next/static|_next/image|favicon.ico|sitemap.xml|robots.txt).*)',
  ],
}
```

### 조건부 matcher (`has` / `missing`)

```ts
export const config = {
  matcher: [
    {
      source: '/api/:path*',
      has: [{ type: 'header', key: 'Authorization' }],
    },
    {
      source: '/dashboard/:path*',
      missing: [{ type: 'cookie', key: 'session' }],
    },
  ],
}
```

**matcher 규칙**
- `/`로 시작해야 함
- `:path*`, `:path+`, `:path?` 같은 path-to-regexp 문법 사용 가능
- **빌드 타임 정적 분석** → `matcher`는 **상수**여야 함 (변수에 넣으면 무시됨)
- `export const config = { ... }` 형태로 **직접 선언**해야 함 (별도 변수에 담아 re-export하면 인식 안 될 수 있음)

---

## 4. 자주 쓰는 동작

### 다음으로 통과

```ts
return NextResponse.next()
```

### 리다이렉트 / 리라이트

```ts
return NextResponse.redirect(new URL('/login', request.url))
return NextResponse.rewrite(new URL('/dashboard/user', request.url))
```

### 쿠키·헤더 설정

```ts
const response = NextResponse.next()
response.cookies.set('token', 'abc')
response.headers.set('x-custom', 'value')
return response
```

### 직접 JSON 응답 (인증 실패 등)

```ts
export const config = { matcher: '/api/:path*' }

export function middleware(request: NextRequest) {
  if (!isAuthenticated(request)) {
    return Response.json(
      { success: false, message: 'authentication failed' },
      { status: 401 }
    )
  }
}
```

---

## 5. Runtime (Next.js 15.5+)

기본값은 **Edge runtime**입니다. Node.js API가 필요하면:

```ts
export const config = {
  runtime: 'nodejs',
  matcher: '/api/:path*',
}
```

v15.5.0부터 Node.js runtime이 stable입니다.

---

## 6. 실행 순서 (참고)

미들웨어는 대략 다음 순서에서 **3번째**에 실행됩니다.

1. `next.config.js` headers  
2. `next.config.js` redirects  
3. **Middleware**  
4. 파일시스템 라우트 (`app/`, `pages/` 등)

---

## 7. 실전 예: 인증 가드

```ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const token = request.cookies.get('session')?.value

  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*'],
}
```

---

## 주의사항

| 항목 | 내용 |
|------|------|
| Static export | 미들웨어 **미지원** |
| 공유 모듈 | Edge/CDN 최적화 환경을 고려해 과도한 의존성 피하기 |
| 테스트 | v15.1+ `next/experimental/testing/server`로 matcher/동작 단위 테스트 가능 |

---

context7으로 최신 문서를 직접 조회하려면 **Agent 모드**로 전환해 주세요. Agent 모드에서는 context7 MCP로 `/vercel/next.js` 라이브러리 문서를 실시간 조회할 수 있습니다.

추가로 **인증**, **i18n locale**, **CORS** 같은 특정 시나리오 예제가 필요하면 말씀해 주세요.

---

## Prompt 4

**User**

```
▶ 프롬프트
Github MCP를 이용해서 내 GitHub 저장소 목록을 보여줘
```

**Cursor**

GitHub MCP 도구 스키마를 확인한 뒤 저장소 목록을 조회합니다.

---

**Cursor**

인증된 사용자 정보를 확인한 뒤 저장소 목록을 조회합니다.

---

**Cursor**

GitHub MCP로 조회한 **내 저장소 목록**입니다.

## 계정 정보

| 항목 | 값 |
|------|-----|
| 사용자 | [CUNACUNA](https://github.com/CUNACUNA) |
| Public 저장소 | 1 |
| 가입일 | 2022-11-06 |

---

## 저장소 목록 (총 1개)

| 저장소 | 설명 | 언어 | 공개 | 기본 브랜치 | 최근 push | ⭐ |
|--------|------|------|------|-------------|-----------|-----|
| [cursor-tdd-cart](https://github.com/CUNACUNA/cursor-tdd-cart) | cursor AI test repository, 작성자: 배대규, 리뷰어: 홍홍홍 | Python | Public | `main` | 2026-06-25 | 0 |

**추가 정보**
- Open Issues: 1
- Fork: 0
- 권한: Admin (push/pull 가능)
- Clone: `https://github.com/CUNACUNA/cursor-tdd-cart.git`

---

현재 계정에는 **public 저장소 1개**만 검색되었습니다. private 저장소가 더 있다면 GitHub MCP 토큰에 `repo` 스코프가 있어야 목록에 포함될 수 있습니다.

특정 저장소의 브랜치, PR, Issue 등을 더 보고 싶으면 알려 주세요.

---

## Prompt 5

**User**

```
Github MCP를 이용해서 @c:\dev\MagicSquare_1004 폴더 작업 내용을 모두 commit & push해줘
```

**Cursor**

로컬 변경사항과 원격 저장소 상태를 확인한 뒤 commit & push를 진행합니다.

---

**Cursor**

원격 저장소가 없어 GitHub MCP로 저장소를 생성한 뒤 파일을 push하고, 로컬 git과 동기화합니다.

---

**Cursor**

저장소가 이미 있어 GitHub MCP `push_files`로 파일을 push합니다.

---

**Cursor**

GitHub MCP `push_files`는 빈 저장소에서 실패해, 로컬 commit 후 push로 진행합니다.

---

**Cursor**

원격에 빈 README 초기 커밋이 있어 병합 후 push합니다.

---

**Cursor**

commit & push가 완료되었습니다.

## 결과 요약

**저장소:** [CUNACUNA/MagicSquare_1004](https://github.com/CUNACUNA/MagicSquare_1004)  
**브랜치:** `main` (origin 추적 설정됨)

### 커밋된 파일 (4개)

| 파일 | 설명 |
|------|------|
| `.gitignore` | Python/venv/pytest/IDE 제외 규칙 |
| `AGENTS.md` | 프로젝트 지도 (TDD, ECB 구조) |
| `conftest.py` | pytest import 경로 설정 |
| `pytest.ini` | entity/boundary 마커 설정 |

### 제외된 파일 (`.gitignore` 적용)

- `.cursor/rules/dual-track-tdd.mdc`
- `__pycache__/`, `.venv/`, `.pytest_cache/`

### 커밋 이력

```
3f866fc Merge branch 'main' of https://github.com/CUNACUNA/MagicSquare_1004
061216b chore: initial project setup — 마방진 생성기 TDD 스�affold
95946d7 Initial commit (빈 README.md — 원격 초기 커밋)
```

### 진행 과정

1. **GitHub MCP**로 저장소 `MagicSquare_1004` 확인 (이미 존재)
2. **GitHub MCP `push_files`** 시도 → 빈 저장소라 409 오류
3. 로컬 `git commit` → 원격 빈 README와 merge → `git push` 성공
4. **GitHub MCP `get_file_contents`**로 원격 파일 5개 확인 완료

로컬 working tree는 clean 상태이며 `origin/main`과 동기화되어 있습니다.

---

## Prompt 6

**User**

```
---
name: release-notes
description: 두 git 태그/커밋 사이의 변경으로 한국어 릴리스 노트를 작성한다. 사용자가 "릴리스 노트", "변경 로그", "changelog"를 언급하거나 배포 준비를 할 때 사용한다.
---

# Release Notes 작성

## 언제 사용하나
- 새 버전 배포 전, 마지막 릴리스 이후의 변경을 정리할 때

## 절차
1. `scripts/collect_commits.sh <이전태그> <현재태그>`를 실행해 커밋 목록을 수집한다.
2. 커밋을 `✨ 기능 / 🐛 버그 수정 / 🧹 기타`로 분류한다.
3. 사용자에게 보여줄 한국어 릴리스 노트를 다음 형식으로 작성한다:
   - 맨 위 한 줄 요약
   - 카테고리별 불릿 (이슈 번호가 있으면 붙인다)
4. 내부 리팩터링·오타 수정은 "기타"로 묶어 간결하게.

## 출력 형식
마크다운. 사용자에게 바로 복사 가능한 형태로 제시한다.
```

**Cursor**

릴리스 노트 작성 스킬을 만들기 위해 create-skill 가이드를 확인합니다.

---

**Cursor**

릴리스 노트 스킬과 참조 스크립트 `scripts/collect_commits.sh`를 생성합니다.

---

**Cursor**

요청하신 본문은 그대로 두고, 추가했던 보조 섹션은 제거합니다.

---

**Cursor**

`release-notes` 스킬과 참조 스크립트를 생성했습니다.

## 생성된 파일

| 경로 | 역할 |
|------|------|
| `.cursor/skills/release-notes/SKILL.md` | 릴리스 노트 작성 스킬 (제공하신 내용 그대로) |
| `scripts/collect_commits.sh` | 두 ref 사이 커밋 수집 스크립트 |

## 사용 방법

1. **자동 트리거:** "릴리스 노트", "변경 로그", "changelog", 배포 준비 등을 언급하면 에이전트가 스킬을 적용합니다.
2. **수동 호출:** 채팅에서 `/release-notes` 또는 스킬 이름을 지정해 사용할 수 있습니다.

## `collect_commits.sh` 예시

```bash
bash scripts/collect_commits.sh v1.0.0 v1.1.0
```

출력 형식: `커밋해시|메시지|작성자|날짜` (merge 커밋 제외)

## 참고

- `.cursor/`는 `.gitignore`에 포함되어 있어 **스킬 파일은 Git에 올라가지 않습니다** (로컬 전용).
- `scripts/collect_commits.sh`는 저장소에 커밋 가능합니다.
- Windows에서는 **Git Bash** 또는 WSL에서 스크립트를 실행하세요.

스킬을 팀과 공유하려면 `.gitignore`에서 `.cursor/skills/`만 예외 처리하거나, 개인 스킬 폴더(`~/.cursor/skills/`)로 옮기면 됩니다.

---

## Prompt 7

**User**

```
이번 버전 릴리스 노트 좀 만들어줘
```

**Cursor**

릴리스 노트 작성을 위해 release-notes 스킬과 git 이력을 확인합니다.

---

**Cursor**

**v0.1.0 — 마방진 생성기 Dual-Track TDD 프로젝트 초기 스캐폴드**

> 기준: `95946d7`(Initial commit) → `HEAD` (`3f866fc`) · git 태그 없음 — 첫 릴리스로 v0.1.0 가정

---

### ✨ 기능

_(해당 없음 — 도메인 기능·테스트·구현 코드는 아직 포함되지 않음)_

---

### 🐛 버그 수정

_(해당 없음)_

---

### 🧹 기타

- **프로젝트 초기 스캐폴드 구성** — 마방진 생성기 TDD 개발 환경 기반 마련 (`061216b`)
  - `AGENTS.md`: ECB 구조, MomTest/계약 ID, RED→GREEN→REFACTOR 워크플로, 커밋·금지 규칙 정의
  - `pytest.ini`: `entity`(INV-*) / `boundary`(E-*, UC-*) Dual-Track 마커 설정
  - `conftest.py`: `from src...` import를 위한 프로젝트 루트 경로 등록
  - `.gitignore`: Python, venv, pytest cache, IDE/OS 파일 제외
- **GitHub 저장소 연동** — `CUNACUNA/MagicSquare_1004` 원격 `main` 브랜치 push 완료
- **README.md** — 빈 파일로 초기 커밋에 포함 (`95946d7`)

---

### 다음 버전 예고

`AGENTS.md`에 정의된 구조(`src/cart.py`, `src/app.py`, `tests/entity/`, `tests/boundary/`)는 아직 미구현 상태입니다. v0.2.0부터 INV-*/E-* 계약 기반 RED 테스트 추가를 권장합니다.

---

GitHub Release에 붙일 태그 예시:

```bash
git tag -a v0.1.0 -m "chore: initial project scaffold"
git push origin v0.1.0
```

태그 이름이나 버전 번호를 다르게 쓰고 싶으면 알려 주세요.

---

## Prompt 8

**User**

```
릴리즈 노트 내용이 들어간 README.md 파일을 만들어줘
```

**Cursor**

`README.md`에 프로젝트 소개와 v0.1.0 릴리스 노트를 반영해 두었습니다.

포함 내용:
- 프로젝트 한 줄 설명
- v0.1.0 릴리스 노트 (기능 / 버그 수정 / 기타 / 다음 버전 예고)
- GitHub 저장소 링크
- `pytest -q` 빠른 시작
- `AGENTS.md` 참조 안내

커밋까지 진행할까요?

---

## Prompt 9

**User**

```
[역할 정의]
너는 롭 피츠패트릭의 저서 <The Mom Test>에 정통한 프로덕트 매니저(PM)이자 고객 개발 전문가야. 

[내 상황 및 목적]
4x4 매트릭스가 주어지면 가로 혹은 세로 4개 숫자의 합이 34가 되어야 해.
```

**Cursor**

프로젝트 맥락을 확인한 뒤 Mom Test 관점에서 답변합니다.

---

**Cursor**

좋아요. 역할은 받았습니다. Mom Test PM으로, 지금 주신 문장부터 같이 풀어볼게요.

---

## 먼저 짚고 넘어갈 것

말씀하신 내용은 **솔루션/규칙**에 가깝습니다.

> “4×4 매트릭스에서 가로·세로 4개 숫자의 합이 34”

수학적으로는 **4×4 마방진(magic constant 34)** 규칙과 맞닿아 있어요.  
Mom Test 관점에서는 이걸 바로 “만들 기능”으로 받아들이지 않고, **누가·언제·왜 이 문제를 겪는지**부터 확인해야 합니다.

`AGENTS.md`에서도 Mom Test는 기능 요구를 확정하는 도구가 아니라, **실제 사례에서 테스트 가능한 계약을 발견**하는 Discovery 도구라고 되어 있습니다.

---

## 지금 문장에서 보이는 것

| 구분 | 내용 | Mom Test 판단 |
|------|------|----------------|
| **Invariant 후보** | “가로·세로 각 4칸의 합 = 34” | 어떤 입력에서도 깨지면 안 되는 **규칙**으로는 명확 |
| **아직 불명확** | 누가, 어떤 상황에서, 무엇 때문에 | AC(사용자가 받아들이는 조건)를 정하기엔 정보 부족 |
| **위험 신호** | “혹은” | 대각선·전체 16칸·빈칸 허용 등 범위가 아직 열려 있음 |

“가로 **혹은** 세로”만인지, 대각선·부분 행·사용자 입력 검증까지인지에 따라 **완전히 다른 제품**이 됩니다.

---

## Mom Test식 질문 (과거 행동 중심)

아래는 **“이런 앱 만들면 쓸래?”**가 아니라, **이미 겪은 일**을 끌어내는 질문입니다.

### 1. 문제의 출발점
- **최근 3개월 안에** 4×4 숫자 배열을 직접 맞춰본 적이 있나요? (종이, 엑셀, 퍼즐 앱 등)
- 그때 **뭐가 제일 귀찮았나요?** (합 계산? 배치 찾기? 정답 확인? 설명?)
- 그걸 **몇 분/몇 시간** 썼고, **끝까지** 했나요, 중간에 그만뒀나요?

### 2. 대안과 비용
- 지금은 **어떻게** 확인하나요? (손계산, 계산기, 검색, GPT, 교재 답지?)
- 틀렸을 때 **어떻게** 알았나요? 누가 알려줬나요?
- **돈·시간·스트레스** 중 뭐를 가장 아까워했나요?

### 3. “34”의 의미
- **34**는 교재/시험/퍼즐 규칙에서 **고정**인가요, 아니면 “합이 같으면 된다” 수준인가요?
- 숫자는 **1~16 고정**인가요, **임의 입력**인가요, **빈칸 채우기**인가요?

### 4. 사용자 한 명을 특정하기
- 본인 연습용인가요, **학생·수업·숙제**인가요, **퍼즐 앱**인가요?
- **마지막으로** 이 문제를 푼 사람은 누구였고, 그때 **성공/실패** 기준이 뭐였나요?

---

## Mom Test에서 피할 질문

- ❌ “4×4 마방진 생성기 만들면 좋을 것 같지 않아?”
- ❌ “합 34 검증 기능 있으면 쓸 의향 있어?”
- ❌ “UI는 이렇게 하면 어때?”

→ 전부 **가상의 미래**라서, “응, 좋네”만 나오기 쉽습니다.

---

## 다음 단계 제안

한 줄만 더 알려주시면, Invariant / AC 초안을 같이 쪼갤 수 있어요.

1. **누구**를 위한 건가요? (본인 / 학생 / 교사 / 퍼즐 유저)
2. **생성**인가요, **검증**인가요, **힌트/풀이**인가요?
3. **실제로 마지막으로** 이 문제를 다룬 날, 무엇을 하려다 막혔나요?

이 세 가지에 답해 주시면, Mom Test 인터뷰 형식으로 **E-*(입력/UI 계약)** 과 **INV-*(불변식)** 후보를 나눠 드리겠습니다.

---

## Prompt 10

**User**

```
고객의 요구사항은
가로 혹은 세로, 그리고 대각선이 4개인 경우 이 4개의 합이 34가 되어야해
그리고 각 셀의 값은 0이면 안돼.

이 프로젝트에 대해 개발사양을
```

**Cursor**

프로젝트 구조와 기존 계약 정의를 확인한 뒤 개발 사양을 정리합니다.

---

**Cursor**

**MagicSquare_1004** 개발 사양입니다. 고객 발화를 Mom Test·`AGENTS.md` 계약 체계(ECB, INV-*, E-*)에 맞춰 정리했습니다. `src/`·`tests/`는 아직 없으므로 **스캐폴드 이후 첫 구현 기준**으로 작성했습니다.

---

# MagicSquare_1004 개발 사양 (Draft v0.1)

## 1. 개요

| 항목 | 내용 |
|------|------|
| 프로젝트명 | MagicSquare_1004 (4×4 마방진 생성기) |
| 목적 | 4×4 숫자 격자에서 **행·열·대각선(각 4칸)의 합이 34**이고 **셀 값이 0이 아닌** 배열을 다룬다 |
| 스택 | Python 3.12, pytest, Dual-Track TDD |
| 아키텍처 | ECB — Entity(`src/cart.py`), Boundary(`src/app.py`) |

---

## 2. Mom Test 해석 — 고객 말 → 계약

### 고객 발화 (원문)
> 가로 혹은 세로, 그리고 대각선이 4개인 경우 이 4개의 합이 34가 되어야 해.  
> 각 셀의 값은 0이면 안 돼.

### 해석

| 고객 표현 | 기술적 의미 (4×4 고정) | 계약 유형 |
|-----------|------------------------|-----------|
| 가로 4개 합 = 34 | 4개 **행** 각각 `sum(row) == 34` | **Invariant** |
| 세로 4개 합 = 34 | 4개 **열** 각각 `sum(col) == 34` | **Invariant** |
| 대각선 4개 합 = 34 | **주대각선·부대각선** 각각 `sum == 34` | **Invariant** |
| 셀 값 ≠ 0 | 모든 `cell != 0` | **Invariant** |

Mom Test 관점: 위는 **“어떤 입력/출력에서도 깨지면 안 되는 규칙”** → Entity 불변식(`INV-*`) 후보입니다.  
**“생성기인지 검증기인지, 숫자 범위·중복 허용”**은 고객이 아직 말하지 않았으므로 **AC·Boundary(`E-*`)** 또는 **미확정**으로 분리합니다.

---

## 3. 범위

### In Scope (v0.1 — 고객 확인분)
- 4×4 정수 행렬 표현
- 행 4개, 열 4개, 대각선 2개 — 각 4칸 합 = **34**
- 모든 셀 **0 금지**

### Out of Scope (v0.1 — 명시 전까지 구현 금지)
- 3×3, 5×5 등 다른 차수
- Flask UI·주문 폼 (`src/app.py`) — Entity 계약 확정 후
- 힌트, 풀이 과정, 난이도, 점수
- “부분 행/열”만 검사하는 UI (4×4 전체가 아닌 경우)

### 가정 (Assumptions) — **고객 재확인 필요**

| ID | 가정 | 미확정 시 리스크 |
|----|------|------------------|
| A-1 | 격자 크기는 **4×4 고정** | 크기 입력 시 E-* 추가 필요 |
| A-2 | 셀 값은 **정수** | 실수/문자 입력 처리 미정 |
| A-3 | **생성 + 검증** 둘 다 필요 (프로젝트명 “생성기”) | 검증만이면 범위 축소 |
| A-4 | 1~16 **서로 다른 수** (표준 4×4 마방진) | 중복 허용 시 해 space 폭발 |
| A-5 | 대각선은 **주대각선·부대각선** 2개만 | “대각선” 범위 확장 가능 |

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
| **INV-NO-ZERO** | 모든 셀 ≠ 0 | `∀i,j: M[i][j] != 0` |

### Entity API (초안 — TDD RED에서 시그니처 확정)

```python
# src/cart.py (Entity — Flask import 금지)

def is_valid_magic_square(matrix: list[list[int]]) -> bool:
    """INV-ROW/COL/DIAG-SUM, INV-NO-ZERO 통합 검증"""

def row_sums(matrix: list[list[int]]) -> list[int]: ...
def col_sums(matrix: list[list[int]]) -> list[int]: ...
def diag_sums(matrix: list[list[int]]) -> tuple[int, int]: ...
```

**선택적 Invariant (고객 확인 후 추가)**

| ID | 규칙 | 비고 |
|----|------|------|
| INV-SIZE | `len(matrix)==4 and all(len(row)==4 for row in matrix)` | 형상 불변 |
| INV-UNIQUE | 16칸 값 서로 다름 | 표준 마방진 |
| INV-RANGE-1-16 | `1 <= cell <= 16` | A-4 확정 시 |

---

## 6. 수용 조건 (AC) & Boundary 계약 — `tests/boundary/`

AC = **사용자가 “됐다”고 받아들이는 조건** (입력·출력·오류 UX).

### AC (기능 수준)

| ID | 수용 조건 |
|----|-----------|
| **AC-GEN-01** | 사용자가 생성을 요청하면, **INV-*를 모두 만족하는** 4×4 행렬을 받는다 |
| **AC-VAL-01** | 사용자가 4×4 행렬을 입력하면, 마방진 여부(합 34 + 0 아님)를 알 수 있다 |
| **AC-VAL-02** | 조건 위반 시 **어느 규칙**에서 실패했는지 구분 가능 (선택, v0.2) |

### Boundary 입력 계약 (E-*)

| ID | 입력 | 기대 동작 |
|----|------|-----------|
| **E-MAT-SHAPE** | 4×4가 아닌 배열 | 거부 또는 `False` / 명확한 오류 |
| **E-CELL-ZERO** | 셀에 0 포함 | `is_valid` → `False` (INV-NO-ZERO) |
| **E-CELL-NONINT** | 문자·실수·빈칸 | Boundary에서 거부 (Entity까지 안 감) |
| **E-CELL-NEG** | 음수 | A-2/A-4 확정 전 **미구현** 또는 `False` |

Flask Boundary(`src/app.py`)는 **E-* 검증 후** Entity 호출만 담당.

---

## 7. ECB 책임 분리

| 레이어 | 파일 | 책임 |
|--------|------|------|
| **Entity** | `src/cart.py` | 합 계산, INV-* 검증, (확정 시) 마방진 **생성** 알고리즘 |
| **Boundary

...(truncated)...

---

## Prompt 11

**User**

```
이 내용을 @c:\dev\MagicSquare_1004\ 폴더아래 docs 폴더아래 PRODUCT-Spec.md 파일이름으로 저장해줘
```

**Cursor**

`docs/PRODUCT-Spec.md`에 저장했습니다.

**경로:** `c:\dev\MagicSquare_1004\docs\PRODUCT-Spec.md`

포함 내용:
- 개요 및 Mom Test 해석
- In/Out of Scope, 가정(A-1~A-5)
- INV-*, AC-*, E-* 계약 정의
- ECB 책임 분리, TDD 구현 순서
- Mom Test 후속 확인 질문

커밋까지 진행할까요?

---

## Prompt 12

**User**

```
@c:\dev\MagicSquare_1004\ 폴더 아래 report 폴더 안에 보고서를 생성하고 prompt 폴더안에 폴더에 Transcript도 Export 해줘. 01.XXX 형식으로 저장해야 해.
```

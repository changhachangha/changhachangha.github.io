# 가격의 문법 — 챕터 작성 규약

이 문서는 "가격의 문법" 핸드북의 모든 챕터에 적용되는 공통 규약이다.
챕터 작성자는 이 문서를 먼저 끝까지 읽고 작업한다.

## 0. 파일 규약

- 각 챕터의 원본은 `chapters/chNN.html` 다. `<section>` 바깥 태그와 `.pager`는
  쓰지 않는다 — `scripts/build.py`가 생성한다.
- `index.html`을 직접 수정하지 않는다. 빌드가 파셜을 병합한다.
- 챕터 파일 맨 위 두 줄 형식:
  ```html
  <!-- CHAPTER 05 · smc -->
  <!-- LEX: [{"t":"spring(일시 이탈 후 회수)","k":"구조","p":"theories","aka":"스프링 shakeout","d":"range 하단을 깨고 즉시 회수하는 사건."}] -->
  ```
- `LEX` 블록: 이 챕터에서 처음 정의되는 색인 용어 목록(JSON 배열). 필드는
  `t`(표제어) `k`(분류: 이론/구조/패턴/지표/언어) `p`(이 챕터의 페이지 id)
  `aka`(검색 별칭) `d`(한 줄 정의). 없으면 블록 자체를 생략.
  `t`는 영어 원어다. 뜻이 있는 용어만 괄호에 그 뜻을 둔다. 인명에는 뜻을 붙이지 않는다.
  예전 한글 음차는 `aka`에만 둔다. 보이는 표제어로 쓰지 않는다.
- 플래그 주석: `<!-- STRUCTURE-ONLY -->`(내용 검사 제외, 16/17 전용),
  `<!-- NO-SOURCES -->`(출처 블록 생략, 00 전용).

## 1. 본문 구조 (확장 챕터 공통 골격)

```html
<div class="crumb">Chapter 05</div>
<h2 class="page-title">smart money · 유동성 언어</h2>
<p class="lede">한 단락 리드.</p>

<div class="chapter-summary"><b>요약.</b> 3~5문장으로 이 챕터 전체를 압축.</div>

<nav class="chapter-toc">
  <div class="toc-title">이 챕터에서</div>
  <ol>
    <li><a data-scroll="sec-smc-1">유동성 — 스톱이 모이는 자리</a></li>
    <li><a data-scroll="sec-smc-2">…</a></li>
  </ol>
</nav>

<h3 id="sec-smc-1">유동성 — 스톱이 모이는 자리</h3>
<p>정의 → 근거/메커니즘. 전문 용어는 첫 등장에 각주를 단다.
spring(일시 이탈 후 회수)<sup class="fnref" id="fnref-smc-1"><a data-scroll="fn-smc-1">1</a></sup>은
… <sup class="cit"><a data-scroll="src-smc-1">[1]</a></sup></p>
<figure class="fig">
  <img src="images/ch05/sweep.svg" alt="range 하단 이탈 후 즉시 회수하는 spring" loading="lazy" />
  <figcaption>그림 1. spring의 구조. …
    <span class="src">출처: 자체 제작</span></figcaption>
</figure>
<p>실전 적용(시나리오+무효화)과 한계·반례까지 한 섹션.</p>

…(h3 개념 섹션 4~7개 반복)…

<div class="footnotes">
  <div class="fn-title">용어 각주</div>
  <ol>
    <li id="fn-smc-1"><b>spring(일시 이탈 후 회수)</b>: range 하단을 일시 이탈 후 즉시
    회수하는 Wyckoff 매집 이벤트. liquidity sweep과 같은 사건.
    <a class="fnback" data-scroll="fnref-smc-1">↩</a></li>
  </ol>
</div>

<div class="sources">
  <div class="src-title">출처</div>
  <ol>
    <li id="src-smc-1">Wyckoff, R. D., <i>The Richard D. Wyckoff Method of
    Trading and Investing in Stocks</i>, 1931 코스.</li>
    <li id="src-smc-2">저자, "글 제목", https://… (접속일 2026-09-23).</li>
  </ol>
</div>
```

- id 규칙: `sec-{페이지id}-{n}`, `fnref-{페이지id}-{n}`, `fn-{페이지id}-{n}`,
  `src-{페이지id}-{n}`. 페이지 id는 파일 헤더 주석에 있다(home, map, smc …).
- **금지**: 챕터 내부에서 `href="#…"` 링크 — 해시 라우터와 충돌한다.
  모든 내부 이동은 `data-scroll` 속성만 사용한다.
- 챕터 간 이동은 `.pager`가 자동 생성하니 본문에 넣지 않는다.
  다른 챕터를 본문에서 언급할 때는 `<a href="#{페이지id}">`만 쓸 수 있다
  (페이지 id만 유효).

## 2. 내용 규약

- **원전 기준**: 정의·조건·수치는 원전/표준 교과서에서 가져온다.
  Dow(WSJ 사설 → Hamilton → Rhea 정리), Wyckoff(1931 코스, *Studies in Tape
  Reading*), Elliott(Frost & Prechter, *Elliott Wave Principle*), candle(Nison,
  *Japanese Candlestick Charting Techniques*), Market Profile(Steidlmayer),
  Bollinger(*Bollinger on Bollinger Bands*), Murphy(*Technical Analysis of the
  Financial Markets*), harmonic(Carney), Elder(*Trading for a Living*) 등.
  블로그 2차 정리 문구를 그대로 베끼지 않는다.
- **교차 표기**: 같은 사건의 다른 이름은 반드시 같이 쓴다
  (spring=liquidity sweep, FVG=gap/비효율, CHoCH=Dow 반전 신호).
  LEX에 등록하면 16 용어 색인이 빌드에서 자동 동기화된다.
- **기존 압축 메모 흡수**: 파셜에 남아 있는 기존 압축 문구의 모든 주장과
  용어가 새 본문 어딘가에 살아남아야 한다. 표현은 바뀌어도 내용은 보존.
- **분량**: 본문 5,000~8,000자(태그 제외, 공백 포함). `build.py --stats`로 확인.
- **시나리오 프레임**: 예언이 아니라 "조건 → 시나리오 → 무효화 가격"으로 쓴다.
- **한계·반례**: 각 개념 섹션 끝에 실패 조건이나 학술적 반론을 둔다.

## 3. 문체

- 기존 사이트 톤: 단문, 고밀도, 과장·광고성 표현 금지.
- "~해야 한다"가 아니라 "~다" 체. 독자에게 말을 거는 구어체도 쓰지 않는다.
- 절 제목은 FAQ·슬라이드식 「~인가」「~무엇인가」「왜 ~하는가」「~하는 법」「~을 만났을 때」를 피한다. 주어가 되는 명사나 책의 소제목으로 쓴다 — 창고의 목적, 분류의 이유, 유동성 언어의 계보. 본문 속의 수사적 물음까지 금하지는 않는다.
- 「이 챕터는 ~를 다룬다」「이 페이지의 몫이다」「이 절의 범위다」「여기서는 ~만 본다」처럼 글이 자기 범위를 해설하는 틀 문장을 반복하지 않는다. 요약 상자의 문장을 본문 첫 단락에서 다시 옮기지 않는다.
- 「핵심은 하나다」「공통 결론은 하나다」「남는 쓸모는」 같은 병렬 상투는 아껴 쓴다. 조건 → 시나리오 → 무효화는 기술 프레임이므로 유지한다.
- 마무리 상투구("결론적으로", "~이 중요하다", "중요한 것은", "무엇보다") 금지.
- 작성 완료 후 `korean-humanizer` 스킬로 윤문하고 `korean-spell-check`로
  맞춤법을 검사한다.

잠근 표기 — 본문·LEX·도해 라벨·사이드바에 공통이다.

영어 이름은 소리 나는 대로 한글로 옮기지 않는다. 라코니쇼크처럼 쓰지 않고 Lakonishok이라고 쓴다.

- **인명**은 영어만 쓴다. 성이나 이름 옆에 한국어 뜻을 붙이지 않는다. 이름에는 뜻이 없다. Brock, Lakonishok, LeBaron. Dow, Wyckoff, Elliott, Gann, Hurst, Fibonacci, Bollinger, Murphy, Bulkowski, Nison도 같다. 성으로 만든 지표·지수 이름(Bollinger Bands, Dow)도 영어 이름을 유지한다.
- **인명이 아닌 용어**는 영어 단어를 쓴다. 책에 이미 있는 뜻이 있을 때만 그 뜻을 곁에 둔다. 뜻을 만들지 않는다. 예: gap(창), candle(봉), neckline(목선), head and shoulders(머리어깨), momentum(탄력), divergence(괴리), confluence(합류), pitchfork(삼지창), spring(일시 이탈 후 회수), tenets(원칙), harmonic(조화). premium·discount는 이 책이 정의하는 위쪽 절반·아래쪽 절반이다.
- 한국어 뜻은 그 장에서 처음 나올 때, 용어를 정의하는 문장, 그리고 색인 표제어에만 둔다. 이후 반복은 영어만 쓴다.
- 예전 한글 음차(스프링, 벌코프스키, 헤드앤숄더, 다우, 와이코프 등)는 검색 별칭 `aka`에만 남긴다.
- 일본어를 읽은 이름과 차트 말은 음차가 아니다. 도지, 하라미, 마루보즈, 하이킨아시, 렌코, 사카타, 혼마 무네히사, 호소다, 일목·일목산인은 그대로 둔다. 이미 붙어 있는 뜻(임신, 깎은 머리, 한눈에 균형)도 유지한다.
- 이미 자리 잡은 말과 책의 한국어는 영어 머리말로 되돌리지 않는다. 차트, 패턴, 시스템, 데이터, 모델, 필터, 리스크, 페이지, 지지·저항, 가짜 돌파, 공정가치, 비석형.
- **지지·저항.** 붙여 쓰지 않는다.
- **왼어깨·오른어깨.** 좌어깨·우어깨라고 쓰지 않는다.
- **공정가치**는 경매·VWAP·POC가 가리키는 가격이다. 빈 구간은 **공정가치 gap**(Fair Value Gap, FVG)이다. 공정가·공정가 gap으로 줄이지 않는다.
- **가짜 돌파.** 붙여 쓰지 않는다.
- **이중 천장·바닥.** 천장바닥으로 붙이지 않는다.
- **비석형** (gravestone doji).
- 존의 무효화 경계는 **바깥 끝**, swing 앵커의 무효화 경계는 **반대쪽 끝**이라고 적는다.

## 4. 이미지

- 핵심 개념마다 차트 예시 1개 이상. 챕터당 보통 3~6개.
- 저장 위치: `images/chNN/`.
- 우선순위:
  1. 라이선스가 허용하는 원본(Wikimedia Commons 등 CC/PD, 재사용 허용 명시된
     공식 문서) — 파일을 로컬에 저장하고 캡션 `.src`에 `출처: 이름 (CC BY-SA 4.0)` 표기.
  2. 없으면 자체 SVG — 배경 `#f7f1e6`, 상승 `#2c5a4c`, 하락 `#8f3d3a`,
     보조선 `#b08948`, 텍스트 `#4a453c`. 라벨은 영어 원어.
     뜻이 있는 용어의 한국어는 그 장 캡션의 첫 언급에만 둔다.
     캡션 `.src`는 `자체 제작`.
- 라이선스 불명 이미지는 긁지 않는다. 핫링크 금지 — 반드시 로컬 파일.
- 캡션 형식: `그림 N. 한 줄 설명. …` + `<span class="src">출처: …</span>`.

## 5. 출처

- 책: `저자, *제목*(이탤릭), 판/연도, 해당 장`. fetch 없이 인용 가능.
- 웹: `제목, URL (접속일 YYYY-MM-DD)` — **실제로 접속해 확인한 페이지만** 인용.
- 본문에서 `<sup class="cit"><a data-scroll="src-{id}-{n}">[n]</a></sup>`로 연결.
- 챕터당 출처 3개 이상, 원전 우선.

## 6. 완료 전 자가 점검

- [ ] `python3 scripts/build.py --check {페이지id}` ERROR 0 (warn은 가능한 해소)
- [ ] `python3 scripts/build.py --stats` 에서 내 챕터 5,000~8,000자
- [ ] 필수 블록: chapter-summary, chapter-toc, figure.fig(figcaption+출처),
      footnotes, sources
- [ ] data-scroll 대상 id 전부 존재, `href="#"` 내부 링크 없음
- [ ] 기존 압축 메모의 주장·용어 누락 없음
- [ ] LEX 블록 JSON 파싱 가능, 색인에 넣을 용어 누락 없음
- [ ] index.html 직접 수정 안 함, build.py 실행(쓰기) 안 함
  (check는 읽기 전용이라 실행 가능)

## 7. 챕터별 메모

- ch00 home(표지): hero와 카드 링크 유지. 아래에 서문 본문 — 핸드북 구조,
  읽는 순서, 표기 규약, 면책. sources 생략 가능(NO-SOURCES 유지).
- ch09 atlas(패턴 도감): 기존 `.atlas` SVG 그리드 유지. 패턴군별 장문 섹션 추가.
- ch16 lexicon, ch17 notes: STRUCTURE-ONLY — 내용 확장 없음. 건드리지 않는다.

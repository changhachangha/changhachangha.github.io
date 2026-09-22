#!/usr/bin/env python3
"""가격의 문법 — index.html 빌드/검증 스크립트.

chapters/chNN.html 이 각 페이지 본문의 원본이다.
index.html 은 쉘(head/CSS/nav/script)을 소유하고, 마커 구역만 재생성한다.

    <!-- PAGE:{id} --> ... <!-- /PAGE:{id} -->   →  <section> + 파셜 + .pager
    // LEXICON:BEGIN ... // LEXICON:END          →  const lexicon = [...]

용법:
    python3 scripts/build.py              index.html 재생성
    python3 scripts/build.py --check      재생성 결과를 메모리에서 검증 (파일 쓰기 없음)
    python3 scripts/build.py --check smc  특정 챕터만 내용 검증 (병렬 작업 중 사용)
    python3 scripts/build.py --stats      챕터별 본문 글자수
    python3 scripts/build.py --init       일회성: index.html → 파셜 분리 + 마커 삽입
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
CH_DIR = ROOT / "chapters"

LEX_RE = re.compile(r"<!--\s*LEX:\s*(\[.*?\])\s*-->", re.S)
FLAG_RE = re.compile(r"<!--\s*(STRUCTURE-ONLY|NO-SOURCES|NO-FIG)\s*-->")
SEC_RE = '<section class="page" id="page-%s">(.*?)</section>'
ATTR_RE = re.compile(r"출처|자체 제작|©|CC BY|CC0|Public [Dd]omain|공정사용|Wikimedia")

REQUIRED_CLASSES = ["chapter-summary", "chapter-toc", "footnotes", "sources"]
LEN_HARD_MIN, LEN_HARD_MAX = 3500, 12000
LEN_SOFT_MIN, LEN_SOFT_MAX = 4800, 8800


def read_index():
    return INDEX.read_text(encoding="utf-8")


def page_ids(html):
    m = re.search(r"const pages = \[(.*?)\];", html, re.S)
    return re.findall(r'"(\w+)"', m.group(1))


def title_map(html):
    m = re.search(r"const titles = \{(.*?)\};", html, re.S)
    return dict(re.findall(r'(\w+):\s*"([^"]*)"', m.group(1)))


def chapter_file(i):
    return CH_DIR / f"ch{i:02d}.html"


def load_partial(i):
    f = chapter_file(i)
    return f.read_text(encoding="utf-8") if f.exists() else None


def lex_entries(inner):
    out = []
    for m in LEX_RE.finditer(inner):
        out += json.loads(m.group(1))
    return out


def flags(inner):
    return set(FLAG_RE.findall(inner))


def pager_for(ids, tmap, i):
    links = []
    if i > 0:
        links.append(f'<a href="#{ids[i-1]}">← {tmap[ids[i-1]]}</a>')
    if i < len(ids) - 1:
        links.append(f'<a href="#{ids[i+1]}">{tmap[ids[i+1]]} →</a>')
    return '        <div class="pager">' + "".join(links) + "</div>"


def render_lexicon(entries):
    j = lambda v: json.dumps(v, ensure_ascii=False)
    lines = ["    const lexicon = ["]
    for e in entries:
        lines.append(
            f'      {{ t: {j(e["t"])}, k: {j(e["k"])}, p: {j(e["p"])}, '
            f'aka: {j(e.get("aka", ""))}, d: {j(e["d"])} }},'
        )
    lines.append("    ];")
    return "\n".join(lines)


def build(src):
    """index.html 문자열을 받아 재생성된 문자열을 반환한다."""
    ids = page_ids(src)
    tmap = title_map(src)
    lex = []
    seen = set()
    for i, pid in enumerate(ids):
        inner = load_partial(i)
        if inner is None:
            continue
        for e in lex_entries(inner):
            if e["t"] not in seen:
                seen.add(e["t"])
                lex.append(e)
        section = (
            f'<section class="page" id="page-{pid}">\n'
            + inner.rstrip()
            + "\n"
            + pager_for(ids, tmap, i)
            + "\n      </section>"
        )
        pat = re.compile(
            r"(<!-- PAGE:%s -->).*?(<!-- /PAGE:%s -->)" % (pid, pid), re.S
        )
        src, n = pat.subn(
            lambda m: m.group(1) + "\n      " + section + "\n      " + m.group(2),
            src,
            count=1,
        )
        if n == 0:
            print(f"경고: PAGE 마커 없음 — {pid}", file=sys.stderr)
    src = re.sub(
        r"(// LEXICON:BEGIN).*?(// LEXICON:END)",
        lambda m: m.group(1) + "\n" + render_lexicon(lex) + "\n    " + m.group(2),
        src,
        flags=re.S,
        count=1,
    )
    return src


def text_len(sec_html):
    txt = re.sub(r"<!--.*?-->", "", sec_html, flags=re.S)
    txt = re.sub(r"<[^>]+>", "", txt)
    return len(re.sub(r"\s+", " ", txt).strip())


def init():
    """현재 index.html의 section을 chapters/ 파셜로 분리하고 마커를 삽입한다."""
    html = read_index()
    ids = page_ids(html)
    CH_DIR.mkdir(exist_ok=True)

    # 1) section 추출 → 파셜, index.html 에는 마커만 남김
    for i, pid in enumerate(ids):
        m = re.search(SEC_RE % pid, html, re.S)
        if not m:
            print(f"섹션을 찾지 못함: {pid}")
            continue
        inner = re.sub(r"\n?\s*<div class=\"pager\">.*?</div>\s*$", "", m.group(1), flags=re.S)
        chapter_file(i).write_text(
            f"<!-- CHAPTER {i:02d} · {pid} -->\n" + inner.rstrip() + "\n",
            encoding="utf-8",
        )
        html = (
            html[: m.start()]
            + f"<!-- PAGE:{pid} -->\n      <!-- /PAGE:{pid} -->"
            + html[m.end() :]
        )

    # 2) 기존 lexicon 항목을 소속 챕터(p 필드)의 LEX 블록으로 이주
    lm = re.search(r"const lexicon = \[(.*?)\];", html, re.S)
    entry_re = re.compile(
        r'\{\s*t:\s*"((?:[^"\\]|\\.)*)",\s*k:\s*"((?:[^"\\]|\\.)*)",\s*'
        r'p:\s*"((?:[^"\\]|\\.)*)",\s*aka:\s*"((?:[^"\\]|\\.)*)",\s*'
        r'd:\s*"((?:[^"\\]|\\.)*)"\s*\}'
    )
    by_page = {}
    for em in entry_re.finditer(lm.group(1)):
        e = {"t": em.group(1), "k": em.group(2), "p": em.group(3),
             "aka": em.group(4), "d": em.group(5)}
        by_page.setdefault(e["p"], []).append(e)
    for i, pid in enumerate(ids):
        ents = by_page.get(pid)
        f = chapter_file(i)
        if not f.exists():
            continue
        txt = f.read_text(encoding="utf-8")
        if pid in ("lexicon", "notes"):
            txt = "<!-- STRUCTURE-ONLY -->\n" + txt
        if pid == "home":
            txt = "<!-- NO-SOURCES -->\n<!-- NO-FIG -->\n" + txt
        if ents:
            txt = txt.replace(
                "\n", "\n<!-- LEX: " + json.dumps(ents, ensure_ascii=False) + " -->\n", 1
            )
        f.write_text(txt, encoding="utf-8")

    # 3) lexicon 문을 마커로 감쌈
    html = (
        html[: lm.start()]
        + "// LEXICON:BEGIN\n"
        + html[lm.start() : lm.end()]
        + "\n    // LEXICON:END"
        + html[lm.end() :]
    )
    INDEX.write_text(html, encoding="utf-8")
    print(f"파셜 {sum(1 for i in range(len(ids)) if chapter_file(i).exists())}개 생성, "
          f"색인 {sum(len(v) for v in by_page.values())}개 이주 완료")


def check(filter_ids=None):
    src = read_index()
    built = build(src)
    ids = page_ids(built)
    errors, warns = [], []

    if built != src:
        warns.append("index.html이 파셜보다 오래됨 — build.py 실행 필요")

    # nav ↔ section
    for pid in ids:
        if f'id="page-{pid}"' not in built:
            errors.append(f"섹션 없음: {pid}")
    for m in re.finditer(r'data-page="(\w+)"', built):
        if m.group(1) not in ids:
            errors.append(f"nav 대상 없는 페이지: {m.group(1)}")

    # 페이지 해시 링크
    for m in re.finditer(r'href="#([\w-]+)"', built):
        if m.group(1) not in ids:
            errors.append(f'유효하지 않은 페이지 링크: #{m.group(1)} '
                          f'(챕터 내부 링크는 data-scroll을 쓸 것)')

    # id 중복
    allids = re.findall(r'id="([^"]+)"', built)
    dupes = sorted({x for x in allids if allids.count(x) > 1})
    if dupes:
        errors.append(f"중복 id: {', '.join(dupes)}")

    # 챕터별 검사
    for i, pid in enumerate(ids):
        if filter_ids and pid not in filter_ids:
            continue
        m = re.search(SEC_RE % pid, built, re.S)
        if not m:
            continue
        sec = m.group(1)
        inner = load_partial(i)
        if inner is None:
            errors.append(f"{pid}: chapters/ch{i:02d}.html 없음")
            continue
        fl = flags(inner)

        # 섹션 내부 data-scroll 대상
        for sm in re.finditer(r'data-scroll="([^"]+)"', sec):
            if f'id="{sm.group(1)}"' not in sec:
                errors.append(f"{pid}: data-scroll 대상 없음 — {sm.group(1)}")

        if "STRUCTURE-ONLY" in fl:
            continue

        for cls in REQUIRED_CLASSES:
            if cls == "sources" and "NO-SOURCES" in fl:
                continue
            if cls not in sec:
                errors.append(f"{pid}: .{cls} 블록 없음")

        # figure.fig + figcaption + 출처 표기 (atlas의 장식 figure는 제외)
        figs = re.findall(r'<figure class="fig".*?</figure>', sec, re.S)
        if not figs and "NO-FIG" not in fl:
            errors.append(f"{pid}: figure.fig 이미지 없음")
        for fg in figs:
            if "<figcaption" not in fg:
                errors.append(f"{pid}: figure에 figcaption 없음")
            elif not ATTR_RE.search(fg):
                warns.append(f"{pid}: 캡션에 출처 표기 없음")

        for im in re.finditer(r'<img[^>]+src="([^"]+)"', sec):
            srcp = im.group(1)
            if srcp.startswith(("http", "data:")):
                warns.append(f"{pid}: 외부/인라인 이미지 — 로컬 저장 권장 {srcp[:60]}")
            elif not (ROOT / srcp).exists():
                errors.append(f"{pid}: 이미지 파일 없음 — {srcp}")

        # 길이
        n = text_len(sec)
        if n < LEN_HARD_MIN:
            errors.append(f"{pid}: 본문 {n}자 — 너무 짧음 (목표 5000~8000)")
        elif n > LEN_HARD_MAX:
            errors.append(f"{pid}: 본문 {n}자 — 너무 김 (목표 5000~8000)")
        elif not (LEN_SOFT_MIN <= n <= LEN_SOFT_MAX):
            warns.append(f"{pid}: 본문 {n}자 — 목표 5000~8000에서 벗어남")

    # LEX 수집 검증
    lex_terms = set()
    for i, pid in enumerate(ids):
        inner = load_partial(i)
        if inner:
            for e in lex_entries(inner):
                if e["t"] in lex_terms:
                    warns.append(f"색인 중복 무시됨: {e['t']} ({pid})")
                lex_terms.add(e["t"])
    lm = re.search(r"const lexicon = \[(.*?)\];", built, re.S)
    if lm and f'"t"' not in lm.group(1) and not lex_terms:
        warns.append("색인이 비어 있음")

    print("== 검증 결과 ==")
    for e in errors:
        print("ERROR", e)
    for w in warns:
        print("warn ", w)
    if not errors and not warns:
        print("모든 검사 통과")
    print(f"-- errors {len(errors)} / warnings {len(warns)}")
    return 1 if errors else 0


def stats():
    src = read_index()
    built = build(src)
    ids = page_ids(built)
    for i, pid in enumerate(ids):
        m = re.search(SEC_RE % pid, built, re.S)
        inner = load_partial(i) or ""
        fl = flags(inner)
        n = text_len(m.group(1)) if m else 0
        tag = " [구조 유지]" if "STRUCTURE-ONLY" in fl else ""
        print(f"ch{i:02d} {pid:<12} {n:>6}자{tag}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--init" in args:
        init()
    elif "--stats" in args:
        stats()
    elif "--check" in args:
        filt = [a for a in args if not a.startswith("--")] or None
        sys.exit(check(filt))
    else:
        INDEX.write_text(build(read_index()), encoding="utf-8")
        print("index.html 재생성 완료")

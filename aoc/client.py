from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

from .config import (
    AOC_YEAR,
    INPUTS_DIR,
    QUESTIONS_DIR,
    get_session_cookie,
    get_user_agent,
)

AOC_BASE_URL = "https://adventofcode.com"


@dataclass
class FetchResult:
    year: int
    day: int
    input_path: str
    example_paths: List[str]
    question_text_path: Optional[str]
    question_html_path: Optional[str]


def _make_session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": get_user_agent()})
    s.cookies.set("session", get_session_cookie(), domain="adventofcode.com")
    return s


def fetch_input(day: int, year: int | None = None) -> str:
    if year is None:
        year = AOC_YEAR
    url = f"{AOC_BASE_URL}/{year}/day/{day}/input"
    with _make_session() as s:
        resp = s.get(url)
        if resp.status_code != 200:
            raise RuntimeError(
                f"Failed to fetch input for {year}-day{day}: HTTP {resp.status_code}"
            )
        return resp.text.rstrip("\n") + "\n"


def fetch_puzzle_html(day: int, year: int | None = None) -> str:
    if year is None:
        year = AOC_YEAR
    url = f"{AOC_BASE_URL}/{year}/day/{day}"
    with _make_session() as s:
        resp = s.get(url)
        if resp.status_code != 200:
            raise RuntimeError(
                f"Failed to fetch puzzle page for {year}-day{day}: HTTP {resp.status_code}"
            )
        return resp.text

def html_fragment_to_markdown(fragment_html: str) -> str:
    """Convert AoC puzzle HTML into nicer Markdown.

    Prefer markdownify if available, fall back to html2text, then to plain text.
    """
    # First try markdownify
    try:
        import markdownify
    except ImportError:
        markdownify = None

    if markdownify is not None:
        md = markdownify.markdownify(
            fragment_html,
            heading_style="ATX",  # ### headings
        )
        return md.strip() + "\n"

    # Then try html2text
    try:
        import html2text  # type: ignore[import-not-found]
    except ImportError:
        html2text = None

    if html2text is not None:
        h = html2text.HTML2Text()
        h.body_width = 0          # don’t wrap lines
        h.ignore_links = False    # keep links
        h.ignore_images = True
        md = h.handle(fragment_html)
        return md.strip() + "\n"

    # Fallback: current behavior (plain text)
    soup = BeautifulSoup(fragment_html, "html.parser")
    text = soup.get_text("\n")
    return text.strip() + "\n"


def extract_examples_from_html(html: str) -> list[str]:
    """All <pre><code> blocks (some may be code, some example inputs)."""
    soup = BeautifulSoup(html, "html.parser")
    examples: list[str] = []
    for pre in soup.find_all("pre"):
        code = pre.code
        text = (code or pre).get_text("\n")
        cleaned = text.strip("\n")
        if cleaned:
            examples.append(cleaned + "\n")
    return examples


def extract_puzzle_markdown(html: str) -> str:
    """Return the puzzle description(s) as Markdown.

    - Includes part 1 (and part 2 once unlocked).
    - Uses html_fragment_to_markdown for nicer formatting.
    """
    soup = BeautifulSoup(html, "html.parser")
    articles = soup.find_all("article", class_="day-desc")
    if not articles:
        return ""

    fragments: list[str] = []
    for article in articles:
        # Convert each article separately so part 1 / part 2 are clearly separated
        fragments.append(html_fragment_to_markdown(str(article)))

    # Separate part 1 and part 2 with a horizontal rule
    return ("\n\n---\n\n".join(fragments)).rstrip() + "\n"


def save_day_data(
    day: int,
    *,
    year: int | None = None,
    overwrite: bool = False,
) -> FetchResult:
    """Fetch input, puzzle HTML, examples, and store them for this day.

    Paths are day-based only (no year folders), assuming one year per repo.
    """
    if year is None:
        year = AOC_YEAR

    day_folder = INPUTS_DIR / f"day{day:02d}"
    day_folder.mkdir(parents=True, exist_ok=True)

    # Input
    input_path = day_folder / "input.txt"
    if overwrite or not input_path.exists():
        text = fetch_input(day, year)
        input_path.write_text(text, encoding="utf-8")

    # Puzzle HTML + question text
    QUESTIONS_DIR.mkdir(parents=True, exist_ok=True)
    q_text_path = QUESTIONS_DIR / f"day{day:02d}.md"
    q_html_path = QUESTIONS_DIR / f"day{day:02d}.html"

    html = fetch_puzzle_html(day, year)

    QUESTIONS_DIR.mkdir(parents=True, exist_ok=True)
    q_text_path = QUESTIONS_DIR / f"day{day:02d}.md"
    q_html_path = QUESTIONS_DIR / f"day{day:02d}.html"

    # Always store the raw HTML (so you can re-run the conversion if wanted)
    if overwrite or not q_html_path.exists():
        q_html_path.write_text(html, encoding="utf-8")

    # Markdown conversion
    puzzle_md = extract_puzzle_markdown(html)
    if puzzle_md and (overwrite or not q_text_path.exists()):
        q_text_path.write_text(puzzle_md, encoding="utf-8")
        q_text_str: str | None = str(q_text_path)
    else:
        q_text_str = None

    # Examples
    examples = extract_examples_from_html(html)
    example_paths: list[str] = []
    for idx, example in enumerate(examples, start=1):
        ex_path = day_folder / f"example{idx}.txt"
        if overwrite or not ex_path.exists():
            ex_path.write_text(example, encoding="utf-8")
        example_paths.append(str(ex_path))

    return FetchResult(
        year=year,
        day=day,
        input_path=str(input_path),
        example_paths=example_paths,
        question_text_path=q_text_str,
        question_html_path=str(q_html_path),
    )

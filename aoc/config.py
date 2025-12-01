from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parents[1]
INPUTS_DIR = ROOT / "inputs"
QUESTIONS_DIR = ROOT / "questions"

# One year per repo. Set this in .env.
AOC_YEAR = int(os.getenv("AOC_YEAR", "2023"))


def get_session_cookie() -> str:
    token = os.getenv("AOC_SESSION")
    if not token:
        raise RuntimeError(
            "AOC_SESSION is not set. Put your Advent of Code 'session' cookie "
            "into a .env file or environment variable named AOC_SESSION."
        )
    return token.strip()


def get_user_agent() -> str:
    return os.getenv(
        "AOC_USER_AGENT",
        "github.com/yourname/aoc-python (Advent of Code helper script)",
    )

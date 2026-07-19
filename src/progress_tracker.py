"""
문제별 회독 수(복습 횟수)를 로컬 JSON 파일에 기록/조회하는 모듈.

문제마다 '과목_챕터_질문' 조합으로 고유 키를 만들어 회독 수를 누적 저장한다.
"""

import json
import os

PROGRESS_FILE = "progress.json"


def load_progress(path: str = PROGRESS_FILE) -> dict:
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_progress(progress_data: dict, path: str = PROGRESS_FILE) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(progress_data, f, ensure_ascii=False, indent=4)


def make_key(subject: str, chapter: str, question: str) -> str:
    return f"{subject}_{chapter}_{question}"


def increment(progress_data: dict, key: str) -> dict:
    progress_data[key] = progress_data.get(key, 0) + 1
    return progress_data

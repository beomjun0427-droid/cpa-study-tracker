"""
엑셀(data.xlsx) 기반 문제 데이터를 불러오고 전처리하는 모듈.

- 시트별(과목별)로 분리된 엑셀 데이터를 하나의 DataFrame으로 병합
- 결측치 및 줄바꿈 문자를 Streamlit(Markdown) 렌더링에 맞게 정리
"""

import pandas as pd
import streamlit as st


REQUIRED_COLUMNS = ["과목", "챕터", "질문", "정답"]


@st.cache_data
def load_data(path: str = "data.xlsx") -> pd.DataFrame:
    """엑셀 파일의 모든 시트를 하나의 DataFrame으로 병합해서 반환한다.

    시트 이름이 곧 과목명이라는 전제 하에, '과목' 컬럼이 없는 시트는
    시트 이름을 과목명으로 채워 넣는다.
    """
    try:
        excel_data = pd.read_excel(path, sheet_name=None)
    except FileNotFoundError:
        st.error(f"'{path}' 파일을 찾을 수 없습니다. 파일을 먼저 준비해 주세요.")
        return pd.DataFrame(columns=REQUIRED_COLUMNS)

    df_list = []
    for sheet_name, sheet_df in excel_data.items():
        if "과목" not in sheet_df.columns:
            sheet_df["과목"] = sheet_name
        df_list.append(sheet_df)

    final_df = pd.concat(df_list, ignore_index=True)
    final_df = final_df.dropna(subset=["질문"])

    # 엑셀 상 빈칸으로 인한 NaN을 빈 문자열로 치환
    final_df = final_df.fillna("")

    # 엑셀 줄바꿈('\n')을 마크다운 줄바꿈('  \n')으로 치환해 Streamlit에서 올바르게 렌더링
    final_df = final_df.replace("\n", "  \n", regex=True)

    return final_df


def get_subjects(df: pd.DataFrame) -> list[str]:
    return df["과목"].dropna().unique().tolist()


def get_chapters(df: pd.DataFrame, subject: str) -> list[str]:
    subject_df = df[df["과목"] == subject]
    chapters = subject_df["챕터"].dropna().unique().tolist()
    chapters.insert(0, "전체 챕터")
    return chapters


def filter_questions(df: pd.DataFrame, subject: str, chapter: str) -> pd.DataFrame:
    subject_df = df[df["과목"] == subject]
    if chapter != "전체 챕터":
        return subject_df[subject_df["챕터"] == chapter]
    return subject_df

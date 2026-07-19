import random

import streamlit as st

from src.data_loader import load_data, get_subjects, get_chapters, filter_questions
from src.progress_tracker import load_progress, save_progress, make_key, increment


def render_browse_mode(subject_df, selected_subject, selected_chapter):
    st.subheader(f"[{selected_subject}] {selected_chapter} - 전체 보기")

    progress = load_progress()

    for _, row in subject_df.iterrows():
        q_key = make_key(selected_subject, selected_chapter, row["질문"])
        read_count = progress.get(q_key, 0)

        with st.expander(f"Q. {row['질문']} (현재 {read_count}회독)"):
            st.write(f"**A.** {row['정답']}")

            if st.button("✅ 읽음 완료 (+1)", key=f"btn_{q_key}"):
                progress = increment(progress, q_key)
                save_progress(progress)
                st.rerun()


def render_quiz_mode(subject_df, selected_subject, selected_chapter):
    st.subheader(f"[{selected_subject}] {selected_chapter} - 퀴즈 모드")

    if len(subject_df) == 0:
        st.warning("해당 조건에 저장된 문제가 없습니다.")
        return

    if "quiz_index" not in st.session_state:
        st.session_state.quiz_index = random.randint(0, len(subject_df) - 1)
    if "show_answer" not in st.session_state:
        st.session_state.show_answer = False

    current_q = subject_df.iloc[st.session_state.quiz_index]

    st.info(f"**질문:** {current_q['질문']}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("정답 확인 🔍"):
            st.session_state.show_answer = True
            st.rerun()
    with col2:
        if st.button("다음 문제 ⏭️"):
            st.session_state.quiz_index = random.randint(0, len(subject_df) - 1)
            st.session_state.show_answer = False
            st.rerun()

    if st.session_state.show_answer:
        st.success(f"**정답:** {current_q['정답']}")


def main():
    st.set_page_config(page_title="회계사 시험 대비 앱", page_icon="📚")
    st.title("📚 회계사 시험 대비 암기장 & 퀴즈")

    df = load_data()
    if df.empty:
        return

    st.sidebar.header("⚙️ 학습 설정")

    if "과목" not in df.columns:
        st.error("데이터에 '과목' 정보가 없습니다. 엑셀 형식을 확인해 주세요.")
        return

    selected_subject = st.sidebar.selectbox("과목 선택", get_subjects(df))
    selected_chapter = st.sidebar.selectbox("챕터 선택", get_chapters(df, selected_subject))

    filtered_df = filter_questions(df, selected_subject, selected_chapter)

    mode = st.sidebar.radio("학습 모드", ["📖 챕터별 열람", "🧠 랜덤 퀴즈"])
    st.divider()

    if mode == "📖 챕터별 열람":
        render_browse_mode(filtered_df, selected_subject, selected_chapter)
    elif mode == "🧠 랜덤 퀴즈":
        render_quiz_mode(filtered_df, selected_subject, selected_chapter)


if __name__ == "__main__":
    main()

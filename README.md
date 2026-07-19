# 📚 CPA Study Tracker
🔗 **[Live Demo 바로가기](https://cpa-study-tracke-z7f856v6dz2hjqlhckpevx.streamlit.app/)**

CPA 2차 시험(재무회계·세법·원가) 준비 과정에서 자투리 시간을 학습 시간으로 바꾸기 위해 만든 Streamlit 기반 암기장 & 퀴즈 앱입니다.

## Problem

CPA 시험을 준비하면서 학업과 병행하다 보니, 왕복 통근 시간만 하루 약 2시간이 그냥 버려지고 있었습니다. 기존에 쓰던 종이 암기장이나 워드 파일 정리 방식은 이동 중에 꺼내 보기 불편했고, 어떤 문제를 몇 번 봤는지 스스로 추적하기도 어려웠습니다.

## Solution

- 재무회계·세법·원가 세 과목의 질문-정답 데이터를 엑셀로 관리하고, 앱이 이를 불러와 과목·챕터별로 탐색할 수 있게 구성했습니다.
- **챕터별 열람 모드**: 특정 챕터의 문제를 전체 훑어보며, 문제마다 개별 회독 수를 누적 기록합니다.
- **랜덤 퀴즈 모드**: 선택한 범위 내에서 무작위로 문제를 출제해 실전처럼 연습할 수 있게 했습니다.
- 스마트폰에서도 바로 접속해 쓸 수 있도록 Streamlit으로 배포해, 통근 중 자투리 시간에 활용했습니다.

## Technical Decisions

- **데이터 소스로 엑셀을 선택한 이유**: 시험 준비 중에는 문제를 새로 추가하거나 수정하는 빈도가 잦았는데, 매번 코드를 건드리지 않고 엑셀만 수정하면 바로 반영되도록 데이터와 로직을 분리했습니다.
- **문제별 고유 키 설계**: 회독 수를 문제 단위로 추적하기 위해 `과목_챕터_질문` 조합을 키로 사용했습니다. 별도의 문제 ID 체계 없이도 중복 없는 식별자를 만들 수 있는 실용적인 방법이었습니다.
- **모듈 분리**: 초기 버전은 데이터 로딩, 진도 관리, UI 로직이 한 파일(`app.py`)에 섞여 있었습니다. 이후 `src/data_loader.py`(데이터 전처리), `src/progress_tracker.py`(진도 기록)로 책임을 분리해, 데이터 형식이 바뀌거나 저장 방식을 교체(예: 로컬 JSON → DB)해야 할 때 UI 코드를 건드리지 않도록 구조를 정리했습니다.
- **Gemini API 활용**: 초기 프로토타이핑 단계에서 Gemini의 도움을 받아 Streamlit 세션 상태(session_state) 관리 로직을 빠르게 검증하고 반복했습니다.

## Impact

이 도구를 실제로 활용하며 CPA 2차 재무회계·재무관리·회계감사 과목에 합격했습니다. 이동 시간을 학습 시간으로 전환한 것이 실질적인 효과가 있었습니다.

## Tech Stack

`Python` · `Streamlit` · `Pandas` · `Gemini API`

## Project Structure

```
cpa-study-tracker/
├── app.py                    # Streamlit 진입점 및 UI 로직
├── src/
│   ├── data_loader.py        # 엑셀 데이터 로딩 및 전처리
│   └── progress_tracker.py   # 회독 수 기록/조회
├── data.xlsx                 # 과목별(회계/세법/원가) 질문-정답 데이터
└── requirements.txt
```

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Screenshots

### 챕터별 열람 모드
![챕터별 열람 화면](screenshots/browse_mode.png)

### 랜덤 퀴즈 모드
![랜덤 퀴즈 화면](screenshots/quiz_mode.png)

## Future Improvements

- 로컬 JSON 대신 클라우드 DB와 연동해 여러 기기 간 회독 기록을 동기화
- 오답 노트 기능 추가 (틀린 문제만 모아 다시 출제)
- 회독 수 기반 우선순위 출제 (적게 본 문제를 더 자주 노출)

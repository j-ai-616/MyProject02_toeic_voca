import streamlit as st
import pandas as pd
import random
from pathlib import Path

# --------------------------------------------------
# 기본 설정
# --------------------------------------------------
st.set_page_config(
    page_title="TOEIC VOCA 학습 앱",
    page_icon="📘",
    layout="wide"
)

FILE_PATH = Path(__file__).parent / "toeic_voca.xlsx"

# --------------------------------------------------
# CSS 스타일
# --------------------------------------------------
st.markdown("""
<style>
    .main {
        background: linear-gradient(180deg, #f8fbff 0%, #eef5ff 100%);
    }

    .block-container {
        padding-top: 3.2rem;
        padding-bottom: 2rem;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #163a6b 0%, #244f8f 100%);
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    .app-title {
        background: linear-gradient(135deg, #1f4e79, #3b82f6);
        padding: 28px;
        border-radius: 20px;
        color: white;
        box-shadow: 0 10px 25px rgba(31, 78, 121, 0.18);
        margin-bottom: 20px;
    }

    .app-title h1 {
        margin: 0;
        font-size: 2.1rem;
    }

    .app-title p {
        margin: 8px 0 0 0;
        font-size: 1.02rem;
        opacity: 0.95;
    }

    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 18px;
        border: 1px solid #dfe8f5;
        box-shadow: 0 6px 18px rgba(0,0,0,0.06);
        text-align: center;
    }

    .metric-label {
        font-size: 0.95rem;
        color: #5b6b7f;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #183b66;
    }

    .section-card {
        background: white;
        border-radius: 18px;
        padding: 24px;
        border: 1px solid #e4edf7;
        box-shadow: 0 6px 20px rgba(0,0,0,0.05);
        margin-bottom: 18px;
    }

    .word-card {
        background: linear-gradient(135deg, #ffffff, #f4f8ff);
        border: 1px solid #dbe7f5;
        border-radius: 24px;
        padding: 38px 28px;
        text-align: center;
        box-shadow: 0 12px 28px rgba(37, 99, 235, 0.08);
        margin: 16px 0 24px 0;
    }

    .day-badge {
        display: inline-block;
        background: #e8f1ff;
        color: #1d4f91;
        padding: 6px 14px;
        border-radius: 999px;
        font-size: 0.92rem;
        font-weight: 600;
        margin-bottom: 14px;
    }

    .word-title {
        font-size: 2.4rem;
        font-weight: 800;
        color: #183b66;
        margin-bottom: 12px;
    }

    .word-meaning {
        font-size: 1.15rem;
        color: #425466;
        line-height: 1.7;
    }

    .quiz-card {
        background: white;
        border-radius: 22px;
        padding: 28px;
        border: 1px solid #dfe8f5;
        box-shadow: 0 10px 24px rgba(0,0,0,0.05);
        margin-top: 12px;
    }
    
    .quiz-word-box {
        background: white;
        border: 1px solid #dfe8f5;
        border-radius: 22px;
        padding: 28px;
        box-shadow: 0 10px 24px rgba(0,0,0,0.05);
        margin-top: 12px;
        margin-bottom: 16px;
    }

    .quiz-word {
        font-size: 2rem;
        font-weight: 800;
        color: #173a67;
        margin-bottom: 10px;
    }

    .subtle-text {
        color: #64748b;
        font-size: 0.95rem;
    }

    .highlight-box {
        background: linear-gradient(135deg, #eff6ff, #f8fbff);
        border-left: 6px solid #3b82f6;
        padding: 18px;
        border-radius: 14px;
        color: #274060;
        margin-bottom: 18px;
    }

    .wrong-card {
        background: #fffaf5;
        border: 1px solid #fde7c7;
        border-radius: 18px;
        padding: 18px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.04);
    }

    .footer-note {
        text-align: center;
        color: #6b7280;
        font-size: 0.92rem;
        margin-top: 20px;
    }

    div[data-testid="stButton"] > button {
        border-radius: 12px;
        border: none;
        padding: 0.65rem 1rem;
        font-weight: 700;
    }

    div[data-testid="stDownloadButton"] > button {
        border-radius: 12px;
        font-weight: 700;
    }

    div[data-testid="stDataFrame"] {
        border-radius: 16px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 데이터 불러오기
# --------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_excel(FILE_PATH, sheet_name="Sheet1")
    df = df.dropna(subset=["Day", "단어", "뜻"]).copy()

    df["Day"] = df["Day"].astype(str).str.strip()
    df["단어"] = df["단어"].astype(str).str.strip()
    df["뜻"] = df["뜻"].astype(str).str.strip()

    df["day_num"] = df["Day"].str.extract(r"(\d+)").astype(int)
    df = df.sort_values(["day_num", "단어"]).reset_index(drop=True)
    return df

df = load_data()

# --------------------------------------------------
# 세션 상태 초기화
# --------------------------------------------------
if "show_meaning" not in st.session_state:
    st.session_state.show_meaning = False

if "random_word" not in st.session_state:
    st.session_state.random_word = None

if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = []

if "quiz_index" not in st.session_state:
    st.session_state.quiz_index = 0

if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0

if "quiz_answered" not in st.session_state:
    st.session_state.quiz_answered = False

if "quiz_selected" not in st.session_state:
    st.session_state.quiz_selected = None

if "wrong_answers" not in st.session_state:
    st.session_state.wrong_answers = []

if "study_index" not in st.session_state:
    st.session_state.study_index = 0

if "last_selected_day" not in st.session_state:
    st.session_state.last_selected_day = None

# --------------------------------------------------
# 공통 함수
# --------------------------------------------------
all_days = sorted(df["Day"].unique(), key=lambda x: int("".join(filter(str.isdigit, x))))

def reset_quiz():
    st.session_state.quiz_questions = []
    st.session_state.quiz_index = 0
    st.session_state.quiz_score = 0
    st.session_state.quiz_answered = False
    st.session_state.quiz_selected = None

def make_quiz_questions(source_df, quiz_count=10):
    usable_df = source_df.drop_duplicates(subset=["단어"]).copy()

    if len(usable_df) < 4:
        return []

    quiz_count = min(quiz_count, len(usable_df))
    sampled = usable_df.sample(n=quiz_count, random_state=None).to_dict("records")

    questions = []
    all_meanings = usable_df["뜻"].tolist()

    for row in sampled:
        correct_word = row["단어"]
        correct_meaning = row["뜻"]

        wrong_pool = [m for m in all_meanings if m != correct_meaning]
        wrong_choices = random.sample(wrong_pool, 3)
        choices = wrong_choices + [correct_meaning]
        random.shuffle(choices)

        questions.append({
            "word": correct_word,
            "answer": correct_meaning,
            "choices": choices
        })

    return questions

def add_wrong_answer(day, word, meaning):
    item = {"Day": day, "단어": word, "뜻": meaning}
    if item not in st.session_state.wrong_answers:
        st.session_state.wrong_answers.append(item)

def render_header(title, subtitle):
    st.markdown(
        f"""
        <div class="app-title">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# --------------------------------------------------
# 사이드바
# --------------------------------------------------
st.sidebar.markdown("## 📚 TOEIC VOCA")
st.sidebar.markdown("Day별 학습 · 랜덤 복습 · 퀴즈 · 오답노트")

menu = st.sidebar.radio(
    "메뉴 선택",
    ["Home", "Day Study", "Vocab List", "Random Word", "Quiz", "Wrong Answers"]
)

st.sidebar.markdown("---")
st.sidebar.info("매일 조금씩 반복하면 오래 기억되고, 내 것이 됩니다.")

# --------------------------------------------------
# HOME
# --------------------------------------------------
if menu == "Home":
    render_header("📘 TOEIC VOCA 학습 앱", "Day별 암기부터 퀴즈 복습까지 한 번에 정리하는 단어 학습 앱")

    total_words = len(df)
    total_days = df["Day"].nunique()
    wrong_count = len(st.session_state.wrong_answers)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">전체 단어 수</div>
            <div class="metric-value">{total_words}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">전체 Day 수</div>
            <div class="metric-value">{total_days}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">오답노트</div>
            <div class="metric-value">{wrong_count}</div>
        </div>
        """, unsafe_allow_html=True)


    left, right = st.columns([1.2, 1])

    with left:
        st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)
        st.subheader("📊 Day별 단어 수")
        day_counts = (
            df.groupby("Day")["단어"]
            .count()
            .reset_index(name="단어 수")
            .assign(day_num=lambda x: x["Day"].str.extract(r"(\d+)").astype(int))
            .sort_values("day_num")
        )
        st.bar_chart(day_counts.set_index("Day")["단어 수"])

    with right:
        st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)
        st.subheader("🚀 바로 시작")
        selected_day_home = st.selectbox("학습할 Day 선택", all_days, index=0, key="home_day")
        st.success(f"오늘은 **{selected_day_home}** 학습을 시작해보세요.")

        if st.button("🎲 오늘의 랜덤 단어 뽑기", use_container_width=True):
            row = df.sample(1).iloc[0]
            st.session_state.random_word = row.to_dict()
            st.success(f"오늘의 랜덤 단어는 **{row['단어']}** 입니다.")

        st.markdown("""
        <div class="highlight-box">
        추천 학습 순서: <b>Day Study → Quiz → Wrong Answers → Random Word</b><br>
        먼저 외우고, 바로 확인하고, 틀린 것만 다시 보는 흐름이 가장 효율적입니다..
        </div>
        """, unsafe_allow_html=True)

# --------------------------------------------------
# DAY STUDY
# --------------------------------------------------
elif menu == "Day Study":
    render_header("📝 Day별 단어 학습", "하루치 단어를 차례대로 보고 뜻을 확인하면서 반복 학습해보세요.")

    selected_day = st.selectbox("Day 선택", all_days, index=0, key="study_day")

    if st.session_state.last_selected_day != selected_day:
        st.session_state.study_index = 0
        st.session_state.show_meaning = False
        st.session_state.last_selected_day = selected_day

    day_df = df[df["Day"] == selected_day].reset_index(drop=True)

    if len(day_df) == 0:
        st.warning("해당 Day 데이터가 없습니다.")
    else:
        if st.session_state.study_index >= len(day_df):
            st.session_state.study_index = 0

        st.markdown(f"""
        <div class="highlight-box">
            현재 <b>{selected_day}</b> 학습 중 · 총 <b>{len(day_df)}개</b> 단어
        </div>
        """, unsafe_allow_html=True)

        col_a, col_b, col_c = st.columns([1, 1, 1])

        with col_a:
            if st.button("⬅ 이전 단어", use_container_width=True):
                st.session_state.study_index = (st.session_state.study_index - 1) % len(day_df)

        with col_b:
            if st.button("👁 뜻 보기 / 가리기", use_container_width=True):
                st.session_state.show_meaning = not st.session_state.show_meaning

        with col_c:
            if st.button("다음 단어 ➡", use_container_width=True):
                st.session_state.study_index = (st.session_state.study_index + 1) % len(day_df)

        current = day_df.iloc[st.session_state.study_index]

        meaning_text = f"뜻: {current['뜻']}" if st.session_state.show_meaning else "뜻을 먼저 떠올려보세요."

        st.markdown(
            f"""
            <div class="word-card">
                <div class="day-badge">{selected_day} · {st.session_state.study_index + 1} / {len(day_df)}</div>
                <div class="word-title">{current['단어']}</div>
                <div class="word-meaning">{meaning_text}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.expander("전체 단어 목록 보기"):
            st.dataframe(day_df[["단어", "뜻"]], use_container_width=True, hide_index=True)

# --------------------------------------------------
# VOCAB LIST
# --------------------------------------------------
elif menu == "Vocab List":
    render_header("📚 전체 단어장", "Day별 필터와 검색 기능으로 단어를 빠르게 찾아보세요.")

    filter_col1, filter_col2 = st.columns([1, 2])

    with filter_col1:
        day_filter = st.selectbox("Day 필터", ["전체"] + all_days)

    with filter_col2:
        keyword = st.text_input("검색어 입력 (단어 / 뜻)", placeholder="예: resume, 계약, 감소 ...")

    filtered_df = df.copy()

    if day_filter != "전체":
        filtered_df = filtered_df[filtered_df["Day"] == day_filter]

    if keyword.strip():
        filtered_df = filtered_df[
            filtered_df["단어"].str.contains(keyword, case=False, na=False) |
            filtered_df["뜻"].str.contains(keyword, case=False, na=False)
        ]

    st.markdown(f"""
    <div class="highlight-box">
        검색 결과 <b>{len(filtered_df)}개</b>
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(
        filtered_df[["Day", "단어", "뜻"]],
        use_container_width=True,
        hide_index=True
    )

# --------------------------------------------------
# RANDOM WORD
# --------------------------------------------------
elif menu == "Random Word":
    render_header("🎲 랜덤 단어 학습", "범위를 정해서 랜덤으로 단어를 뽑고 바로 복습해보세요.")

    random_day_option = st.selectbox("범위 선택", ["전체"] + all_days)

    if st.button("🎯 랜덤 단어 뽑기", use_container_width=True):
        pool = df if random_day_option == "전체" else df[df["Day"] == random_day_option]

        if len(pool) > 0:
            st.session_state.random_word = pool.sample(1).iloc[0].to_dict()
            st.session_state.show_meaning = False

    if st.session_state.random_word:
        word_data = st.session_state.random_word
        meaning_text = f"뜻: {word_data['뜻']}" if st.session_state.show_meaning else "뜻을 생각한 뒤 버튼을 눌러 확인해보세요."

        st.markdown(
            f"""
            <div class="word-card">
                <div class="day-badge">{word_data['Day']}</div>
                <div class="word-title">{word_data['단어']}</div>
                <div class="word-meaning">{meaning_text}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        c1, c2 = st.columns(2)

        with c1:
            if st.button("👀 뜻 보기", use_container_width=True):
                st.session_state.show_meaning = True

        with c2:
            if st.button("🔄 다른 단어", use_container_width=True):
                pool = df if random_day_option == "전체" else df[df["Day"] == random_day_option]
                st.session_state.random_word = pool.sample(1).iloc[0].to_dict()
                st.session_state.show_meaning = False
                st.rerun()

    else:
        st.info("버튼을 눌러 랜덤 단어를 시작해보세요.")

# --------------------------------------------------
# QUIZ
# --------------------------------------------------
elif menu == "Quiz":
    render_header("❓ 단어 퀴즈", "뜻을 보고 맞히며 암기 상태를 점검해보세요.")

    top1, top2 = st.columns([1, 1])

    with top1:
        quiz_day = st.selectbox("퀴즈 범위", ["전체"] + all_days)

    with top2:
        quiz_count = st.selectbox("문제 수", [5, 10, 15, 20], index=1)

    if st.button("🧠 퀴즈 시작", use_container_width=True):
        source_df = df if quiz_day == "전체" else df[df["Day"] == quiz_day]
        reset_quiz()
        st.session_state.quiz_questions = make_quiz_questions(source_df, quiz_count)

    if st.session_state.quiz_questions:
        total_q = len(st.session_state.quiz_questions)
        idx = st.session_state.quiz_index

        if idx < total_q:
            q = st.session_state.quiz_questions[idx]

            st.progress(idx / total_q)
            st.caption(f"진행률: {idx + 1} / {total_q}")

            st.markdown(
                f"""
                <div class="quiz-word-box">
                    <div class="quiz-word">{q["word"]}</div>
                    <div class="subtle-text">이 단어의 뜻으로 가장 알맞은 것을 고르세요.</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            selected = st.radio(
                "정답 선택",
                q["choices"],
                key=f"quiz_radio_{idx}",
                label_visibility="collapsed"
            )

            b1, b2 = st.columns(2)

            with b1:
                if st.button("정답 확인", use_container_width=True):
                    if not st.session_state.quiz_answered:
                        st.session_state.quiz_selected = selected
                        st.session_state.quiz_answered = True

                        if selected == q["answer"]:
                            st.session_state.quiz_score += 1
                        else:
                            matched = df[df["단어"] == q["word"]].iloc[0]
                            add_wrong_answer(matched["Day"], matched["단어"], matched["뜻"])

            if st.session_state.quiz_answered:
                if st.session_state.quiz_selected == q["answer"]:
                    st.success("정답입니다!")
                else:
                    st.error(f"오답입니다. 정답: {q['answer']}")

                with b2:
                    if st.button("다음 문제", use_container_width=True):
                        st.session_state.quiz_index += 1
                        st.session_state.quiz_answered = False
                        st.session_state.quiz_selected = None
                        st.rerun()

        else:
            score = st.session_state.quiz_score
            st.markdown(f"""
            <div class="section-card" style="text-align:center;">
                <h2>퀴즈 종료</h2>
                <p style="font-size:1.2rem;">최종 점수</p>
                <p style="font-size:2.4rem; font-weight:800; color:#1d4f91;">{score} / {total_q}</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button("다시 시작", use_container_width=True):
                reset_quiz()
                st.rerun()
                
# --------------------------------------------------
# WRONG ANSWERS
# --------------------------------------------------
elif menu == "Wrong Answers":
    render_header("📌 오답노트", "퀴즈에서 틀린 단어를 다시 확인하고 집중 복습해보세요.")

    wrong_list = st.session_state.wrong_answers

    if not wrong_list:
        st.info("아직 오답노트가 비어 있습니다.")
    else:
        wrong_df = pd.DataFrame(wrong_list).drop_duplicates().reset_index(drop=True)

        st.markdown(f"""
        <div class="highlight-box">
            현재 오답 단어는 <b>{len(wrong_df)}개</b> 입니다.
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="wrong-card">', unsafe_allow_html=True)
        st.dataframe(
            wrong_df[["Day", "단어", "뜻"]],
            use_container_width=True,
            hide_index=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("🗑 오답노트 비우기", use_container_width=True):
            st.session_state.wrong_answers = []
            st.success("오답노트를 비웠습니다.")
            st.rerun()

st.markdown('<div class="footer-note">Made by Jieun Son · TOEIC VOCA Study App</div>', unsafe_allow_html=True)
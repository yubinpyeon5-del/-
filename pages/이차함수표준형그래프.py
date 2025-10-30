# app.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 페이지 설정
st.set_page_config(page_title="이차함수 교과서: y = a x^2", layout="wide")

# --- 사용자 설정 (배경색) ---
st.markdown("<h1 style='text-align:center'>이차함수 교과서: $y=ax^2$</h1>", unsafe_allow_html=True)
bg_color = st.color_picker("교과서 배경색을 고르세요", "#FFFFFF")

# CSS로 배경 적용 (Streamlit 구조에 따라 테스트된 방법)
st.markdown(
    f"""
    <style>
    /* 전체 배경 */
    [data-testid="stAppViewContainer"] {{
        background-color: {bg_color};
    }}
    /* 본문 카드(선택사항: 투명하게 하거나 카드 색상 변경 가능) */
    .stApp .css-18e3th9 {{ background-color: rgba(255,255,255,0.0); }}
    </style>
    """,
    unsafe_allow_html=True
)

st.write("")  # 여백

# --- 그래프와 설명 영역 ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("그래프: $y = a x^2$")
    # 사용자 입력: a 값
    a = st.slider("a 값 (계수)", min_value=-5.0, max_value=5.0, value=1.0, step=0.1, format="%.1f")
    show_family = st.checkbox("여러 a 값(파라볼라 가족)도 함께 보기", value=False)

    # x 범위
    x = np.linspace(-10, 10, 400)
    fig, ax = plt.subplots(figsize=(7, 5))
    # 메인 그래프
    y = a * x**2
    ax.plot(x, y, label=f"y = {a}x²", linewidth=3)

    # 선택: 파라볼라 가족 (예: a = -4,-2,-1,0.5,1,2,4)
    if show_family:
        family_as = [-4, -2, -1, -0.5, 0.5, 1, 2, 4]
        for fa in family_as:
            if fa == a:
                continue
            ay = fa * x**2
            ax.plot(x, ay, linewidth=1, alpha=0.6, label=f"a={fa}")

    # 축, 레이블, 그리드
    ax.axhline(0, color="gray", linewidth=0.8)
    ax.axvline(0, color="gray", linewidth=0.8)
    ax.set_xlim(-10, 10)
    # y축 범위 자동 조정: 현재 a에 따라 적절히 보이도록
    ymax = max(1, abs(a) * 10**2)
    ax.set_ylim(-ymax, ymax)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(f"y = {a}x² (a = {a})")
    ax.grid(True, linestyle='--', linewidth=0.5)
    ax.legend(loc='upper right', fontsize='small')

    # concavity annotation (볼록성 주석)
    if a > 0:
        concave_text = "a > 0 이므로 아래로 볼록 (∪)"
        ax.text(0.02, 0.95, "아래로 볼록 (concave up)", transform=ax.transAxes,
                fontsize=12, verticalalignment='top', bbox=dict(boxstyle="round", fc="white", alpha=0.6))
    elif a < 0:
        concave_text = "a < 0 이므로 위로 볼록 (∩)"
        ax.text(0.02, 0.95, "위로 볼록 (concave down)", transform=ax.transAxes,
                fontsize=12, verticalalignment='top', bbox=dict(boxstyle="round", fc="white", alpha=0.6))
    else:
        concave_text = "a = 0 이면 2차항이 사라져 직선 y = 0"
        ax.text(0.02, 0.95, "a = 0 → 직선 y = 0", transform=ax.transAxes,
                fontsize=12, verticalalignment='top', bbox=dict(boxstyle="round", fc="white", alpha=0.6))

    st.pyplot(fig)

with col2:
    st.subheader("성질 요약")
    st.markdown("""
    - **함수 형태**: \(y = a x^2\)  
      - \(a > 0\) 이면 **아래로 볼록** (곡선이 위로 열림, 최소값을 가짐)  
      - \(a < 0\) 이면 **위로 볼록** (곡선이 아래로 열림, 최대값을 가짐)  
      - \(a = 0\) 이면 2차항이 없어져서 직선(상수함수) 또는 \(y=0\)이 됨  
    - **대칭축**: 항상 \(x = 0\) (y축)  
    - **정점(vertex)**: 항상 원점 \((0,0)\) (단 계수 a에 의해 오르내림 없이 위치 동일)
    """)
    st.write("---")
    st.subheader("직관적 설명")
    if a > 0:
        st.write("계수 a가 클수록(양수) 그래프가 더 '가늘어'지며, 작은 양수(예: 0.5)는 '넓게' 펼쳐집니다.")
    elif a < 0:
        st.write("음수일 때도 절댓값이 클수록 더 가늘고(급격히 증가/감소), 절댓값이 작을수록 넓게 퍼집니다.")
    else:
        st.write("a = 0 이면 2차항이 사라져 포물선이 아닌 선이 됩니다.")

st.write("---")

# --- 개념 확인 문제 (마지막 부분) ---
st.header("개념확인 문제")

st.markdown("""
**문제 1.** 다음 함수의 그래프는 위로 볼록인가요, 아래로 볼록인가요?  
> 함수: \(y = -2x^2\)  
- 답은 **'위로 볼록'** 또는 **'아래로 볼록'** (띄어쓰기 상관 없음) 형태로 입력하세요.
""")

# 정답 체크를 폼 안에 넣어 버튼으로 처리
with st.form("quiz_form"):
    user_answer = st.text_input("여기에 답을 입력하세요")
    submitted = st.form_submit_button("제출")

if submitted:
    # 정답 판정 (유연한 비교)
    ans = user_answer.strip().replace(" ", "").lower()
    # 허용되는 정답 형태들
    correct_variants = {"위로볼록", "위로", "위로볼록이다", "위로볼록입니다"}
    incorrect_variants = {"아래로볼록", "아래로", "아래로볼록이다", "아래로볼록입니다"}

    if ans in correct_variants:
        st.success("참 잘했어요")  # 정확히 요구한 문구
    elif ans in incorrect_variants:
        st.error("다시 시도해보아요")
    else:
        # 유연성: a값 음수 → 위로 볼록이 정답, 그 외 일반 안내
        # 허용하는 키워드 포함 검사
        if "위로" in ans and "볼록" in ans:
            st.success("참 잘했어요")
        elif "아래로" in ans and "볼록" in ans:
            st.error("다시 시도해보아요")
        else:
            st.info("입력을 확인해 주세요. 예: '위로 볼록' 또는 '아래로 볼록'")

st.write("")  # 여백

st.markdown("---")
st.caption("앱 제작: 이차함수 교과서 데모 — 필요하시면 문제 추가, 그래프 범위 변경, 여러 문제(자동 채점) 등으로 확장해 드릴게요.")

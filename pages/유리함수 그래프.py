# app.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- 페이지 기본 설정 ---
st.set_page_config(page_title="유리함수 교과서 — y = k/x", layout="wide")

# --- 교과서 스타일 ---
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #FEF6E4 0%, #FFFDF9 100%);
        color: #0b2a4a;
        font-family: 'Apple SD Gothic Neo', 'Malgun Gothic', '맑은 고딕', sans-serif;
    }
    .explain-box {
        background: rgba(255,255,255,0.85);
        padding: 16px;
        border-radius: 10px;
        border: 1px solid rgba(11,42,74,0.08);
        margin-bottom: 20px;
    }
    h1, h2, h3 {
        color: #1A4D7A;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- 제목 ---
st.title("📘 유리함수 교과서 — 함수:  y = k / x  (k ≠ 0)")
st.write("슬라이더로 k 값을 조절하며 그래프의 변화와 성질을 탐구해보세요.")

# --- 슬라이더 설정 ---
with st.sidebar:
    st.header("설정")
    k = st.slider("k 값 (k ≠ 0)", -10.0, 10.0, 2.0, 0.1)
    if abs(k) < 1e-9:
        k = 0.1  # 0 방지
    x_range = st.slider("x 범위 (대칭)", 5.0, 50.0, 10.0, 1.0)
    show_points = st.checkbox("대표 점 표시 (x = ±1, ±2)", value=True)
    show_table = st.checkbox("대표 값 표 보기", value=True)

# --- 개념 설명 ---
st.markdown("<div class='explain-box'>", unsafe_allow_html=True)
st.header("정의 (Definition)")
st.markdown(
    """
- **함수식**: \\(y = \\dfrac{k}{x}, \\; k \\neq 0\\)  
- **정의역 (Domain)**: \\(x\\)는 0이 될 수 없습니다. → \\(x \\neq 0\\)  
- **치역 (Range)**: \\(y\\)도 0이 될 수 없습니다. → \\(y \\neq 0\\)
"""
)

st.header("점근선 (Asymptotes)")
st.markdown(
    """
- **수직 점근선**: \\(x = 0\\) — x가 0에 가까워질수록 함수값은 무한히 커지거나 작아집니다.  
- **수평 점근선**: \\(y = 0\\) — x가 ±∞로 갈수록 y는 0에 가까워집니다.  
즉, 좌표축 두 개가 모두 점근선입니다.
"""
)

st.header("대칭 성질 (Symmetry)")
st.markdown(
    """
- **원점 대칭**: \\(f(-x) = -f(x)\\) → **홀함수**  
- **y=x, y=-x 대칭 관계**  
  - \\(y = \\dfrac{k}{x}\\)을 y=x에 대해 대칭이동하면 \\(y = \\dfrac{x}{k}\\)  
  - y=-x에 대해 대칭이동하면 \\(y = -\\dfrac{x}{k}\\)
"""
)

st.header("k 값에 따른 그래프 변화")
st.markdown(
    """
- **k > 0** → 그래프는 1사분면과 3사분면에 위치  
- **k < 0** → 그래프는 2사분면과 4사분면에 위치  
- **|k|가 커질수록** → 그래프가 좌표축에서 멀어짐  
- **|k|가 작을수록** → 그래프가 좌표축에 가까워짐
"""
)
st.markdown("</div>", unsafe_allow_html=True)

# --- 그래프 데이터 생성 ---
x_min, x_max = -x_range, x_range
x_left = np.linspace(x_min, -0.001, 1000)
x_right = np.linspace(0.001, x_max, 1000)
y_left = k / x_left
y_right = k / x_right

# --- Matplotlib 그래프 ---
fig, ax = plt.subplots(figsize=(7, 7))

# 함수 그래프
ax.plot(x_left, y_left, 'b', label=f'y = {k:.2f}/x')
ax.plot(x_right, y_right, 'b')

# 점근선 (x=0, y=0)
ax.axvline(0, color='gray', linestyle='--', linewidth=1)
ax.axhline(0, color='gray', linestyle='--', linewidth=1)

# 대칭선 (y=x, y=-x)
xx = np.linspace(-x_range, x_range, 500)
ax.plot(xx, xx, color='lightblue', linestyle=':', linewidth=1, label='y = x')
ax.plot(xx, -xx, color='lightblue', linestyle=':', linewidth=1, label='y = -x')

# 대표점 표시
if show_points:
    xs = np.array([1, -1, 2, -2])
    ys = k / xs
    ax.scatter(xs, ys, color='crimson', s=50, label='대표점')
    for x, y in zip(xs, ys):
        ax.text(x, y, f"({x:.0f},{y:.1f})", fontsize=10, ha='left', va='bottom')

# 축 범위 및 비율
ax.set_xlim(-x_range, x_range)
ax.set_ylim(-x_range, x_range)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title(f"y = {k:.2f}/x  ｜  k의 부호: {'+' if k>0 else '-'}  ｜  |k| = {abs(k):.2f}")
ax.legend(loc="upper right")
ax.grid(True, linestyle=':')

st.pyplot(fig)

# --- 대표값 표 출력 ---
if show_table:
    st.subheader("대표 값 (예시)")
    xs_table = np.array([1, -1, 2, -2])
    ys_table = k / xs_table
    st.table({
        "x": [f"{x:.1f}" for x in xs_table],
        "y = k/x": [f"{y:.4f}" for y in ys_table],
    })

# --- 요약 정리 ---
st.markdown("---")
st.subheader("📖 핵심 정리")
st.markdown(
    """
- 정의역: \\(x \\neq 0\\)  
- 치역: \\(y \\neq 0\\)  
- 점근선: 수직 \\(x=0\\), 수평 \\(y=0\\)  
- 대칭성: 원점에 대해 대칭, y=x·y=-x에 대해 대칭 관계 존재  
- k>0 → 1사분면과 3사분면 / k<0 → 2사분면과 4사분면  
- |k| 커질수록 그래프가 축에서 멀어짐
"""
)

st.markdown("---")
st.caption("💡 제작: 유빈의 스트림릿 교과서 | © 2025")

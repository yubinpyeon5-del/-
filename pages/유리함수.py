# app.py
import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- 페이지 기본 설정 ---
st.set_page_config(page_title="유리함수 교과서 — y = k/x", layout="wide")

# --- 교과서 느낌 스타일 ---
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
    k = st.slider("k 값 (k ≠ 0)", min_value=-10.0, max_value=10.0, value=2.0, step=0.1)
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
- 이 함수는 **원점 대칭** 함수입니다.  
  → \\(f(-x) = -f(x)\\) 이므로 **홀함수**입니다.  
- 또한, 함수 \\(y = \\dfrac{k}{x}\\)의 그래프는  
  직선 **y = x** 와 **y = -x** 에 대해 서로 **대칭 관계**에 있습니다.  
  즉, \\(y = \\dfrac{k}{x}\\)를 y=x에 대해 대칭이동하면 \\(y = \\dfrac{x}{k}\\)가 되고,  
  y=-x에 대해 대칭이동하면 \\(y = -\\dfrac{x}{k}\\)가 됩니다.
"""
)

st.header("k 값에 따른 그래프의 변화")
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
x_left = np.linspace(x_min, -1e-6, 1000)
x_right = np.linspace(1e-6, x_max, 1000)
y_left = k / x_left
y_right = k / x_right

# --- 그래프 그리기 ---
fig = go.Figure()

# 유리함수 그래프
fig.add_trace(go.Scatter(x=x_left, y=y_left, mode="lines", name=f"y = {k:.2f}/x", line=dict(width=2)))
fig.add_trace(go.Scatter(x=x_right, y=y_right, mode="lines", showlegend=False, line=dict(width=2)))

# 점근선 (x=0, y=0)
fig.add_shape(type="line", x0=0, x1=0, y0=-x_range*10, y1=x_range*10,
              line=dict(color="gray", width=1, dash="dash"))
fig.add_shape(type="line", x0=-x_range, x1=x_range, y0=0, y1=0,
              line=dict(color="gray", width=1, dash="dash"))

# 대칭선 (y=x, y=-x)
fig.add_shape(type="line", x0=-x_range, x1=x_range, y0=-x_range, y1=x_range,
              line=dict(color="lightblue", width=1, dash="dot"))
fig.add_shape(type="line", x0=-x_range, x1=x_range, y0=x_range, y1=-x_range,
              line=dict(color="lightblue", width=1, dash="dot"))

# 대표점 표시
if show_points:
    xs = np.array([1, -1, 2, -2])
    ys = k / xs
    fig.add_trace(go.Scatter(
        x=xs, y=ys,
        mode="markers+text",
        text=[f"({x:.1f}, {y:.2f})" for x, y in zip(xs, ys)],
        textposition="top center",
        marker=dict(size=8, color="crimson"),
        name="대표점"
    ))

# 그래프 설정
fig.update_layout(
    title=f"그래프: y = {k:.2f}/x  ｜  k의 부호: {'+' if k>0 else '-'}  ｜  |k| = {abs(k):.2f}",
    xaxis=dict(title="x", range=[x_min, x_max], zeroline=False),
    yaxis=dict(title="y", range=[-x_range, x_range], zeroline=False),
    height=650,
    margin=dict(l=40, r=40, t=80, b=40),
)

# --- 그래프 출력 ---
st.plotly_chart(fig, use_container_width=True)

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
- 대칭성: 원점에 대하여 대칭, y=x·y=-x에 대해 대칭 관계 존재  
- k>0 → 1사분면과 3사분면 / k<0 → 2사분면과 4사분면  
- |k| 커질수록 그래프가 축에서 멀어짐  
"""
)

st.markdown("---")
st.caption("💡 제작: 유빈의 스트림릿 교과서 | © 2025")

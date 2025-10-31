import streamlit as st
import pandas as pd
import numpy as np

# 페이지 기본 설정
st.set_page_config(page_title="유리함수 y=k/x 교과서", layout="centered", page_icon="📘")
st.title("📘 유리함수 y = k/x (k ≠ 0)")

# 💡 배경색(#d4f4ff) + 글자색(검정) 스타일 적용
st.markdown(
    """
    <style>
    body {
        background-color: #d4f4ff;
        color: #000000;
    }
    .stApp {
        background-color: #d4f4ff;
        color: #000000;
    }
    h1, h2, h3, h4, h5, h6, p, span, div {
        color: #000000 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 🔹 유리함수 기본 개념
st.markdown("## 🔹 유리함수의 기본 개념")
st.write("""
유리함수는 **y = k/x (단, k ≠ 0)** 형태의 함수로,  
x가 0이 되면 정의되지 않습니다.  
따라서 **x=0은 정의역에 포함되지 않으며**,  
이때 그래프가 가까워지지만 닿지 않는 직선이 존재합니다.  
이를 **점근선(asymptote)** 이라고 합니다.
""")

# ✅ 정의역과 치역
st.markdown("### ✅ 정의역과 치역")
st.write("""
- **정의역**: x ≠ 0  
- **치역**: y ≠ 0  
그래프는 x=0, y=0인 두 축을 중심으로 네 부분(사분면)에 나뉘어 그려집니다.
""")

# 🔸 k 값 조절
k = st.slider("k 값을 조절해보세요", -5.0, 5.0, 1.0, 0.5)

# 데이터 생성
x1 = np.linspace(-10, -0.1, 200)
x2 = np.linspace(0.1, 10, 200)
y1 = k / x1
y2 = k / x2

# 데이터프레임 생성 (Streamlit 기본 그래프용)
df1 = pd.DataFrame({"x": x1, "y": y1})
df2 = pd.DataFrame({"x": x2, "y": y2})

st.markdown(f"### 📈 현재 그래프: y = {k}/x")

# 그래프 출력 (st.line_chart은 한 번에 하나의 그래프만 표시 가능)
st.line_chart(df1, x="x", y="y", height=400)
st.line_chart(df2, x="x", y="y", height=400)

# 📘 그래프 성질 정리
st.markdown("## 📘 그래프의 성질 정리")

if k > 0:
    st.write("""
    - 그래프는 **1사분면**과 **3사분면**에 그려집니다.  
    - x가 커질수록 y는 작아지고, x가 0에 가까워질수록 y는 커집니다.  
    - 즉, **x가 커질수록 y가 감소**하는 반비례 관계입니다.  
    """)
else:
    st.write("""
    - 그래프는 **2사분면**과 **4사분면**에 그려집니다.  
    - x가 커질수록 y의 절댓값이 작아지고, x가 0에 가까워질수록 y의 절댓값이 커집니다.  
    - 마찬가지로 **반비례 관계**이지만, y값이 음수가 됩니다.  
    """)

# 🔹 대칭성 설명
st.markdown("### 🔹 대칭성")
st.write("""
- 유리함수의 그래프는 **원점에 대하여 대칭**입니다.  
- 또한, \( y = 1/x \) 그래프는 \( y = x \) 에 대하여 대칭이고,  
  \( y = -1/x \) 그래프는 \( y = -x \) 에 대하여 대칭입니다.  
이를 통해 유리함수의 다양한 형태를 서로 연결해 이해할 수 있습니다.
""")

# ⚡ 점근선 설명
st.markdown("### ⚡ 점근선의 의미")
st.write("""
- 유리함수 y = k/x 에서, x가 0으로 가까워질수록 y는 무한히 커지거나 작아집니다.  
- 따라서 **x=0**은 그래프가 접근하지만 만나지 않는 세로선(**수직 점근선**)입니다.  
- 또한 **y=0**도 그래프가 접근하지만 만나지 않는 가로선(**수평 점근선**)입니다.
""")

# 마무리 문구
st.success("👉 이렇게 유리함수 y=k/x의 정의역, 치역, 대칭성, 점근선, 그래프 형태를 모두 이해할 수 있습니다!")

import streamlit as st
import random
import pandas as pd
from datetime import datetime

# 페이지 설정
st.set_page_config(page_title="로또 번호 생성기", layout="centered")
st.title("🎯 로또 번호 생성기 (대한민국 1~45 중 6개)")

# 사이드바 설정
st.sidebar.header("🔧 설정")
num_sets = st.sidebar.number_input("생성할 세트 수", min_value=1, max_value=50, value=1)
sort_choice = st.sidebar.checkbox("각 세트 정렬하여 표시하기", value=True)
seed_input = st.sidebar.text_input("랜덤 시드 (선택)", value="")
st.sidebar.markdown("---")
st.sidebar.write("📋 포함/제외 숫자는 쉼표(,)로 구분하세요. 예: 3, 7, 21")

include_raw = st.sidebar.text_input("강제로 포함할 숫자 (선택)")
exclude_raw = st.sidebar.text_input("제외할 숫자 (선택)")

# 문자열을 숫자 리스트로 변환
def parse_numbers(text):
    if not text:
        return []
    nums = []
    for part in text.split(","):
        try:
            n = int(part.strip())
            if 1 <= n <= 45:
                nums.append(n)
        except:
            continue
    return sorted(set(nums))

include_nums = parse_numbers(include_raw)
exclude_nums = parse_numbers(exclude_raw)

# 입력 검증
if len(include_nums) > 6:
    st.error("❌ 포함할 숫자는 최대 6개까지만 지정할 수 있습니다.")
    st.stop()

if set(include_nums) & set(exclude_nums):
    st.error("❌ 포함 숫자와 제외 숫자에 같은 값이 존재합니다.")
    st.stop()

if len(exclude_nums) >= 45:
    st.error("❌ 제외 숫자가 너무 많습니다.")
    st.stop()

# 시드 설정
if seed_input.strip():
    try:
        seed_val = int(seed_input)
    except:
        seed_val = sum(ord(c) for c in seed_input)
    random.seed(seed_val)

# 번호 생성 함수
def generate_lotto(include, exclude, sort_flag=True):
    pool = [n for n in range(1, 46) if n not in exclude and n not in include]
    need = 6 - len(include)
    if len(pool) < need:
        raise ValueError("조건에 맞는 번호를 생성할 수 없습니다.")
    picked = random.sample(pool, need)
    result = include + picked
    if sort_flag:
        result = sorted(result)
    return result

# 세션 상태 초기화
if "history" not in st.session_state:
    st.session_state.history = []

# 버튼
col1, col2 = st.columns([3, 1])

with col1:
    if st.button("✨ 로또 번호 생성하기"):
        try:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for i in range(num_sets):
                numbers = generate_lotto(include_nums, exclude_nums, sort_choice)
                st.session_state.history.append({
                    "time": now,
                    "set": i + 1,
                    "numbers": numbers
                })
            st.success(f"{num_sets}세트 생성 완료!")
            st.rerun()  # 최신 Streamlit 버전에서 지원됨
        except ValueError as e:
            st.error(str(e))

with col2:
    if st.button("🧹 히스토리 초기화"):
        st.session_state.history = []
        st.success("히스토리 초기화 완료")

# 최근 결과
st.subheader("📅 최근 생성 결과")
if st.session_state.history:
    recent = st.session_state.history[-num_sets:]
    df_recent = pd.DataFrame([
        {
            "시간": r["time"],
            "세트번호": r["set"],
            "번호": ", ".join(map(str, r["numbers"]))
        }
        for r in reversed(recent)
    ])
    st.table(df_recent)
else:
    st.info("아직 생성된 번호가 없습니다. ‘로또 번호 생성하기’를 눌러보세요.")

# 전체 히스토리
st.subheader("📜 전체 생성 히스토리")
if st.session_state.history:
    df_all = pd.DataFrame([
        {
            "시간": h["time"],
            "세트": h["set"],
            **{f"번호{i+1}": (h["numbers"][i] if i < len(h["numbers"]) else "") for i in range(6)}
        }
        for h in st.session_state.history
    ])
    st.dataframe(df_all)

    csv = df_all.to_csv(index=False).encode("utf-8-sig")
    st.download_button("⬇️ CSV로 다운로드", csv, "lotto_history.csv", "text/csv")
else:
    st.write("히스토리가 비어 있습니다.")

# 도움말
st.markdown("---")
st.markdown("### ℹ️ 사용 방법")
st.markdown("""
- **강제로 포함할 숫자**: 반드시 포함할 번호 (예: `7, 14, 22`)  
- **제외할 숫자**: 절대 포함되지 않을 번호 (예: `1, 2, 3`)  
- **랜덤 시드**: 같은 시드를 넣으면 같은 번호가 나옵니다.  
- 생성된 번호는 항상 **1~45 사이의 중복 없는 6개 숫자**입니다.
""")
st.caption("⚠️ 이 앱은 오락용이며, 실제 복권 당첨과는 무관합니다.")

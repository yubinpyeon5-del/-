import streamlit as st
import random
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="로또 번호 생성기", layout="centered")

st.title("🎯 로또 번호 생성기 (한국식: 1–45 중 6개)")

# --- 사이드바 옵션 ---
st.sidebar.header("설정")
num_sets = st.sidebar.number_input("생성할 세트 수", min_value=1, max_value=50, value=1, step=1)
sort_choice = st.sidebar.checkbox("각 세트 정렬하여 표시하기", value=True)
seed_input = st.sidebar.text_input("랜덤 시드 (선택, 비워두면 무작위)", value="")
st.sidebar.markdown("---")
st.sidebar.write("포함/제외 숫자는 쉼표(,)로 구분하세요. 예: 3,7,21")

include_raw = st.sidebar.text_input("강제로 포함할 숫자 (선택)")
exclude_raw = st.sidebar.text_input("제외할 숫자 (선택)")

# --- 파싱 유틸 ---
def parse_numbers(text):
    """쉼표로 구분된 숫자 문자열을 파싱하여 유효 숫자 리스트 반환 (1~45 범위)"""
    if not text:
        return []
    out = []
    for part in text.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            n = int(part)
            if 1 <= n <= 45:
                out.append(n)
        except:
            # 무시: 비숫자 입력
            continue
    # 중복 제거, 원래 순서 유지
    seen = set()
    uniq = []
    for x in out:
        if x not in seen:
            uniq.append(x)
            seen.add(x)
    return uniq

include_nums = parse_numbers(include_raw)
exclude_nums = parse_numbers(exclude_raw)

# --- 입력 검증 ---
error_msgs = []
if len(include_nums) > 6:
    error_msgs.append("포함할 숫자는 최대 6개까지만 지정할 수 있습니다.")
if set(include_nums) & set(exclude_nums):
    error_msgs.append("포함할 숫자와 제외할 숫자에 같은 값이 존재합니다.")
if len(exclude_nums) >= 45:
    error_msgs.append("제외할 숫자가 너무 많아 유효한 조합을 만들 수 없습니다.")

if error_msgs:
    for em in error_msgs:
        st.error(em)
    st.stop()

# --- 시드 설정 ---
if seed_input.strip() != "":
    try:
        seed_val = int(seed_input)
    except:
        seed_val = sum(ord(c) for c in seed_input)  # 문자열 시드도 사용
    random.seed(seed_val)

# --- 로또 생성 함수 ---
def generate_one(include, exclude):
    pool = [n for n in range(1, 46) if n not in exclude and n not in include]
    need = 6 - len(include)
    if need < 0:
        raise ValueError("포함 숫자가 6개를 초과합니다.")
    if len(pool) < need:
        raise ValueError("포함/제외 조건 때문에 가능한 조합이 없습니다.")
    picked = random.sample(pool, need)
    result = sorted(include + picked) if sort_choice else (include + picked)
    # 정렬하지 않을 때도 보기 편하게 내부적으로는 정리
    if not sort_choice:
        # 섞어 표시하려면 섞음
        random.shuffle(result)
    return result

# --- 세트 생성 및 히스토리 관리 (session_state) ---
if "history" not in st.session_state:
    st.session_state.history = []  # 리스트 of dicts: {"time":..., "numbers":[...], "seed":...}

col_generate, col_clear = st.columns([3,1])
with col_generate:
    if st.button("✨ 생성하기"):
        generated = []
        try:
            for i in range(num_sets):
                one = generate_one(include_nums, exclude_nums)
                generated.append(one)
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # 히스토리에 저장 (각 세트를 개별 항목으로 저장)
            for idx, gs in enumerate(generated, start=1):
                st.session_state.history.append({
                    "time": now,
                    "set_index": idx,
                    "numbers": gs
                })
            st.success(f"{len(generated)}세트 생성됨")
            st.experimental_rerun()  # 생성 결과를 바로 화면에 보여주기 위해 리런
        except ValueError as e:
            st.error(str(e))

with col_clear:
    if st.button("히스토리 초기화"):
        st.session_state.history = []
        st.success("히스토리 초기화 완료")

# --- 결과 영역 ---
st.subheader("최근 생성 결과")
if st.session_state.history:
    # 최신 항목(생성된 가장 마지막 num_sets개) 표시
    last = st.session_state.history[-num_sets:]
    # 표로 보기 쉽게 변환
    rows = []
    for item in reversed(last):  # 최신이 위에
        rows.append({
            "시간": item["time"],
            "세트번호": item["set_index"],
            "번호": ", ".join(str(x) for x in item["numbers"])
        })
    df_recent = pd.DataFrame(rows)
    st.table(df_recent)
else:
    st.info("아직 생성된 번호가 없습니다. '생성하기' 버튼을 눌러보세요.")

# --- 전체 히스토리 & 다운로드 ---
st.subheader("전체 생성 히스토리")
if st.session_state.history:
    df_all = pd.DataFrame([{
        "시간": h["time"],
        "세트번호": h["set_index"],
        **{f"번호{i+1}": (h["numbers"][i] if i < len(h["numbers"]) else "") for i in range(6)}
    } for h in st.session_state.history])
    # 보여주기
    st.dataframe(df_all)
    # CSV 다운로드
    csv = df_all.to_csv(index=False).encode('utf-8-sig')
    st.download_button("CSV로 다운로드", data=csv, file_name="lotto_history.csv", mime="text/csv")
else:
    st.write("히스토리가 비어있습니다.")

# --- 도움말 / 사용 예시 ---
st.markdown("---")
st.markdown("**사용 팁**")
st.markdown("""
- 특정 숫자를 꼭 포함시키고 싶으면 '강제로 포함할 숫자'에 입력하세요.  
- 특정 번호를 피하고 싶다면 '제외할 숫자'에 입력하세요.  
- 포함 숫자 3개를 미리 정하면 나머지 3개를 무작위로 채워 6개 세트를 만듭니다.
""")
st.caption("앱은 교육/연습용입니다. 복권 구매·당첨과는 무관합니다.")

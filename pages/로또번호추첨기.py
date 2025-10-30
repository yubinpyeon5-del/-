import streamlit as st
import random
import pandas as pd
from datetime import datetime

# --- 기본 설정 ---
st.set_page_config(page_title="로또 번호 생성기", layout="centered")
st.title("🎯 로또 번호 생성기 (대한민국 1~45 중 6개)")

# --- 사이드바 설정 ---
st.sidebar.header("🔧 설정")
num_sets = st.sidebar.number_input("생성할 세트 수", min_value=1, max_value=50, value=1)
sort_choice = st.sidebar.checkbox("각 세트 정렬하여 표시하기", value=True)
seed_input = st.sidebar.text_input("랜덤 시드 (선택)", value="")
st.sidebar.markdown("---")
st.sidebar.write("📋 포함/제외 숫자는 쉼표(,)로 구분하세요. 예: 3, 7, 21")

include_raw = st.sidebar.text_input("강제로 포함할 숫자 (선택)")
exclude_raw = st.sidebar.text_input("제외할 숫자 (선택)")

# --- 숫자 파싱 함수 ---
def parse_numbers(text):
    """쉼표로 구분된 숫자 문자열을 정수 리스트로 변환 (1~45 범위)"""
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
    # 중복 제거
    nums = sorted(set(nums))
    return nums

include_nums = parse_numbers(include_raw)
exclude_nums = parse_numbers(exclude_raw)

# --- 입력 검증 ---
if len(include_nums) > 6:
    st.error("❌ 포함할 숫자는 최대 6개까지만 지정할 수 있습니다.")
    st.stop()

if set(include_nums) & set(exclude_nums):
    st.error("❌ 포함 숫자와 제외 숫자에 같은 값이 존재합니다.")
    st.stop()

if len(exclude_nums) >= 45:
    st.error("❌ 제외 숫자가 너무 많습니다. 가능한 조합이 없습니다.")
    st.stop()

# --- 랜덤 시드 설정 ---
if seed_input.strip():
    try:
        seed_val = int(seed_input)
    except:
        seed_val = sum(ord(c) for c in seed_input)
    random.seed(seed_val)

# --- 번호 생성 함수 ---
def generate_lotto(include, exclude, sort_flag=True):
    pool = [n for n in range(1, 46) if n not in exclude and n not in include]
    need = 6 - len(include)
    if len(pool) < need:
        raise ValueError("조건

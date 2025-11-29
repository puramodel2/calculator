import streamlit as st
import math

# --- 페이지 설정 ---
st.set_page_config(
    page_title="다기능 계산기",
    layout="wide"
)

st.title("🔢 다기능 계산기 웹앱")
st.markdown("---")

# --- 계산 함수 정의 ---

def calculate(num1, operation, num2=None):
    """
    선택된 연산에 따라 계산을 수행하는 함수.
    이항 연산(사칙, 모듈러, 지수)과 단항 연산(로그)을 모두 처리합니다.
    """
    try:
        # 사칙연산, 모듈러 연산, 지수 연산 (이항 연산)
        if operation == '+':
            return num1 + num2
        elif operation == '-':
            return num1 - num2
        elif operation == '*':
            return num1 * num2
        elif operation == '/':
            if num2 == 0:
                st.error("오류: 0으로 나눌 수 없습니다.")
                return None
            return num1 / num2
        elif operation == '% (모듈러)':
            return num1 % num2
        elif operation == '** (지수)':
            return num1 ** num2
        
        # 로그 연산 (단항 연산)
        elif operation == 'log (밑 10)':
            if num1 <= 0:
                st.error("오류: 로그의 진수는 0보다 커야 합니다.")
                return None
            return math.log10(num1)
        
        # 자연로그 연산 (추가)
        elif operation == 'ln (자연로그)':
            if num1 <= 0:
                st.error("오류: 로그의 진수는 0보다 커야 합니다.")
                return None
            return math.log(num1) # math.log()는 자연로그 (밑 e)입니다.

    except TypeError:
        st.error("오류: 유효한 숫자를 입력하세요.")
        return None
    except Exception as e:
        st.error(f"계산 중 오류가 발생했습니다: {e}")
        return None

# --- UI 구성 ---

# 1. 숫자 입력 및 연산자 선택
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.header("입력")
    
    # 연산 선택
    operation = st.selectbox(
        "**수행할 연산을 선택하세요**",
        ('+', '-', '*', '/', '% (모듈러)', '** (지수)', 'log (밑 10)', 'ln (자연로그)')
    )
    
    # 연산에 따라 입력 필드 다르게 표시
    if operation in ['log (밑 10)', 'ln (자연로그)']:
        # 단항 연산 (로그)
        num1 = st.number_input("**숫자 (진수)**", value=10.0, step=0.1)
        num2 = None # 사용하지 않음
        st.caption("로그 연산은 **첫 번째 입력 값**을 진수로 사용합니다.")
    else:
        # 이항 연산 (사칙, 모듈러, 지수)
        num1 = st.number_input("**첫 번째 숫자 (Operand 1)**", value=10.0, step=0.1)
        num2 = st.number_input("**두 번째 숫자 (Operand 2)**", value=5.0, step=0.1)
    
with col2:
    st.header("연산")
    st.markdown(f"## {operation}")

with col3:
    st.header("결과")
    
    # 2. 계산 버튼
    if st.button("계산하기 🟰", key='calculate_button', help="입력된 값으로 계산을 수행합니다.", use_container_width=True):
        
        # 3. 계산 및 결과 표시
        result = calculate(num1, operation, num2)
        
        if result is not None:
            st.success(f"**결과:**")
            st.markdown(f"## `{result:.4f}`") # 소수점 4자리까지 표시
        
st.markdown("---")

# --- 기능 설명 ---
st.info("""
### ✨ 구현된 기능
* **사칙연산:** `+`, `-`, `*`, `/` (더하기, 빼기, 곱하기, 나누기)
* **모듈러 연산:** `% (나머지)`
* **지수 연산:** `** (거듭제곱)`
* **로그 연산:** `log (밑 10)` (상용로그), `ln (자연로그)` (밑 $e$)
""")

#
